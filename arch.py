from binaryninja import Architecture, InstructionInfo, RegisterInfo, IntrinsicInfo,Type
from .disassembly import *
from .lifter import VMMODlifter

class VMMODarch(Architecture):
    name = "vmmod"

    default_int_size = 2
    address_size = 2
    max_instruction_length = 5

    stack_pointer = "sp"
    regs = {
        "sp":RegisterInfo("sp",2)
    }
    for x in range(23):
        regs[f"r{x}"] = RegisterInfo(f"r{x}",2)
    
    opcodes = {
        0 : default,
        1 : pr,
        2 : call,
        3 : ret,
        4 : remap,
        5 : default,
        6 : default,
        7 : default,
        8 : default,
        9 : default,
        0xa : f_not,
        0xb : jz,
        0xc : jmp,
        0xd : default,
        0xe : store,
        0xf : ld,
        0x12 : read1,
        0xff : f_exit
    }

    intrinsics = {
        "read":IntrinsicInfo([Type.int(2)],[]),
        "print":IntrinsicInfo([Type.int(2)],[]),
        "exit":IntrinsicInfo([],[]),
        "remap":IntrinsicInfo([Type.int(2),Type.int(2)],[])
    }

    def __init__(self):
        super().__init__()

    def get_instruction_info(self,data,addr):
        try:
            op = data[0]
            tokens,length,cond = VMMODarch.opcodes[op](data,addr)
            result = InstructionInfo()
            result.length = length 
            for c in cond:
                if c[1] is not None:
                    result.add_branch(c[0],c[1])
                else:
                    result.add_branch(c[0])
            return result
        except KeyError:
            pass

    def get_instruction_text(self,data,addr):
        try:
            op = data[0]
            tokens,length,cond = VMMODarch.opcodes[op](data,addr)
            return tokens,length
        except KeyError:
            pass

    def get_instruction_low_level_il(self,data,addr,il):
        try:
            op = data[0]
            disas = VMMODarch.opcodes[op](data,addr)
            return VMMODlifter.opcodes[op](data,addr,il,disas)
        except KeyError:
            pass
