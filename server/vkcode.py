VK_CODE = [None] * 255

VK_SHIFT = [0x10, 0xa0, 0xa1]
VK_CAPS_LOCK = 0x14

def NormalChar(vkCode):
    return (vkCode >=0x30 and vkCode <=0x39) or (vkCode >=0x41 and vkCode <=0x5a) or (vkCode >= 0x60 and vkCode <= 0x6f and vkCode != 0x6c) or (vkCode >=0xca and vkCode <=0xd0) or (vkCode >=0xdb and vkCode <=0xde) or vkCode == 0x20

VK_CODE[0x00] = 'UKN'
VK_CODE[0x01] = 'UKN'
VK_CODE[0x02] = 'UKN'
VK_CODE[0x03] = 'UKN'
VK_CODE[0x04] = 'UKN'
VK_CODE[0x05] = 'UKN'
VK_CODE[0x06] = 'UKN'
VK_CODE[0x07] = 'UKN'
VK_CODE[0x08] = 'BACKSPACE'
VK_CODE[0x09] = 'TAB'
VK_CODE[0x0a] = 'UKN'
VK_CODE[0x0b] = 'UKN'
VK_CODE[0x0c] = 'CLEAR'
VK_CODE[0x0d] = 'ENTER'
VK_CODE[0x0e] = 'UKN'
VK_CODE[0x0f] = 'UKN'
VK_CODE[0x10] = 'SHIFT'
VK_CODE[0x11] = 'CTRL'
VK_CODE[0x12] = 'ALT'
VK_CODE[0x13] = 'PAUSE'
VK_CODE[0x14] = 'CAPSLOCK'
VK_CODE[0x15] = 'UKN'
VK_CODE[0x16] = 'UKN'
VK_CODE[0x17] = 'UKN'
VK_CODE[0x18] = 'UKN'
VK_CODE[0x19] = 'UKN'
VK_CODE[0x1a] = 'UKN'
VK_CODE[0x1b] = 'ESCAPE'
VK_CODE[0x1c] = 'UKN'
VK_CODE[0x1d] = 'UKN'
VK_CODE[0x1e] = 'UKN'
VK_CODE[0x1f] = 'UKN'
VK_CODE[0x20] = ' '
VK_CODE[0x21] = 'PAGEUP'
VK_CODE[0x22] = 'PAGEDOWN'
VK_CODE[0x23] = 'END'
VK_CODE[0x24] = 'HOME'
VK_CODE[0x25] = 'LEFTARROW'
VK_CODE[0x26] = 'UPARROW'
VK_CODE[0x27] = 'RIGHTARROW'
VK_CODE[0x28] = 'DOWNARROW'
VK_CODE[0x29] = 'SELECT'
VK_CODE[0x2a] = 'PRINT'
VK_CODE[0x2b] = 'EXECUTE'
VK_CODE[0x2c] = 'PRINTSCREEN'
VK_CODE[0x2d] = 'INSERT'
VK_CODE[0x2e] = 'DELETE'
VK_CODE[0x2f] = 'HELP'
VK_CODE[0x30] = '0'
VK_CODE[0x31] = '1'
VK_CODE[0x32] = '2'
VK_CODE[0x33] = '3'
VK_CODE[0x34] = '4'
VK_CODE[0x35] = '5'
VK_CODE[0x36] = '6'
VK_CODE[0x37] = '7'
VK_CODE[0x38] = '8'
VK_CODE[0x39] = '9'
VK_CODE[0x3a] = 'UKN'
VK_CODE[0x3b] = 'UKN'
VK_CODE[0x3c] = 'UKN'
VK_CODE[0x3d] = 'UKN'
VK_CODE[0x3e] = 'UKN'
VK_CODE[0x3f] = 'UKN'
VK_CODE[0x40] = 'UKN'
VK_CODE[0x41] = ('a', 'A')
VK_CODE[0x42] = ('b', 'B')
VK_CODE[0x43] = ('c', 'C')
VK_CODE[0x44] = ('d', 'D')
VK_CODE[0x45] = ('e', 'E')
VK_CODE[0x46] = ('f', 'F')
VK_CODE[0x47] = ('g', 'G')
VK_CODE[0x48] = ('h', 'H')
VK_CODE[0x49] = ('i', 'I')
VK_CODE[0x4a] = ('j', 'J')
VK_CODE[0x4b] = ('k', 'K')
VK_CODE[0x4c] = ('l', 'L')
VK_CODE[0x4d] = ('m', 'M')
VK_CODE[0x4e] = ('n', 'N')
VK_CODE[0x4f] = ('o', 'O')
VK_CODE[0x50] = ('p', 'P')
VK_CODE[0x51] = ('q', 'Q')
VK_CODE[0x52] = ('r', 'R')
VK_CODE[0x53] = ('s', 'S')
VK_CODE[0x54] = ('t', 'T')
VK_CODE[0x55] = ('u', 'U')
VK_CODE[0x56] = ('v', 'V')
VK_CODE[0x57] = ('w', 'W')
VK_CODE[0x58] = ('x', 'X')
VK_CODE[0x59] = ('y', 'Y')
VK_CODE[0x5a] = ('z', 'Z')
VK_CODE[0x5b] = 'LWINDOW'
VK_CODE[0x5c] = 'RWINDOW'
VK_CODE[0x5d] = 'APPS'
VK_CODE[0x5e] = 'UKN'
VK_CODE[0x5f] = 'SLEEP'
VK_CODE[0x60] = '0'
VK_CODE[0x61] = '1'
VK_CODE[0x62] = '2'
VK_CODE[0x63] = '3'
VK_CODE[0x64] = '4'
VK_CODE[0x65] = '5'
VK_CODE[0x66] = '6'
VK_CODE[0x67] = '7'
VK_CODE[0x68] = '8'
VK_CODE[0x69] = '9'
VK_CODE[0x6a] = '*'
VK_CODE[0x6b] = '+'
VK_CODE[0x6c] = 'UKN'
VK_CODE[0x6d] = '-'
VK_CODE[0x6e] = '.'
VK_CODE[0x6f] = '/'
VK_CODE[0x70] = 'F1'
VK_CODE[0x71] = 'F2'
VK_CODE[0x72] = 'F3'
VK_CODE[0x73] = 'F4'
VK_CODE[0x74] = 'F5'
VK_CODE[0x75] = 'F6'
VK_CODE[0x76] = 'F7'
VK_CODE[0x77] = 'F8'
VK_CODE[0x78] = 'F9'
VK_CODE[0x79] = 'F10'
VK_CODE[0x7a] = 'F11'
VK_CODE[0x7b] = 'F12'
VK_CODE[0x7c] = 'F13'
VK_CODE[0x7d] = 'F14'
VK_CODE[0x7e] = 'F15'
VK_CODE[0x7f] = 'F16'
VK_CODE[0x80] = 'F17'
VK_CODE[0x81] = 'F18'
VK_CODE[0x82] = 'F19'
VK_CODE[0x83] = 'F20'
VK_CODE[0x84] = 'F21'
VK_CODE[0x85] = 'F22'
VK_CODE[0x86] = 'F23'
VK_CODE[0x87] = 'F24'
VK_CODE[0x88] = 'UKN'
VK_CODE[0x89] = 'UKN'
VK_CODE[0x8a] = 'UKN'
VK_CODE[0x8b] = 'UKN'
VK_CODE[0x8c] = 'UKN'
VK_CODE[0x8d] = 'UKN'
VK_CODE[0x8e] = 'UKN'
VK_CODE[0x8f] = 'UKN'
VK_CODE[0x90] = 'NUMLOCK'
VK_CODE[0x91] = 'SCROLLLOCK'
VK_CODE[0x92] = 'UKN'
VK_CODE[0x93] = 'UKN'
VK_CODE[0x94] = 'UKN'
VK_CODE[0x95] = 'UKN'
VK_CODE[0x96] = 'UKN'
VK_CODE[0x97] = 'UKN'
VK_CODE[0x98] = 'UKN'
VK_CODE[0x99] = 'UKN'
VK_CODE[0x9a] = 'UKN'
VK_CODE[0x9b] = 'UKN'
VK_CODE[0x9c] = 'UKN'
VK_CODE[0x9d] = 'UKN'
VK_CODE[0x9e] = 'UKN'
VK_CODE[0x9f] = 'UKN'
VK_CODE[0xa0] = 'LSHIFT'
VK_CODE[0xa1] = 'RSHIFT'
VK_CODE[0xa2] = 'LCTRL'
VK_CODE[0xa3] = 'RCTRL'
VK_CODE[0xa4] = 'LMENU'
VK_CODE[0xa5] = 'RMENU'
VK_CODE[0xa6] = 'UKN'
VK_CODE[0xa7] = 'UKN'
VK_CODE[0xa8] = 'UKN'
VK_CODE[0xa9] = 'UKN'
VK_CODE[0xaa] = 'UKN'
VK_CODE[0xab] = 'UKN'
VK_CODE[0xac] = 'UKN'
VK_CODE[0xad] = 'UKN'
VK_CODE[0xae] = 'UKN'
VK_CODE[0xaf] = 'UKN'
VK_CODE[0xb0] = 'UKN'
VK_CODE[0xb1] = 'UKN'
VK_CODE[0xb2] = 'UKN'
VK_CODE[0xb3] = 'UKN'
VK_CODE[0xb4] = 'UKN'
VK_CODE[0xb5] = 'UKN'
VK_CODE[0xb6] = 'UKN'
VK_CODE[0xb7] = 'UKN'
VK_CODE[0xb8] = 'UKN'
VK_CODE[0xb9] = 'UKN'
VK_CODE[0xba] = (';',':')
VK_CODE[0xbb] = ('=','+')
VK_CODE[0xbc] = (',','<')
VK_CODE[0xbd] = ('-','_')
VK_CODE[0xbe] = ('.','>')
VK_CODE[0xbf] = ('/','?')
VK_CODE[0xc0] = ('`','~')
VK_CODE[0xc1] = 'UKN'
VK_CODE[0xc2] = 'UKN'
VK_CODE[0xc3] = 'UKN'
VK_CODE[0xc4] = 'UKN'
VK_CODE[0xc5] = 'UKN'
VK_CODE[0xc6] = 'UKN'
VK_CODE[0xc7] = 'UKN'
VK_CODE[0xc8] = 'UKN'
VK_CODE[0xc9] = 'UKN'
VK_CODE[0xca] = 'UKN'
VK_CODE[0xcb] = 'UKN'
VK_CODE[0xcc] = 'UKN'
VK_CODE[0xcd] = 'UKN'
VK_CODE[0xce] = 'UKN'
VK_CODE[0xcf] = 'UKN'
VK_CODE[0xd0] = 'UKN'
VK_CODE[0xd1] = 'UKN'
VK_CODE[0xd2] = 'UKN'
VK_CODE[0xd3] = 'UKN'
VK_CODE[0xd4] = 'UKN'
VK_CODE[0xd5] = 'UKN'
VK_CODE[0xd6] = 'UKN'
VK_CODE[0xd7] = 'UKN'
VK_CODE[0xd8] = 'UKN'
VK_CODE[0xd9] = 'UKN'
VK_CODE[0xda] = 'UKN'
VK_CODE[0xdb] = ('(','{')
VK_CODE[0xdc] = ('\\','|')
VK_CODE[0xdd] = (')','}')
VK_CODE[0xde] = ('\'','\"')
VK_CODE[0xdf] = 'UKN'
VK_CODE[0xe0] = 'UKN'
VK_CODE[0xe1] = 'UKN'
VK_CODE[0xe2] = 'UKN'
VK_CODE[0xe3] = 'UKN'
VK_CODE[0xe4] = 'UKN'
VK_CODE[0xe5] = 'UKN'
VK_CODE[0xe6] = 'UKN'
VK_CODE[0xe7] = 'UKN'
VK_CODE[0xe8] = 'UKN'
VK_CODE[0xe9] = 'UKN'
VK_CODE[0xea] = 'UKN'
VK_CODE[0xeb] = 'UKN'
VK_CODE[0xec] = 'UKN'
VK_CODE[0xed] = 'UKN'
VK_CODE[0xee] = 'UKN'
VK_CODE[0xef] = 'UKN'
VK_CODE[0xf0] = 'UKN'
VK_CODE[0xf1] = 'UKN'
VK_CODE[0xf2] = 'UKN'
VK_CODE[0xf3] = 'UKN'
VK_CODE[0xf4] = 'UKN'
VK_CODE[0xf5] = 'UKN'
VK_CODE[0xf6] = 'UKN'
VK_CODE[0xf7] = 'UKN'
VK_CODE[0xf8] = 'UKN'
VK_CODE[0xf9] = 'UKN'
VK_CODE[0xfa] = 'UKN'
VK_CODE[0xfb] = 'UKN'
VK_CODE[0xfc] = 'UKN'
VK_CODE[0xfd] = 'UKN'
VK_CODE[0xfe] = 'UKN'