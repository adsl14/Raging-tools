class MtrlLayer:

  def __init__(self):
    # self.source_name_offset = 0 -> Won't store the name offset. Instead, we will store the tx2d_data_entry that
    # has inside the name offset
    self.layer_name_offset = 0
    # Extra info
    self.layer_name = ""
    self.tx2d_data_entry = None
