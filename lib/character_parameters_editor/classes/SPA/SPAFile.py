from lib.character_parameters_editor.classes.SPA.SPAHeader import SPAHeader


class SPAFile:

    def __init__(self):
        self.spa_header = SPAHeader()
        self.bone_entries = dict({})

        # Extra info
        self.path = ""
        self.size = 0
        self.modified = False
