from lib.gsc_explorer.classes.GSAC.GSACData import GsacData


class GsacHeader:

    def __init__(self):
        self.unk0x04 = b'\x10\x00\x00\x00'
        self.id = b''
        self.data = GsacData()
