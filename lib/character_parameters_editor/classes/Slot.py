class Slot:

    def __init__(self):

        # Position in the file cs_form for a slot
        self.position_cs_form = -1
        # Number of transformations that has the slot
        self.num_transformations = -1
        # ID of the character
        self.chara_id = 255
        # ID for each transformation slot
        self.transformations_id = [255, 255, 255, 255, 255]
        # Reference to the qlabel object in the tool
        self.qlabel_object = None
