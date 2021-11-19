
class CPEVRE:

    roster_editor_first_activation = True
    cs_chip_path = ""
    cs_form_path = ""
    # Index of the slot selected in the main panel
    slot_chara_selected = -1
    # Index of the transformation slot selected in the main panel
    slot_trans_selected = -1
    # Boolean that will tell if the user is editing a character slot or trans slot
    selecting_character = True
    # Size of trans slots
    num_slots_transformations = 5
    # Array of slots objects for the transformations
    slots_transformations = []
    # Size character slots
    num_slots_characters = 72
    # Array of slots objects for the characters
    slots_characters = []
    # slots that are already edited
    slots_edited = []
    # Size between characters in cs_form
    size_between_character_cs_form = 36
