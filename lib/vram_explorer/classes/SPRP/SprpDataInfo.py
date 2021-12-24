class SprpDataInfo:

    def __init__(self):
        self.name = ""
        self.extension = ""
        self.name_offset = 0
        self.data_offset = 0
        self.data_size = 0
        self.child_count = 0
        self.child_offset = 0
        # Could be Tx2dInfo, MtrlInfo, IoramInfo
        self.data = None
