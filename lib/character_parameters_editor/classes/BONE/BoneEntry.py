class BoneEntry:

    def __init__(self):
        self.name = ""
        self.unk0x04 = b''
        self.translation_block_count = 0
        self.rotation_block_count = 0
        self.unknown_block_count = 0
        self.translation_frame_offset = 0
        self.rotation_frame_offset = 0
        self.unknown_frame_offset = 0
        self.translation_float_offset = 0
        self.rotation_float_offset = 0
        self.unknown_float_offset = 0
        self.unk0x2c = b''
        self.translation_frame_data = []
        self.translation_float_data = []
        self.rot_frame_data = []
        self.rot_float_data = []
        self.unknown_frame_data = []
        self.unknown_float_data = []
