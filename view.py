from binaryninja import BinaryView, Architecture, SegmentFlag, SectionSemantics

class VMMODview(BinaryView):
    name = "vmmod"
    long_name = "vmmod binary view"

    def __init__(self,data):
        BinaryView.__init__(self,file_metadata=data.file,parent_view=data)
        self.raw = data

    @classmethod
    def is_valid_for_data(cls,data):
        return "out.bin" in data.file.original_filename

    def init(self):
        self.platform = Architecture['vmmod'].standalone_platform
        self.arch = Architecture['vmmod']

        self.entry_addr = 0
        self.add_auto_segment(0,len(self.raw),0,len(self.raw),SegmentFlag.SegmentContainsCode)
        self.add_auto_section(".code",0,len(self.raw),SectionSemantics.ReadOnlyCodeSectionSemantics)

        self.add_entry_point(self.entry_addr)
        self.add_function(self.entry_addr)

        return True