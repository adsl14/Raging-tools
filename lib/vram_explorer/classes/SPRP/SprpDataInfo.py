class SprpDataInfo:

    def __init__(self):
        self.name_offset = 0
        self.data_offset = 0
        self.data_size = 0
        self.child_count = 0
        self.child_offset = 0
        # Extra info
        self.name = ""
        self.extension = ""
        self.name_size = 0
        self.new_name_offset = 0
        self.name_offset_calculated = False
        # SprpDataInfo
        self.child_info = []
        # Could be Tx2dInfo, MtrlInfo
        self.data = None
