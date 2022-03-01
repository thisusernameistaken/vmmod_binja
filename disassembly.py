from binaryninja import InstructionTextToken, InstructionTextTokenType,BranchType
import struct

def ld(data,addr):
    tokens = [InstructionTextToken(InstructionTextTokenType.TextToken, "ld")]
    length = 5
    dest = data[1]
    off = data[2:4]
    off = struct.unpack("<h",off)[0]
    source = data[4]
    dest = dest-0x80
    reg = f"r{dest}"
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken,reg))
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ', '))
    if source & 0x80 !=0:
        source = source-0x80
        s_reg = f"r{source}"
        tokens.append(InstructionTextToken(InstructionTextTokenType.CodeRelativeAddressToken, hex(addr+5),addr+5))
        tokens.append(InstructionTextToken(InstructionTextTokenType.BeginMemoryOperandToken,"("))
        tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken,s_reg))
        tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' + '))
        tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, hex(off),off))
        tokens.append(InstructionTextToken(InstructionTextTokenType.EndMemoryOperandToken,")"))
    else:
        tokens.append(InstructionTextToken(InstructionTextTokenType.CodeRelativeAddressToken, hex(addr+5),addr+5))
        tokens.append(InstructionTextToken(InstructionTextTokenType.BeginMemoryOperandToken,"("))
        tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, hex(off+source),off+source))
        tokens.append(InstructionTextToken(InstructionTextTokenType.EndMemoryOperandToken,")"))
        
    return tokens,length,[]

def store(data,addr):
    tokens = [InstructionTextToken(InstructionTextTokenType.TextToken, "store")]
    length = 5
    dest = data[1]
    off = data[2:4]
    off = struct.unpack("<h",off)[0]
    source = data[4]
    dest = dest-0x80
    reg = f"r{dest}"
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken,reg))
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ', '))
    if source & 0x80 !=0:
        source = source-0x80
        s_reg = f"r{source}"
        tokens.append(InstructionTextToken(InstructionTextTokenType.CodeRelativeAddressToken, hex(addr+5),value=addr+5))
        tokens.append(InstructionTextToken(InstructionTextTokenType.BeginMemoryOperandToken,"("))
        tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken,s_reg))
        tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' + '))
        tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, hex(off),off))
        tokens.append(InstructionTextToken(InstructionTextTokenType.EndMemoryOperandToken,")"))
    else:
        tokens.append(InstructionTextToken(InstructionTextTokenType.CodeRelativeAddressToken, hex(addr+5),addr+5))
        tokens.append(InstructionTextToken(InstructionTextTokenType.BeginMemoryOperandToken,"("))
        tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, hex(off+source),off+source))
        tokens.append(InstructionTextToken(InstructionTextTokenType.EndMemoryOperandToken,")"))
        
    return tokens,length,[]

def jmp(data,addr):
    tokens = [InstructionTextToken(InstructionTextTokenType.TextToken, "jmp")]
    target = data[1:3]
    t = struct.unpack("<h",target)[0]+3
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
    tokens.append(InstructionTextToken(InstructionTextTokenType.CodeRelativeAddressToken, hex(addr+t),addr+t))
    length = 3
    cond = [(BranchType.UnconditionalBranch,addr+t)]
    return tokens,length,cond

def call(data,addr):
    tokens = [InstructionTextToken(InstructionTextTokenType.TextToken, "call")]
    target = data[1:3]
    t = struct.unpack("<h",target)[0]+3
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
    tokens.append(InstructionTextToken(InstructionTextTokenType.CodeRelativeAddressToken, hex(addr+t),addr+t))
    length = 3
    cond = [(BranchType.CallDestination,addr+t)]
    return tokens,length,cond

def jz(data,addr):
    tokens = [InstructionTextToken(InstructionTextTokenType.TextToken, "jz")]
    dest = data[1]
    dest = dest-0x80
    reg = f"r{dest}"
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken,reg))
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ', '))
    target = data[2:4]
    t = struct.unpack("<h",target)[0]+4
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
    tokens.append(InstructionTextToken(InstructionTextTokenType.CodeRelativeAddressToken, hex(addr+t),addr+t))
    length = 4
    cond = [(BranchType.TrueBranch,addr+t),(BranchType.FalseBranch,addr+4)]
    return tokens,length,cond

def ret(data,addr):
    tokens = [InstructionTextToken(InstructionTextTokenType.TextToken, "ret")]
    length = 1
    cond = [(BranchType.FunctionReturn,None)]
    return tokens,length,cond

def f_exit(data,addr):
    tokens = [InstructionTextToken(InstructionTextTokenType.TextToken, "exit")]
    length = 1
    cond = [(BranchType.FunctionReturn,None)]
    return tokens,length,cond

def read1(data,addr):
    tokens = [InstructionTextToken(InstructionTextTokenType.TextToken, "read")]
    length = 2
    dest = data[1]
    dest = dest-0x80
    reg = f"r{dest}"
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken,reg))
    return tokens,length,[]

def pr(data,addr):
    tokens = [InstructionTextToken(InstructionTextTokenType.TextToken, "print")]
    length = 2
    dest = data[1]
    dest = dest-0x80
    reg = f"r{dest}"
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken,reg))
    return tokens,length,[]

def f_not(data,addr):
    tokens = [InstructionTextToken(InstructionTextTokenType.TextToken, "not")]
    length = 2
    dest = data[1]
    dest = dest-0x80
    reg = f"r{dest}"
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken,reg))
    return tokens,length,[]

def remap(data,addr):
    tokens = [InstructionTextToken(InstructionTextTokenType.TextToken, "remap")]
    length = 3
    dest = data[1]
    source = data[2]
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
    tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, hex(dest),dest))
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ', '))
    tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, hex(source),source))
    return tokens,length,[]

def default(data,addr):
    default_instrs = {
        0:"mov",
        5:"add",
        6:"and",
        7:"xor",
        8:"shl",
        9:"shr",
        0xd:"sub"
    }
    tokens = [InstructionTextToken(InstructionTextTokenType.TextToken, default_instrs[data[0]])]
    length = 3
    dest = data[1]
    source = data[2]
    dest = dest-0x80
    reg = f"r{dest}"
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ' '))
    tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken,reg))
    tokens.append(InstructionTextToken(InstructionTextTokenType.TextToken, ', '))
    if source & 0x80 !=0:
        source = source-0x80
        s_reg = f"r{source}"
        tokens.append(InstructionTextToken(InstructionTextTokenType.RegisterToken,s_reg))
    else:
        tokens.append(InstructionTextToken(InstructionTextTokenType.IntegerToken, hex(source),source))
    return tokens,length,[]