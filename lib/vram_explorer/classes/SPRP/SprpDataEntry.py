from lib.vram_explorer.classes.SPRP.SprpDataInfo import SprpDataInfo


class SprpDataEntry:

    def __init__(self):
        self.data_type = 0xff
        self.index = 0
        # Check if is a brand new entry
        self.new_entry = False
        # SprpDataInfo
        self.data_info = SprpDataInfo()
