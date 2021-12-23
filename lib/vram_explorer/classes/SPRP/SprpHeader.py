class SprpHeader:

    def __init__(self):
        self.data_tag = 0xff
        self.entry_count = 0
        self.entry_info_size = 0
        self.string_table_size = 0
        self.data_info_size = 0
        self.vram_data_size = 0
