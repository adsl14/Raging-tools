# Read the file cs_form searching the ID from cs_chip
from lib.character_parameters_editor.REV import REV


def search_id(file_cs_form, slot_character):

    data = file_cs_form.read(REV.size_between_character_cs_form)
    while data:

        # Get the position
        position = file_cs_form.tell() - REV.size_between_character_cs_form

        # Get the ID of the character for the roster
        chara_id_cs_form = data[15]

        # If are equal, we found the ID from cs_chip in cs_form
        if slot_character.chara_id == chara_id_cs_form:

            # Save the position
            slot_character.position_cs_form = position

            # Get number transformations
            slot_character.num_transformations = data[11]

            # Get the transformations ID
            position = 19
            for i in range(0, 5):

                # Change from 255 in file to 101 in memory
                transformation_id = data[position]
                if transformation_id == 255:
                    transformation_id = 101

                slot_character.transformations_id[i] = transformation_id
                position = position + 4

            # Stop the searching
            break

        # Read the next 36 bytes
        data = file_cs_form.read(REV.size_between_character_cs_form)

    # Move the pointer of the file to the beginning
    file_cs_form.seek(0)


# Calculate the number of transformations when the user add or remove a transformation
def get_num_transformations(slot_chara):

    # If we find a transformation ID that is not 101 (not empty slot), we return the position where we found a
    # transformation slot that is actually a character
    for i in range(REV.num_slots_transformations - 1, -1, -1):
        if slot_chara.transformations_id[i] != 101:
            return i + 1

    return 0
