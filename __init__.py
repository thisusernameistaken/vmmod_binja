from .arch import VMMODarch
from .view import VMMODview
from binaryninja import CallingConvention, Architecture

class VMMODcc(CallingConvention):
    name = "vmmod_cc"
    int_arg_regs = ["r10","r11","r12"]


VMMODarch.register()
Architecture['vmmod'].register_calling_convention(VMMODcc(Architecture['vmmod'],'default'))
VMMODview.register()