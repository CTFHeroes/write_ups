str = [
    0x71,
    0x76,
    0x4E,
    0x71,
    0x62,
    0x79,
    0x26,
    0x49,
    0x70,
    0x7B,
    0x7E,
    0x79,
    0x73,
    0x2D,
    0x31,
    0x7A,
    0x44,
    0x4C,
    0x0E,
    0x4C,
    0x2D,
    0x57,
    0x53,
    0x4C,
    0x5A,
    0x1D,
    0x4A,
    0x5A,
    0x47,
    0x2D,
    0x43,
    0x5F,
    0x59,
    0x42,
    0x5F,
    0x1D,
    0x4C,
]

print(
    "".join(
        chr((v ^ (i + 16)) + 5) if i not in [13, 20, 29] else "-"
        for i, v in enumerate(str)
    )
)
# if ( v6[0] )
#   {
#     do
#       ++v3;
#     while ( v6[v3] );
#     if ( v3 == 37 && v6[13] == 45 && v6[20] == 45 && v6[29] == 45 )
#     {
#       v4 = 0;
#       while ( v4 == 13 || v4 == 20 || v4 == 29 || ((v4 + 16) ^ (v6[v4] - 5)) == dword_402138[v4] )
#       {
#         if ( ++v4 >= 37 )
#         {
#           sub_401020("success");
#           return 0;
#         }
#       }
#     }
#   }
