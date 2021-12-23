class Tx2dInfo:

  def __init__(self):
    self.data_offset = 0
    self.data_offset_old = 0
    self.data_size = 0
    self.data_size_old = 0
    self.width = 0
    self.height = 0
    self.mip_maps = 0
    self.dxt_encoding = 0

    # TX2D_VRAM
    self.tx2d_vram = None
