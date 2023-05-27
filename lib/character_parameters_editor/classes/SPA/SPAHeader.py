class SPAHeader:

    def __init__(self):
        self.unk0x00 = b''
        self.name = ""
        self.extension = ""
        self.unk0x08 = b''
        self.frame_count = 0.0
        self.bone_count = 0
        self.bone_nodes_offset = 0
        self.scene_nodes_count = 0
        self.scene_nodes_offset = 0
        self.camera_count = 0
        self.camera_offset = 0
        self.unk0x28 = b''
        self.unk0x2c = b''
