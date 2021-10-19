class CameraCutscene:

    def __init__(self):

        self.pivots = dict({"pivot_1": 0, "pivot_2": 0, "pivot_3": 0, "pivot_4": 0})
        self.rotations = dict({"X_start": 0, "X_end": 0, "Z_start": 0, "Z_end": 0})
        self.positions = dict({"Y_start": 0, "Y_end": 0, "Z_start": 0, "Z_end": 0})
        self.unknowns = dict({"unknown_block_10": 0, "unknown_block_13": 0})
        self.zoom_in = 0.0
        self.camera_speed = 0.0
        self.modified = False
