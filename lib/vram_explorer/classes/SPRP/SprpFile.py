from lib.vram_explorer.classes.SPRP.SprpHeader import SprpHeader


class SprpFile:

    def __init__(self):
        self.sprp_header = SprpHeader()
        self.entry_info_base = 0
        self.string_table_base = 0
        self.data_info_base = 0
        self.data_block_base = 0
        self.file_size = 0
        # SprpTypeEntry
        self.type_entry = {}
