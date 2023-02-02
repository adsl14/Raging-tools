from PyQt5.QtGui import QPixmap
from lib.character_parameters_editor.CPEV import CPEV
from lib.character_parameters_editor.IPV import IPV
from lib.packages import struct, os


def read_transformation_effect(main_window, animation):

    # Get each four bytes
    for i in range(0, animation.size, 4):
        data = animation.data[i:i+4]

        # If we found the bytes that identify if is a proper trans effect file, we store where is located
        # the background color
        if data == IPV.trans_effect_identification_file:
            # Enable combo box
            main_window.background_color_trans_value.setEnabled(True)
            # Store the data
            IPV.trans_effect_position_byte = i-1
            main_window.background_color_trans_value.setCurrentIndex(main_window.background_color_trans_value.findData
                                                                     (animation.data[i-1]))
            return

    # If we didn't find the bytes that identify if is a proper trans effect file, we disable the combo box
    main_window.background_color_trans_value.setEnabled(False)


def store_camera_cutscene_from_file(camera_cutscene, file):

    # Get the pivots
    camera_cutscene.pivots["pivot_1"] = int.from_bytes(file.read(1), byteorder='big')
    camera_cutscene.pivots["pivot_2"] = int.from_bytes(file.read(1), byteorder='big')
    camera_cutscene.pivots["pivot_3"] = int.from_bytes(file.read(1), byteorder='big')
    camera_cutscene.pivots["pivot_4"] = int.from_bytes(file.read(1), byteorder='big')

    # Rotations Z
    camera_cutscene.rotations["Z_start"] = struct.unpack('>f', file.read(4))[0]
    camera_cutscene.rotations["Z_end"] = camera_cutscene.rotations["Z_start"] + \
        struct.unpack('>f', file.read(4))[0]

    # Translations Y
    camera_cutscene.positions["Y_start"] = struct.unpack('>f', file.read(4))[0]
    camera_cutscene.positions["Y_end"] = camera_cutscene.positions["Y_start"] + \
        struct.unpack('>f', file.read(4))[0]

    # Rotations Y
    camera_cutscene.rotations["Y_start"] = struct.unpack('>f', file.read(4))[0]
    camera_cutscene.rotations["Y_end"] = camera_cutscene.rotations["Y_start"] + \
        struct.unpack('>f', file.read(4))[0]

    # Zoom
    camera_cutscene.zooms["Zoom_start"] = struct.unpack('>f', file.read(4))[0]
    camera_cutscene.zooms["Zoom_end"] = camera_cutscene.zooms["Zoom_start"] + \
        struct.unpack('>f', file.read(4))[0]

    # Translations Z
    camera_cutscene.positions["Z_start"] = struct.unpack('>f', file.read(4))[0]
    camera_cutscene.positions["Z_end"] = camera_cutscene.positions["Z_start"] + \
        struct.unpack('>f', file.read(4))[0]

    # Camera speed (float values)
    camera_cutscene.camera_speed = struct.unpack('>f', file.read(4))[0]

    # Unknown value block 13
    camera_cutscene.unknown_block_13 = file.read(4)


def write_camera_cutscene_to_file(camera_cutscene, file):

    # Write the pivots
    file.write(camera_cutscene.pivots["pivot_1"].to_bytes(1, byteorder="big"))
    file.write(camera_cutscene.pivots["pivot_2"].to_bytes(1, byteorder="big"))
    file.write(camera_cutscene.pivots["pivot_3"].to_bytes(1, byteorder="big"))
    file.write(camera_cutscene.pivots["pivot_4"].to_bytes(1, byteorder="big"))

    # Rotations Z
    file.write(struct.pack('>f', camera_cutscene.rotations["Z_start"]))
    file.write(struct.pack('>f', camera_cutscene.rotations["Z_end"] - camera_cutscene.rotations["Z_start"]))

    # Translations Y
    file.write(struct.pack('>f', camera_cutscene.positions["Y_start"]))
    file.write(struct.pack('>f', camera_cutscene.positions["Y_end"] - camera_cutscene.positions["Y_start"]))

    # Rotations Y
    file.write(struct.pack('>f', camera_cutscene.rotations["Y_start"]))
    file.write(struct.pack('>f', camera_cutscene.rotations["Y_end"] - camera_cutscene.rotations["Y_start"]))

    # Zoom
    file.write(struct.pack('>f', camera_cutscene.zooms["Zoom_start"]))
    file.write(struct.pack('>f', camera_cutscene.zooms["Zoom_end"] - camera_cutscene.zooms["Zoom_start"]))

    # Translations Z
    file.write(struct.pack('>f', camera_cutscene.positions["Z_start"]))
    file.write(struct.pack('>f', camera_cutscene.positions["Z_end"] - camera_cutscene.positions["Z_start"]))

    # Camera speed (float values)
    file.write(struct.pack('>f', camera_cutscene.camera_speed))

    # Unknown value block 13
    file.write(camera_cutscene.unknown_block_13)


def change_camera_cutscene_values(main_window, camera_cutscene):

    # Avoid combobox change the values
    CPEV.disable_logic_events_combobox = True

    # Pivots
    main_window.pivot_value.setValue(camera_cutscene.pivots["pivot_1"])
    main_window.pivot_value_2.setValue(camera_cutscene.pivots["pivot_2"])
    main_window.pivot_value_3.setValue(camera_cutscene.pivots["pivot_3"])
    main_window.pivot_value_4.setValue(camera_cutscene.pivots["pivot_4"])

    # Translations
    main_window.translation_y_start_value.setValue(camera_cutscene.positions["Y_start"])
    main_window.translation_y_end_value.setValue(camera_cutscene.positions["Y_end"])
    main_window.translation_z_start_value.setValue(camera_cutscene.positions["Z_start"])
    main_window.translation_z_end_value.setValue(camera_cutscene.positions["Z_end"])

    # Rotations
    main_window.rotation_y_start_value.setValue(camera_cutscene.rotations["Y_start"])
    main_window.rotation_y_end_value.setValue(camera_cutscene.rotations["Y_end"])
    main_window.rotation_z_start_value.setValue(camera_cutscene.rotations["Z_start"])
    main_window.rotation_z_end_value.setValue(camera_cutscene.rotations["Z_end"])

    # Zoom
    main_window.zoom_start_value.setValue(camera_cutscene.zooms["Zoom_start"])
    main_window.zoom_end_value.setValue(camera_cutscene.zooms["Zoom_end"])

    # Speed
    main_window.speed_camera_value.setValue(camera_cutscene.camera_speed)

    # Enable combobox change the values
    CPEV.disable_logic_events_combobox = False


def change_animation_bones_section(main_window, animation_array):

    # Avoid combobox change the values
    CPEV.disable_logic_events_combobox = True

    # Get the first bone entry
    spa_file = animation_array[0][0]

    # If there is data in the actual spa_file, we'll show it in the tool
    if spa_file.size > 0:

        # Enable the bones section entirely
        if not main_window.bones_frame_section.isEnabled():
            main_window.bones_frame_section.setEnabled(True)

        # Layer
        main_window.animation_spas_layer_value.clear()
        for i in range(0, len(animation_array)):
            main_window.animation_spas_layer_value.addItem(str(i), i)
        main_window.animation_spas_layer_value.setCurrentIndex(0)

        change_animation_layer_spas(main_window, spa_file)

    else:
        # Disable the bones section entirely
        if main_window.bones_frame_section.isEnabled():
            main_window.bones_frame_section.setEnabled(False)

    # Enable combobox change the values
    CPEV.disable_logic_events_combobox = False


def change_animation_layer_spas(main_window, spa_file):

    # Avoid combobox change the values
    CPEV.disable_logic_events_combobox = True

    if spa_file.size > 0:

        if not main_window.animation_bone_value.isEnabled():
            main_window.animation_bone_value.setEnabled(True)

        bone_entry = list(spa_file.bone_entries.values())[0]

        # Bones
        main_window.animation_bone_value.clear()
        for bone_name in spa_file.bone_entries:
            main_window.animation_bone_value.addItem(bone_name)
        main_window.animation_bone_value.setCurrentIndex(0)

        change_animation_bone(main_window, bone_entry, bone_entry.translation_block_count, bone_entry.rotation_block_count, bone_entry.unknown_block_count)
    else:
        if main_window.animation_bone_value.isEnabled():
            main_window.animation_bone_value.setEnabled(False)

        change_animation_bone(main_window, None, 0, 0, 0)

    # Enable combobox change the values
    CPEV.disable_logic_events_combobox = False


def change_animation_bone(main_window, bone_entry, translation_block_count, rotation_block_count, unknown_block_count):

    # Avoid combobox change the values
    CPEV.disable_logic_events_combobox = True

    # Blocks
    # Translations
    if translation_block_count > 0:

        main_window.animation_bone_translation_block_value.setEnabled(True)
        main_window.animation_bone_translation_X_value.setEnabled(True)
        main_window.animation_bone_translation_Y_value.setEnabled(True)
        main_window.animation_bone_translation_Z_value.setEnabled(True)
        main_window.animation_bone_translation_W_value.setEnabled(True)

        main_window.animation_bone_translation_block_value.clear()
        for i in range(0, translation_block_count):
            main_window.animation_bone_translation_block_value.addItem(str(i), i)
        main_window.animation_bone_translation_block_value.setCurrentIndex(0)
        change_animation_bone_translation_block(main_window, bone_entry.translation_float_data[main_window.animation_bone_translation_block_value.currentData()])

    else:
        main_window.animation_bone_translation_block_value.setEnabled(False)
        main_window.animation_bone_translation_X_value.setEnabled(False)
        main_window.animation_bone_translation_Y_value.setEnabled(False)
        main_window.animation_bone_translation_Z_value.setEnabled(False)
        main_window.animation_bone_translation_W_value.setEnabled(False)

    # Rotations
    if rotation_block_count > 0:

        main_window.animation_bone_rotation_block_value.setEnabled(True)
        main_window.animation_bone_rotation_X_value.setEnabled(True)
        main_window.animation_bone_rotation_Y_value.setEnabled(True)
        main_window.animation_bone_rotation_Z_value.setEnabled(True)

        main_window.animation_bone_rotation_block_value.clear()
        for i in range(0, rotation_block_count):
            main_window.animation_bone_rotation_block_value.addItem(str(i), i)
        main_window.animation_bone_rotation_block_value.setCurrentIndex(0)
        # Rotations
        change_animation_bone_rotations_block(main_window, bone_entry.rot_float_data[main_window.animation_bone_rotation_block_value.currentData()])

    else:
        main_window.animation_bone_rotation_block_value.setEnabled(False)
        main_window.animation_bone_rotation_X_value.setEnabled(False)
        main_window.animation_bone_rotation_Y_value.setEnabled(False)
        main_window.animation_bone_rotation_Z_value.setEnabled(False)

    # Unknowns
    if unknown_block_count > 0:

        main_window.animation_bone_unknown_block_value.setEnabled(True)
        main_window.animation_bone_unknown_X_value.setEnabled(True)
        main_window.animation_bone_unknown_Y_value.setEnabled(True)
        main_window.animation_bone_unknown_Z_value.setEnabled(True)
        main_window.animation_bone_unknown_W_value.setEnabled(True)

        main_window.animation_bone_unknown_block_value.clear()
        for i in range(0, unknown_block_count):
            main_window.animation_bone_unknown_block_value.addItem(str(i), i)
        main_window.animation_bone_unknown_block_value.setCurrentIndex(0)
        change_animation_bone_unknown_block(main_window, bone_entry.unknown_float_data[main_window.animation_bone_unknown_block_value.currentData()])

    else:
        main_window.animation_bone_unknown_block_value.setEnabled(False)
        main_window.animation_bone_unknown_X_value.setEnabled(False)
        main_window.animation_bone_unknown_Y_value.setEnabled(False)
        main_window.animation_bone_unknown_Z_value.setEnabled(False)
        main_window.animation_bone_unknown_W_value.setEnabled(False)

    # Enable combobox change the values
    CPEV.disable_logic_events_combobox = False


def change_animation_bone_translation_block(main_window, translations_float_data):

    # Translations
    main_window.animation_bone_translation_X_value.setValue(translations_float_data["x"])
    main_window.animation_bone_translation_Y_value.setValue(translations_float_data["y"])
    main_window.animation_bone_translation_Z_value.setValue(translations_float_data["z"])
    main_window.animation_bone_translation_W_value.setValue(translations_float_data["w"])


def change_animation_bone_rotations_block(main_window, rotations_float_data):

    # Rotations
    main_window.animation_bone_rotation_X_value.setValue(rotations_float_data["x"])
    main_window.animation_bone_rotation_Y_value.setValue(rotations_float_data["y"])
    main_window.animation_bone_rotation_Z_value.setValue(rotations_float_data["z"])


def change_animation_bone_unknown_block(main_window, unknown_float_data):

    # Unknown values. Needs more reseach
    main_window.animation_bone_unknown_X_value.setValue(unknown_float_data["x"])
    main_window.animation_bone_unknown_Y_value.setValue(unknown_float_data["y"])
    main_window.animation_bone_unknown_Z_value.setValue(unknown_float_data["z"])
    main_window.animation_bone_unknown_W_value.setValue(unknown_float_data["w"])


def get_rotation(v):

    return int(((v + 90) / 90) * 0x7ffff)


def store_blast_values_from_file(blast, file):

    # Read all the data
    # Read unk data
    blast.unk0x00 = file.read(2)
    # Glow activation
    blast.glow = int.from_bytes(file.read(1), byteorder='big')
    # Number of hits
    blast.number_of_hits = int.from_bytes(file.read(1), byteorder='big')
    # Read unk data
    blast.unk0x04 = file.read(8)
    # partner model
    blast.partner_id = int.from_bytes(file.read(1), byteorder='big')
    # Read unk data
    blast.unk0x0D = file.read(3)
    # Reach attack
    blast.reach_attack = struct.unpack('>f', file.read(4))[0]
    # Read unk data
    blast.unk0x14 = file.read(4)
    # attack damage
    blast.attack_damage = int.from_bytes(file.read(2), byteorder='big')
    # Read unk data
    blast.unk0x1A = file.read(1)
    # cost attack
    blast.cost_attack = int.from_bytes(file.read(1), byteorder='big')
    # Read unk data
    blast.unk0x1C = file.read(4)
    # Power ups
    blast.power_ups["Melee"] = int.from_bytes(file.read(1), byteorder='big')
    blast.power_ups["Defense"] = int.from_bytes(file.read(1), byteorder='big')
    blast.unk0x22 = file.read(1)
    blast.power_ups["Super Attack"] = int.from_bytes(file.read(1), byteorder='big')
    blast.unk0x24 = file.read(5)
    blast.power_ups["Ki"] = int.from_bytes(file.read(1), byteorder='big')
    # Read unk data
    blast.unk0x2A = file.read(8)
    # Skill stackeable
    blast.skill_stackable = int.from_bytes(file.read(1), byteorder='big')
    # Read unk data
    blast.unk0x33 = file.read(21)
    # Cameras
    for j in range(0, 4):
        blast.camera[j] = int.from_bytes(file.read(1), byteorder='big')
    # Read unk data
    blast.unk0x4C = file.read(2)
    # Activation skill
    blast.activation_skill = int.from_bytes(file.read(1), byteorder='big')
    # Chargeable or boost attack
    blast.chargeable_boost = int.from_bytes(file.read(1), byteorder='big')
    # Read unk data
    blast.unk0x50 = file.read(4)
    # Speed attack
    blast.speed_of_attack = struct.unpack('>f', file.read(4))[0]
    # Read unk data
    blast.unk0x58 = file.read(4)
    # Size attack
    blast.size_of_attack = struct.unpack('>f', file.read(4))[0]
    # Read unk data
    blast.unk0x60 = file.read(4)


def write_blast_values_to_file(blast, file):

    # Write all the data
    # Write unk data
    file.write(blast.unk0x00)
    # Glow activation
    file.write(blast.glow.to_bytes(1, 'big'))
    # Number of hits
    file.write(blast.number_of_hits.to_bytes(1, 'big'))
    # Write unk data
    file.write(blast.unk0x04)
    # partner model
    file.write(blast.partner_id.to_bytes(1, 'big'))
    # Write unk data
    file.write(blast.unk0x0D)
    # Reach attack
    file.write(struct.pack('>f', blast.reach_attack))
    # Write unk data
    file.write(blast.unk0x14)
    # attack damage
    file.write(blast.attack_damage.to_bytes(2, 'big'))
    # Write unk data
    file.write(blast.unk0x1A)
    # cost attack
    file.write(blast.cost_attack.to_bytes(1, 'big'))
    # Write unk data
    file.write(blast.unk0x1C)
    # Power ups
    file.write(blast.power_ups["Melee"].to_bytes(1, 'big'))
    file.write(blast.power_ups["Defense"].to_bytes(1, 'big'))
    # Write unk data
    file.write(blast.unk0x22)
    file.write(blast.power_ups["Super Attack"].to_bytes(1, 'big'))
    file.write(blast.unk0x24)
    file.write(blast.power_ups["Ki"].to_bytes(1, 'big'))
    # Write unk data
    file.write(blast.unk0x2A)
    # Skill stackeable
    file.write(blast.skill_stackable.to_bytes(1, 'big'))
    # Write unk data
    file.write(blast.unk0x33)
    # Cameras
    for j in range(0, 4):
        file.write(blast.camera[j].to_bytes(1, 'big'))
    # Write unk data
    file.write(blast.unk0x4C)
    # Activation skill
    file.write(blast.activation_skill.to_bytes(1, 'big'))
    # Chargeable or boost attack
    file.write(blast.chargeable_boost.to_bytes(1, 'big'))
    # Write unk data
    file.write(blast.unk0x50)
    # Speed attack
    file.write(struct.pack('>f', blast.speed_of_attack))
    # Write unk data
    file.write(blast.unk0x58)
    # Size attack
    file.write(struct.pack('>f', blast.size_of_attack))
    # Write unk data
    file.write(blast.unk0x60)


def change_blast_values(main_window, blast_parameter):

    # Avoid combobox change the values
    CPEV.disable_logic_events_combobox = True

    # Glow
    main_window.glow_activation_value.setCurrentIndex(main_window.glow_activation_value.findData(blast_parameter.glow))
    '''print("Glow: " + str(blast_parameter.glow))'''

    # Number of hits
    main_window.number_of_hits_value.setValue(blast_parameter.number_of_hits)

    # Partner
    main_window.partner_character_value.setPixmap(QPixmap(os.path.join(CPEV.path_small_four_slot_images, "sc_chara_s_" +
                                                                       str(blast_parameter.partner_id).zfill(3) + ".png")))

    # Reach attack
    main_window.reach_attack_value.setValue(blast_parameter.reach_attack)

    # Damage
    main_window.blast_attack_damage_value.setValue(blast_parameter.attack_damage)

    # Cost
    main_window.cost_blast_attack_value.setValue(blast_parameter.cost_attack)

    # Powerups
    main_window.melee_power_up_value.setCurrentIndex(main_window.melee_power_up_value.findData(blast_parameter.power_ups["Melee"]))
    main_window.defense_power_up_value.setCurrentIndex(main_window.defense_power_up_value.findData(blast_parameter.power_ups["Defense"]))
    main_window.super_attack_power_up_value.setCurrentIndex(main_window.super_attack_power_up_value.findData(blast_parameter.power_ups["Super Attack"]
                                                                                                             ))
    main_window.ki_power_up_value.setCurrentIndex(main_window.ki_power_up_value.findData(blast_parameter.power_ups["Ki"]))
    '''print("Melee: " + str(blast_parameter.power_ups["Melee"]))
    print("Defense: " + str(blast_parameter.power_ups["Defense"]))
    print("Super Attack: " + str(blast_parameter.power_ups["Super Attack"]))
    print("Ki: " + str(blast_parameter.power_ups["Ki"]))'''

    # Stackable
    main_window.stackable_skill_value.setCurrentIndex(main_window.stackable_skill_value.findData(blast_parameter.skill_stackable))
    '''print("skill_stackable: " + str(blast_parameter.skill_stackable))'''

    # Camera
    main_window.camera_blast_value_0.setValue(blast_parameter.camera[0])
    main_window.camera_blast_value_1.setValue(blast_parameter.camera[1])
    main_window.camera_blast_value_2.setValue(blast_parameter.camera[2])
    main_window.camera_blast_value_3.setValue(blast_parameter.camera[3])

    # Effect
    main_window.effect_attack_value.setCurrentIndex(main_window.effect_attack_value.findData(blast_parameter.activation_skill))
    '''print("activation_skill: " + str(blast_parameter.activation_skill))'''

    # Boost
    main_window.chargeable_value.setCurrentIndex(main_window.chargeable_value.findData(blast_parameter.chargeable_boost))
    '''print("chargeable_boost: " + str(blast_parameter.chargeable_boost))'''

    # Speed
    main_window.speed_attack_value.setValue(blast_parameter.speed_of_attack)

    # Size
    main_window.size_attack_value.setValue(blast_parameter.size_of_attack)

    # Enable combobox change the values
    CPEV.disable_logic_events_combobox = False
