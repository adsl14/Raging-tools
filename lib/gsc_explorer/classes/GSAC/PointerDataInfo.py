class PointerDataInfo:

    def __init__(self):
        self.type = b''
        self.number_of_pointers = 0
        self.secundary_number_of_pointers = 0
        self.unk0x04 = b''
        self.pointers_data = []  # PointerData()
