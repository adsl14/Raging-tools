class Slot:

    def __init__(self):

        # Position in the file cs_chip for a slot
        self.position_cs_chip = -1
        # Position in the file cs_form for a slot
        self.position_cs_form = -1
        # Number of transformations that has the slot
        self.num_transformations = -1
        # ID of the character
        self.chara_id = 101
        # ID for each transformation slot (101 is Noise image)

        self.transformations_id = [101, 101, 101, 101, 101]
        # Reference to the qlabel object in the tool
        self.qlabel_object = None

    def reset(self):

        # Position in the file cs_chip for a slot
        self.position_cs_chip = -1
        # Position in the file cs_form for a slot
        self.position_cs_form = -1
        # Number of transformations that has the slot
        self.num_transformations = -1
        # ID of the character
        self.chara_id = 101
        # ID for each transformation slot (101 is Noise image)
        for i in range(0, len(self.transformations_id)):
            self.transformations_id[i] = 101
