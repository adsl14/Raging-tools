class VBufInfo:

    def __init__(self):
        self.unk0x00 = b''
        self.unk0x04 = b''
        self.data_offset = 0
        self.data_size = 0
        self.vertex_count = 0
        self.index_count = 0  # UT var
        self.unk0x14 = b''
        self.unk0x16 = b''
        self.decl_count_0 = 0
        self.decl_count_1 = 0
        self.decl_offset = 0
        self.index_offset = 0  # UT var
        # VertexDecl()
        self.vertex_decl = []
