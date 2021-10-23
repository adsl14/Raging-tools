class CameraCutscene:

    def __init__(self):

        self.pivots = dict({"pivot_1": 0, "pivot_2": 0, "pivot_3": 0, "pivot_4": 0})
        self.rotations = dict({"Y_start": 0, "Y_end": 0, "Z_start": 0, "Z_end": 0})
        self.positions = dict({"Y_start": 0.0, "Y_end": 0.0, "Z_start": 0.0, "Z_end": 0.0})
        self.zooms = dict({"Zoom_start": 0, "Zoom_end": 0})
        self.camera_speed = 0.0
        self.unknown_block_13 = 0.0
        self.modified = False
