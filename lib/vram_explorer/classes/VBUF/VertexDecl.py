class VertexDecl:

    def __init__(self):
        self.unk0x00 = b''
        self.resource_name_offset = 0
        self.vertex_usage = b''
        self.index = 0
        self.vertex_format = b''
        self.stride = 0
        self.offset = 0
        # Extra info
        self.resource_name = ""
