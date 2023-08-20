from lib.gsc_explorer.classes.GSHD.GSHDData import GshdData


class GshdHeader:

    def __init__(self):
        self.unk0x04 = b''
        self.unk0x0c = b''
        self.data = GshdData()
