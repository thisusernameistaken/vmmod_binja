from binaryninja import ILRegister, Architecture, InstructionTextTokenType, LowLevelILLabel
from .disassembly import *

def mov(data,addr,il,disas):
    tokens = disas[0]
    dest = tokens[2]
    source = tokens[4]
    if source.type == InstructionTextTokenType.RegisterToken:
        il.append(il.set_reg(2,dest.text,il.reg(2,source.text)))
    else:
        il.append(il.set_reg(2,dest.text,il.const(2,source.value)))
    return disas[1]

def pr(data,addr,il,disas):
    tokens = disas[0]
    dest = tokens[2]
    il.append(il.intrinsic([],'print',[il.reg(2,dest.text)]))
    return disas[1]

def read1(data,addr,il,disas):
    tokens = disas[0]
    dest = tokens[2]
    il.append(il.intrinsic([],'read',[il.reg(2,dest.text)]))
    return disas[1]

def jmp(data,addr,il,disas):
    tokens = disas[0]
    dest = tokens[-1].value
    tmp = il.get_label_for_address(Architecture['vmmod'],dest)
    # il.append(il.goto(tmp))
    il.append(il.jump(il.const_pointer(2,dest)))
    return disas[1]

def call(data,addr,il,disas):
    tokens = disas[0]
    dest = tokens[-1].value
    tmp = il.get_label_for_address(Architecture['vmmod'],dest)
    # il.append(il.goto(tmp))
    il.append(il.call(il.const_pointer(2,dest)))
    return disas[1]

def f_exit(data,addr,il,disas):
    il.append(il.intrinsic([],'exit',[]))
    il.append(il.no_ret())
    return 1

def add(data,addr,il,disas):
    tokens = disas[0]
    dest = tokens[2]
    source = tokens[4]
    if source.type == InstructionTextTokenType.RegisterToken:
        expr = il.add(2,il.reg(2,dest.text),il.reg(2,source.text))
    else:
        expr = il.add(2,il.reg(2,dest.text),il.const(2,source.value))
    il.append(il.set_reg(2,dest.text,expr))
    return disas[1]   

def f_and(data,addr,il,disas):
    tokens = disas[0]
    dest = tokens[2]
    source = tokens[4]
    if source.type == InstructionTextTokenType.RegisterToken:
        expr = il.and_expr(2,il.reg(2,dest.text),il.reg(2,source.text))
    else:
        expr = il.and_expr(2,il.reg(2,dest.text),il.const(2,source.value))
    il.append(il.set_reg(2,dest.text,expr))
    return disas[1]   

def sub(data,addr,il,disas):
    tokens = disas[0]
    dest = tokens[2]
    source = tokens[4]
    if source.type == InstructionTextTokenType.RegisterToken:
        sub_expr = il.sub(2,il.reg(2,dest.text),il.reg(2,source.text))
    else:
        sub_expr = il.sub(2,il.reg(2,dest.text),il.const(2,source.value))
    il.append(il.set_reg(2,dest.text,sub_expr))
    return disas[1]   

def xor(data,addr,il,disas):
    tokens = disas[0]
    dest = tokens[2]
    source = tokens[4]
    if source.type == InstructionTextTokenType.RegisterToken:
        expr = il.xor_expr(2,il.reg(2,dest.text),il.reg(2,source.text))
    else:
        expr = il.xor_expr(2,il.reg(2,dest.text),il.const(2,source.value))
    il.append(il.set_reg(2,dest.text,expr))
    return disas[1]  

def shl(data,addr,il,disas):
    tokens = disas[0]
    dest = tokens[2]
    source = tokens[4]
    if source.type == InstructionTextTokenType.RegisterToken:
        expr = il.shift_left(2,il.reg(2,dest.text),il.reg(2,source.text))
    else:
        expr = il.shift_left(2,il.reg(2,dest.text),il.const(2,source.value))
    il.append(il.set_reg(2,dest.text,expr))
    return disas[1]   

def shr(data,addr,il,disas):
    tokens = disas[0]
    dest = tokens[2]
    source = tokens[4]
    if source.type == InstructionTextTokenType.RegisterToken:
        expr = il.arith_shift_right(2,il.reg(2,dest.text),il.reg(2,source.text))
    else:
        expr = il.arith_shift_right(2,il.reg(2,dest.text),il.const(2,source.value))
    il.append(il.set_reg(2,dest.text,expr))
    return disas[1]    

def jz(data,addr,il,disas):
    tokens = disas[0]
    reg = tokens[2].text
    dest = tokens[-1].value
    il_reg = il.reg(2,reg)
    cond = il.compare_equal(2,il_reg,il.const(2,0))
    t = LowLevelILLabel()
    f = LowLevelILLabel()
    il.append(il.if_expr(cond,t,f))
    il.mark_label(t)
    il.append(il.jump(il.const_pointer(2,dest)))
    il.mark_label(f)
    return disas[1]

def store(data,addr,il,disas):
    tokens = disas[0]
    dest_reg = tokens[2].text
    il_dest_reg = il.reg(2,dest_reg)
    off_addr = tokens[4].value + addr
    source = tokens[6]
    if source.type == InstructionTextTokenType.RegisterToken:
        addr = il.add(2,il.const(2,off_addr),il.reg(2,source.text))

    else:
        off = source.value
        addr = il.add(2,il.const(2,off_addr),il.const(2,off))
    # il.append(il.store(2,il.const_pointer(2,addr),il_dest_reg))
    il.append(il.unimplemented())
    return disas[1]

def f_not(data,addr,il,disas):
    tokens = disas[0]
    dest_reg = tokens[2].text
    il_dest_reg = il.reg(2,dest_reg)
    il.append(il.not_expr(2,il_dest_reg))
    return disas[1]

def ld(data,addr,il,disas):
    tokens = disas[0]
    dest_reg = tokens[2].text
    il_dest_reg = il.reg(2,dest_reg)
    off_addr = tokens[4].value #+ addr
    source = tokens[6]
    if source.type == InstructionTextTokenType.RegisterToken:
        addr = il.add(2,il.reg(2,source.text),il.const(2,off_addr))
    else:
        off = source.value
        addr = il.add(2,il.const(2,off_addr),il.const(2,off))
    # addr = il.add(2,il.const(2,addr),addr)
    il.append(il.set_reg(2,dest_reg,il.load(1,il.const_pointer(2,off_addr))))
    # il.append(il.unimplemented())
    return disas[1]

def remap(data,addr,il,disas):
    dest = data[1]
    source = data[2]
    il.append(il.intrinsic([],'remap',[il.const(2,dest),il.const(2,source)]))
    return disas[1]

def ret(data,addr,il,disas):
    il.append(il.ret(il.pop(2)))
    return 1

class VMMODlifter:
    opcodes = {
        0 : mov,
        1 : pr,
        2 : call,
        3 : ret,
        4 : remap,
        5 : add,
        6 : f_and,
        7 : xor,
        8 : shl,
        9 : shr,
        0xa : f_not,
        0xb : jz,
        0xc : jmp,
        0xd : sub,
        0xe : store,
        0xf : ld,
        0x12 : read1,
        0xff : f_exit
    }