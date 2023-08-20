from lib.gsc_explorer.classes.GSCD.GSCDHeader import GscdHeader
from lib.gsc_explorer.classes.GSDT.GSDTHeader import GsdtHeader
from lib.gsc_explorer.classes.GSHD.GSHDHeader import GshdHeader


class GscfHeader:

    def __init__(self):
        self.unk0x04 = b''
        self.unk0x0c = b''
        self.gshd_header = GshdHeader()
        self.gscd_header = GscdHeader()
        self.gsdt_header = GsdtHeader()
