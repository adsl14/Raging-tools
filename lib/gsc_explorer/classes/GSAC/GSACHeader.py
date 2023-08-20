from lib.gsc_explorer.classes.GSAC.GSACData import GsacData


class GsacHeader:

    def __init__(self):
        self.unk0x04 = b''
        self.id = 0
        self.data = GsacData()
