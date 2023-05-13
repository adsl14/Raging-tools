from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from pyglet.gl import GLException

from lib.functions import check_entry_module, get_name_from_file, show_progress_value
from lib.packages import image, QImage, QPixmap, QMessageBox, os, struct, QStandardItemModel, QStandardItem
from lib.vram_explorer.VEV import VEV
from lib.vram_explorer.classes.MTRL.MtrlInfo import MtrlInfo
from lib.vram_explorer.classes.MTRL.MtrlLayer import MtrlLayer
from lib.vram_explorer.classes.MTRL.MtrlProp import MtrlProp
from lib.vram_explorer.classes.PSHD.PshdInfo import PshdInfo
from lib.vram_explorer.classes.SCNE.EyeData import EyeData
from lib.vram_explorer.classes.SCNE.ScneEyeInfo import ScneEyeInfo
from lib.vram_explorer.classes.SCNE.ScneMaterial import ScneMaterial
from lib.vram_explorer.classes.SCNE.ScneMaterialInfo import ScneMaterialInfo
from lib.vram_explorer.classes.SCNE.ScneModel import ScneModel
from lib.vram_explorer.classes.SHAP.ShapInfo import ShapInfo
from lib.vram_explorer.classes.SPRP.SprpDataEntry import SprpDataEntry
from lib.vram_explorer.classes.SPRP.SprpDataInfo import SprpDataInfo
from lib.vram_explorer.classes.SPRP.SprpFile import SprpFile
from lib.vram_explorer.classes.SPRP.SprpTypeEntry import SprpTypeEntry
from lib.vram_explorer.classes.TX2D.Tx2dInfo import Tx2dInfo
from lib.vram_explorer.classes.TX2D.Tx2dVram import Tx2dVram
from lib.vram_explorer.classes.VBUF.VBufInfo import VBufInfo
from lib.vram_explorer.classes.VBUF.VertexDecl import VertexDecl
from lib.vram_explorer.classes.VSHD.VshdInfo import VshdInfo
from lib.vram_explorer.functions.action_logic import action_export_all_logic, action_import_all_logic, \
    action_import_logic, action_remove_logic, action_export_logic, action_add_logic, action_material_val_changed, \
    action_layer_val_changed, action_type_val_changed, action_texture_val_changed, action_add_material_logic, \
    action_remove_material_logic, action_material_children_logic, action_model_part_val_changed, \
    action_material_model_part_val_changed, show_texture, action_rgb_changed_logic, action_cancel_material_logic, \
    action_save_material_logic, action_effect_val_changed, action_material_export_logic, action_material_import_logic, \
    action_material_export_all_logic, action_material_import_all_logic
from lib.vram_explorer.functions.auxiliary import get_encoding_name, create_header, change_endian, \
    get_dxt_value, fix_bmp_header_data, check_name_is_string_table, write_separator_vram, \
    search_texture
from lib.vram_explorer.functions.xbox_swizzle import process


# Step 1: Create a worker class
class WorkerVef(QObject):

    prepare_buttons_combobox_vram_explorer_signal = pyqtSignal(QMainWindow, str)

    finished = pyqtSignal()
    progressValue = pyqtSignal(float)
    progressText = pyqtSignal(str)

    main_window = None
    vram_separator = b''
    path_output_file = ""
    start_progress = 0.0
    end_progress = 100.0

    def load_spr_vram_file(self):

        # Reset integer values
        VEV.unique_temp_name_offset = 0
        VEV.DbzCharMtrl_offset = 0
        # Reset combo box values
        self.main_window.materialVal.clear()

        self.main_window.typeVal.clear()
        self.main_window.typeVal.addItem("", 0)
        for layer_type in VEV.layer_type:
            self.main_window.typeVal.addItem(layer_type, 0)

        self.main_window.effectVal.clear()
        self.main_window.effectVal.addItem("", 0)
        for layer_effect in VEV.layer_effect:
            self.main_window.effectVal.addItem(layer_effect, 0)

        self.main_window.textureVal.clear()
        self.main_window.textureVal.addItem("", 0)
        self.main_window.modelPartVal.clear()
        self.main_window.materialModelPartVal.clear()
        self.main_window.materialModelPartVal.addItem("", 0)
        # Reset model list view
        self.main_window.listView.model().clear()

        # Get basename from spr_file_path
        basename = os.path.basename(os.path.splitext(VEV.spr_file_path)[0])

        # Open spr and vram (2 tasks)
        step_progress = self.end_progress / 2
        open_spr_file(self, step_progress, self.main_window, self.main_window.listView.model(), VEV.spr_file_path)
        open_vram_file(self, step_progress, VEV.vram_file_path)

        # Prepare all the buttons, comboboxes, set first index ina list and everything related to the GUI in terms of 'set'
        self.prepare_buttons_combobox_vram_explorer_signal.emit(self.main_window, basename)

        # Finish the thread
        self.finished.emit()

    def save_spr_vram_file(self):

        # Default paths
        spr_file_path_modified = os.path.join(self.path_output_file, os.path.basename(VEV.spr_file_path))
        vram_file_path_modified = os.path.join(self.path_output_file, os.path.basename(VEV.vram_file_path))

        # Vars used in order to create the spr from scratch
        num_textures, entry_count, name_offset, entry_info_size, ioram_name_offset, ioram_data_size, vram_name_offset, \
            vram_data_size = self.main_window.listView.model().rowCount(), 0, 0, 0, 0, 0, 0, 0
        string_name_offset = 1
        string_table_size, data_entry_size, data_offset, data_size = 0, 0, 0, 0
        entry_info, header, string_table, data_entry, data = b'', b'', b'', b'', b''
        # Vars used of the mtrl
        num_material = 0
        # Vars used for the txan
        txan_name_offset_assigned = []
        txan_entry = SprpTypeEntry()
        # We will save in this class, some special name offsets
        special_names_dict = {}

        # It will generate the spr from scratch
        if VEV.enable_spr_scratch:

            # Calculate the step for the progress bar
            step_report = self.end_progress / len(VEV.sprp_file.type_entry)
            # Get each type entry and write the data
            for type_entry in VEV.sprp_file.type_entry:

                # ------------------
                # --- Write BIN ---
                # ------------------
                if b'BIN ' == type_entry:
                    # Get the type entry bin
                    bin_type_entry = VEV.sprp_file.type_entry[b'BIN ']

                    # Get each bin data entry
                    sub_step_report = step_report / bin_type_entry.data_count
                    for i in range(0, bin_type_entry.data_count):
                        # Get the data entry for the BIN
                        bin_data_entry = bin_type_entry.data_entry[i]

                        # Report progress
                        self.progressText.emit("Saving " + type_entry.decode('utf-8') + ": writting " + bin_data_entry.data_info.name)
                        show_progress_value(self, sub_step_report)

                        # Write the name for each bin
                        name = bin_data_entry.data_info.name
                        string_table += b'\x00' + name.encode('utf-8')
                        string_table_size += 1 + len(name)

                        # Write the data_entry for each bin
                        data_entry += bin_data_entry.data_type
                        data_entry += i.to_bytes(4, 'big')
                        data_entry += string_name_offset.to_bytes(4, 'big')
                        data_entry += data_offset.to_bytes(4, 'big')
                        data_entry += bin_data_entry.data_info.data_size.to_bytes(4, 'big')
                        data_entry += bin_data_entry.data_info.child_count.to_bytes(4, 'big')
                        # We write the child offset later

                        # Write the data for each bin
                        data += bin_data_entry.data_info.data
                        data_size += bin_data_entry.data_info.data_size

                        # Write children (if any)
                        if bin_data_entry.data_info.child_count > 0:
                            string_table_child, string_table_child_size, string_name_offset, \
                                data_child, data_child_size, data_offset = \
                                write_children(self.main_window, num_material, num_textures,
                                               bin_data_entry.data_info, b'BIN ',
                                               string_table_size + 1, data_size, special_names_dict)

                            # Update the string_name and string_table_size
                            string_table += string_table_child
                            string_table_size += string_table_child_size

                            # Update the data and data_size
                            data += data_child
                            data_size += data_child_size

                            # Write in the data entry, the children offset
                            data_entry += data_offset.to_bytes(4, 'big')
                        else:
                            # Child offset
                            data_entry += b'\x00\x00\x00\x00'
                        data_entry += b'\x00\x00\x00\x00'
                        data_entry_size += 32

                        # Check if the data, the module of 16 is 0
                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                        # Update offsets for the next entry
                        string_name_offset = 1 + string_table_size
                        data_offset = data_size

                    # Update the entry info
                    entry_info += b'BIN ' + b'\x00\x01\x00\x00' + \
                                  bin_type_entry.data_count.to_bytes(4, 'big')
                    # Update the sizes
                    entry_count += 1
                    entry_info_size += 12

                # ------------------
                # --- Write TX2D ---
                # ------------------
                if b'TX2D' == type_entry:
                    entry_info, entry_info_size, entry_count, string_table, string_table_size, string_name_offset, data_entry, \
                        data_entry_size, data, data_size, data_offset, vram_data_size = \
                        generate_tx2d_entry(self, step_report, self.main_window, vram_file_path_modified, entry_info,
                                            entry_info_size, entry_count, string_table,
                                            string_table_size, string_name_offset, data_entry,
                                            data_entry_size, data, data_size, data_offset,
                                            self.vram_separator, num_textures, num_material, special_names_dict)

                # ------------------
                # --- Write VSHD ---
                # ------------------
                if b'VSHD' == type_entry:
                    # Get the type entry vshd
                    vshd_type_entry = VEV.sprp_file.type_entry[b'VSHD']

                    # Get each vshd data entry
                    sub_step_report = step_report / vshd_type_entry.data_count
                    for i in range(0, vshd_type_entry.data_count):
                        # Get the data entry for the VSHD
                        vshd_data_entry = vshd_type_entry.data_entry[i]

                        # Get the data for the vshd
                        vshd_data = vshd_data_entry.data_info.data

                        # Report progress
                        self.progressText.emit("Saving " + type_entry.decode('utf-8') + ": writting " + vshd_data_entry.data_info.name)
                        show_progress_value(self, sub_step_report)

                        # Write the name for each vshd
                        vshd_data_entry.data_info.new_name_offset = string_name_offset
                        string_table += b'\x00' + vshd_data_entry.data_info.name.encode('utf-8')
                        string_table_size += 1 + len(vshd_data_entry.data_info.name)

                        # Write the data_entry for each vshd
                        data_entry += vshd_data_entry.data_type
                        data_entry += i.to_bytes(4, 'big')
                        data_entry += string_name_offset.to_bytes(4, 'big')
                        data_entry += (data_offset + vshd_data.data_size).to_bytes(4, 'big')
                        data_entry += vshd_data_entry.data_info.data_size.to_bytes(4, 'big')
                        data_entry += vshd_data_entry.data_info.child_count.to_bytes(4, 'big')
                        # We write the child offset later

                        # Write the data for each vshd
                        data += vshd_data.data
                        data += vshd_data.unk0x00
                        data += vshd_data.data_size.to_bytes(4, 'big')
                        data += vshd_data.unk0x10
                        data_size += vshd_data.data_size + vshd_data_entry.data_info.data_size

                        # Write children (if any)
                        if vshd_data_entry.data_info.child_count > 0:
                            string_table_child, string_table_child_size, string_name_offset, \
                                data_child, data_child_size, data_offset = \
                                write_children(self.main_window, num_material, num_textures,
                                               vshd_data_entry.data_info, b'VSHD',
                                               string_table_size + 1, data_size, special_names_dict)

                            # Update the string_name and string_table_size
                            string_table += string_table_child
                            string_table_size += string_table_child_size

                            # Update the data and data_size
                            data += data_child
                            data_size += data_child_size

                            # Write in the data entry, the children offset
                            data_entry += data_offset.to_bytes(4, 'big')
                        else:
                            # Child offset
                            data_entry += b'\x00\x00\x00\x00'
                        data_entry += b'\x00\x00\x00\x00'
                        data_entry_size += 32

                        # Check if the data, the module of 16 is 0
                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                        # Update offsets for the next entry
                        string_name_offset = 1 + string_table_size
                        data_offset = data_size

                    # Update the entry info
                    entry_info += b'VSHD' + b'\x00\x00\x00\x08' + \
                                  vshd_type_entry.data_count.to_bytes(4, 'big')
                    # Update the sizes
                    entry_count += 1
                    entry_info_size += 12

                # ------------------
                # --- Write PSHD ---
                # ------------------
                if b'PSHD' == type_entry:
                    # Get the type entry pshd
                    pshd_type_entry = VEV.sprp_file.type_entry[b'PSHD']

                    # Get each pshd data entry
                    sub_step_report = step_report / pshd_type_entry.data_count
                    for i in range(0, pshd_type_entry.data_count):
                        # Get the data entry for the PSHD
                        pshd_data_entry = pshd_type_entry.data_entry[i]

                        # Get the data for the pshd
                        pshd_data = pshd_data_entry.data_info.data

                        # Report progress
                        self.progressText.emit("Saving " + type_entry.decode('utf-8') + ": writting " + pshd_data_entry.data_info.name)
                        show_progress_value(self, sub_step_report)

                        # Write the name for each pshd
                        pshd_data_entry.data_info.new_name_offset = string_name_offset
                        string_table += b'\x00' + pshd_data_entry.data_info.name.encode('utf-8')
                        string_table_size += 1 + len(pshd_data_entry.data_info.name)

                        # Write the data_entry for each pshd
                        data_entry += pshd_data_entry.data_type
                        data_entry += i.to_bytes(4, 'big')
                        data_entry += string_name_offset.to_bytes(4, 'big')
                        data_entry += (data_offset + pshd_data.data_size).to_bytes(4, 'big')
                        data_entry += pshd_data_entry.data_info.data_size.to_bytes(4, 'big')
                        data_entry += pshd_data_entry.data_info.child_count.to_bytes(4, 'big')
                        # We write the child offset later

                        # Write the data for each vshd
                        data += pshd_data.data
                        data += pshd_data.unk0x00
                        data += pshd_data.data_size.to_bytes(4, 'big')
                        data_size += pshd_data.data_size + pshd_data_entry.data_info.data_size

                        # Write children (if any)
                        if pshd_data_entry.data_info.child_count > 0:
                            string_table_child, string_table_child_size, string_name_offset, \
                                data_child, data_child_size, data_offset = \
                                write_children(self.main_window, num_material, num_textures,
                                               pshd_data_entry.data_info, b'PSHD',
                                               string_table_size + 1, data_size, special_names_dict)

                            # Update the string_name and string_table_size
                            string_table += string_table_child
                            string_table_size += string_table_child_size

                            # Update the data and data_size
                            data += data_child
                            data_size += data_child_size

                            # Write in the data entry, the children offset
                            data_entry += data_offset.to_bytes(4, 'big')
                        else:
                            # Child offset
                            data_entry += b'\x00\x00\x00\x00'
                        data_entry += b'\x00\x00\x00\x00'
                        data_entry_size += 32

                        # Check if the data, the module of 16 is 0
                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                        # Update offsets for the next entry
                        string_name_offset = 1 + string_table_size
                        data_offset = data_size

                    # Update the entry info
                    entry_info += b'PSHD' + b'\x00\x00\x00\x08' + \
                                  pshd_type_entry.data_count.to_bytes(4, 'big')
                    # Update the sizes
                    entry_count += 1
                    entry_info_size += 12

                # ------------------
                # --- Write MTRL ---
                # ------------------
                if b'MTRL' == type_entry:
                    num_material = self.main_window.materialVal.count()

                    # TXAN values (will be used to know if the txan entries name offset are
                    # already added to the spr)
                    if b'TXAN' in VEV.sprp_file.type_entry:
                        txan_entry = VEV.sprp_file.type_entry[b"TXAN"]
                        for _ in range(0, txan_entry.data_count):
                            txan_name_offset_assigned.append(False)

                    # Write each material
                    sub_step_report = step_report / num_material
                    for i in range(0, num_material):
                        # Get the material from the tool
                        mtrl_data_entry = self.main_window.materialVal.itemData(i)

                        # Report progress
                        self.progressText.emit("Saving " + type_entry.decode('utf-8') + ": writting " + mtrl_data_entry.data_info.name)
                        show_progress_value(self, sub_step_report)

                        # Write the name for each material
                        mtrl_data_entry.data_info.new_name_offset = string_name_offset
                        string_table += b'\x00' + mtrl_data_entry.data_info.name.encode('utf-8')
                        string_table_size += 1 + len(mtrl_data_entry.data_info.name)

                        # Write the data_entry for each material
                        data_entry += mtrl_data_entry.data_type
                        data_entry += i.to_bytes(4, 'big')
                        mtrl_data_entry.data_info.new_name_offset = string_name_offset
                        data_entry += mtrl_data_entry.data_info.new_name_offset.to_bytes(4, 'big')
                        data_entry += data_offset.to_bytes(4, 'big')
                        data_entry += mtrl_data_entry.data_info.data_size.to_bytes(4, 'big')
                        data_entry += mtrl_data_entry.data_info.child_count.to_bytes(4, 'big')
                        # The child offset will be calculated later

                        # Write the data for each material
                        mtrl_info = mtrl_data_entry.data_info.data
                        data += mtrl_info.unk_00
                        for layer in mtrl_info.layers:

                            # Assing to the spr, the layer type
                            if layer.layer_name == "":
                                data += b'\00\00\00\00'
                            else:
                                # The special name wasn't added to the string name, so the name
                                # offset will be calculated
                                if layer.layer_name not in special_names_dict:
                                    # Write the name for the special name
                                    special_names_dict[layer.layer_name] = 1 + string_table_size
                                    string_table += b'\x00' + layer.layer_name.encode('utf-8')
                                    string_table_size += 1 + len(layer.layer_name)

                                data += special_names_dict[layer.layer_name].to_bytes(4, 'big')

                            # Search for the texture assigned to the material
                            if layer.source_name_offset == 0:
                                data += b'\00\00\00\00'
                            else:
                                # Search the texture
                                found, data = search_texture(self.main_window, data, layer.source_name_offset,
                                                             num_textures)
                                # Search in the TXAN entries
                                if not found:
                                    for j in range(0, txan_entry.data_count):
                                        txan_data_entry = txan_entry.data_entry[j]
                                        if txan_data_entry.data_info.name_offset == layer. \
                                                source_name_offset:
                                            # The TXAN wasn't added to the string name, so the name
                                            # offset will be calculated
                                            if not txan_name_offset_assigned[j]:
                                                name = txan_data_entry.data_info.name + \
                                                       ("." + txan_data_entry.data_info.extension
                                                        if txan_data_entry.data_info.extension else "")
                                                txan_data_entry.data_info.new_name_offset = \
                                                    1 + string_table_size
                                                string_table += b'\x00' + name.encode('utf-8')
                                                string_table_size += 1 + len(name)
                                                txan_name_offset_assigned[j] = True
                                            data += txan_data_entry.data_info.new_name_offset. \
                                                to_bytes(4, 'big')
                                            found = True
                                            break
                                # If we didn't find anything, we add it to the special names var.
                                if not found:
                                    # The special name wasn't added to the string name, so the name
                                    # offset will be calculated
                                    if layer.source_name not in special_names_dict:
                                        # Write the name for the special name
                                        special_names_dict[layer.source_name] = 1 + string_table_size
                                        string_table += b'\x00' + layer.source_name.encode('utf-8')
                                        string_table_size += 1 + len(layer.source_name)

                                    data += special_names_dict[layer.source_name].to_bytes(4, 'big')

                        data_size += mtrl_data_entry.data_info.data_size

                        # Write the children material (if any)
                        if mtrl_data_entry.data_info.child_count > 0:
                            string_table_child, string_table_child_size, string_name_offset, \
                                data_child, data_child_size, data_offset = \
                                write_children(self.main_window, num_material, num_textures,
                                               mtrl_data_entry.data_info, b'MTRL',
                                               string_table_size + 1, data_size, special_names_dict)

                            # Update the string_name and string_table_size
                            string_table += string_table_child
                            string_table_size += string_table_child_size

                            # Update the data and data_size
                            data += data_child
                            data_size += data_child_size

                            # Write in the data entry, the children offset
                            data_entry += data_offset.to_bytes(4, 'big')
                        else:
                            # Child offset
                            data_entry += b'\00\00\00\00'
                        data_entry += b'\00\00\00\00'
                        data_entry_size += 32

                        # Check if the data, the module of 16 is 0
                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                        # Update offsets for the next entry
                        string_name_offset = 1 + string_table_size
                        data_offset = data_size

                    # Update the entry info
                    entry_info += b'MTRL' + b'\x00\x00\x00\x08' + num_material.to_bytes(4, 'big')
                    # Update the sizes
                    entry_count += 1
                    entry_info_size += 12

                # ------------------
                # --- Write SHAP ---
                # ------------------
                if b'SHAP' == type_entry:
                    # Get the type entry shap
                    shap_type_entry = VEV.sprp_file.type_entry[b'SHAP']

                    # Get each shape data entry
                    sub_step_report = step_report / shap_type_entry.data_count
                    for i in range(0, shap_type_entry.data_count):
                        # Get the data entry for the SHAP
                        shap_data_entry = shap_type_entry.data_entry[i]

                        # Report progress
                        self.progressText.emit("Saving " + type_entry.decode('utf-8') + ": writting " + shap_data_entry.data_info.name)
                        show_progress_value(self, sub_step_report)

                        # Write the name for each shape
                        shap_data_entry.data_info.new_name_offset = string_name_offset
                        string_table += b'\x00' + shap_data_entry.data_info.name.encode('utf-8')
                        string_table_size += 1 + len(shap_data_entry.data_info.name)

                        # Write the data_entry for each shape
                        data_entry += shap_data_entry.data_type
                        data_entry += i.to_bytes(4, 'big')
                        data_entry += string_name_offset.to_bytes(4, 'big')
                        data_entry += data_offset.to_bytes(4, 'big')
                        data_entry += shap_data_entry.data_info.data_size.to_bytes(4, 'big')
                        data_entry += shap_data_entry.data_info.child_count.to_bytes(4, 'big')
                        # We write the child offset later

                        # Write the data for each shape
                        shap_info = shap_data_entry.data_info.data
                        data += shap_info.data
                        data_size += shap_data_entry.data_info.data_size

                        # Write children (if any)
                        if shap_data_entry.data_info.child_count > 0:
                            string_table_child, string_table_child_size, string_name_offset, \
                                data_child, data_child_size, data_offset = \
                                write_children(self.main_window, num_material, num_textures,
                                               shap_data_entry.data_info, b'SHAP',
                                               string_table_size + 1, data_size, special_names_dict)

                            # Update the string_name and string_table_size
                            string_table += string_table_child
                            string_table_size += string_table_child_size

                            # Update the data and data_size
                            data += data_child
                            data_size += data_child_size

                            # Write in the data entry, the children offset
                            data_entry += data_offset.to_bytes(4, 'big')
                        else:
                            # Child offset
                            data_entry += b'\x00\x00\x00\x00'
                        data_entry += b'\x00\x00\x00\x00'
                        data_entry_size += 32

                        # Check if the data, the module of 16 is 0
                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                        # Update offsets for the next entry
                        string_name_offset = 1 + string_table_size
                        data_offset = data_size

                    # Update the entry info
                    entry_info += b'SHAP' + b'\x00\x00\x00\x05' + \
                                  shap_type_entry.data_count.to_bytes(4, 'big')
                    # Update the sizes
                    entry_count += 1
                    entry_info_size += 12

                # ------------------
                # --- Write VBUF ---
                # ------------------
                if b'VBUF' == type_entry:
                    # Get the type entry vbuf
                    vbuf_type_entry = VEV.sprp_file.type_entry[b'VBUF']

                    # Get each vbuf data entry
                    sub_step_report = step_report / vbuf_type_entry.data_count
                    for i in range(0, vbuf_type_entry.data_count):
                        # Get the data entry for the VBUF
                        vbuf_data_entry = vbuf_type_entry.data_entry[i]

                        # Report progress
                        self.progressText.emit("Saving " + type_entry.decode('utf-8') + ": writting " + vbuf_data_entry.data_info.name)
                        show_progress_value(self, sub_step_report)

                        # Write the name for each vbuf
                        vbuf_data_entry.data_info.new_name_offset = string_name_offset
                        string_table += b'\x00' + vbuf_data_entry.data_info.name.encode('utf-8')
                        string_table_size += 1 + len(vbuf_data_entry.data_info.name)

                        # Write each vertexDecl first
                        vbuf_info = vbuf_data_entry.data_info.data
                        data_offset_vertex_decl = data_size
                        for j in range(0, vbuf_info.decl_count_0):

                            vertex_decl = vbuf_info.vertex_decl[j]

                            # Read all the data
                            data += vertex_decl.unk0x00

                            # Search what effect is using the vertex declaration for the mesh
                            # If we don't find anything, we write 0
                            if vertex_decl.resource_name == "":
                                data += b'\00\00\00\00'
                            else:
                                # The special name wasn't added to the string name, so the name
                                # offset will be calculated
                                if vertex_decl.resource_name not in special_names_dict:
                                    # Write the name for the special name
                                    special_names_dict[vertex_decl.resource_name] = 1 + \
                                                                                    string_table_size
                                    string_table += b'\x00' + vertex_decl.resource_name.encode('utf-8')
                                    string_table_size += 1 + len(vertex_decl.resource_name)

                                data += special_names_dict[vertex_decl.resource_name].to_bytes(4, 'big')

                            data += vertex_decl.vertex_usage.to_bytes(2, 'big')
                            data += vertex_decl.index.to_bytes(2, 'big')
                            data += vertex_decl.vertex_format
                            data += vertex_decl.stride.to_bytes(2, 'big')
                            data += vertex_decl.offset.to_bytes(4, 'big')
                            data_size += 20

                        # Check if the data, the module of 16 is 0
                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                        # We check the size of the vbuf data due to Game Assets Converter
                        # store the size as 'header + data' instead of 'header'. If the size is
                        # different from 32 or 40 (40 is for UT), we modify the original size
                        if vbuf_data_entry.data_info.data_size != 32 and vbuf_data_entry.data_info.data_size != 40:
                            vbuf_data_entry.data_info.data_size = 32

                        # Write the data_entry for each vbuf
                        data_offset = data_size
                        data_entry += vbuf_data_entry.data_type
                        data_entry += i.to_bytes(4, 'big')
                        data_entry += string_name_offset.to_bytes(4, 'big')
                        data_entry += data_offset.to_bytes(4, 'big')
                        data_entry += vbuf_data_entry.data_info.data_size.to_bytes(4, 'big')
                        data_entry += vbuf_data_entry.data_info.child_count.to_bytes(4, 'big')
                        # We write the child offset later

                        # Write the data for each vbuf
                        data += vbuf_info.unk0x00
                        data += vbuf_info.unk0x04
                        data += vbuf_info.data_offset.to_bytes(4, 'big')
                        data += vbuf_info.data_size.to_bytes(4, 'big')
                        data += vbuf_info.vertex_count.to_bytes(4, 'big')

                        # If the data_info size of the data_entry for the vbuf is 40, means is a UT/Zenkai Battle character
                        if vbuf_data_entry.data_info.data_size == 40:
                            data += vbuf_info.index_count.to_bytes(4, 'big')

                        data += vbuf_info.unk0x14
                        data += vbuf_info.unk0x16
                        data += vbuf_info.decl_count_0.to_bytes(2, 'big')
                        data += vbuf_info.decl_count_1.to_bytes(2, 'big')
                        data += data_offset_vertex_decl.to_bytes(4, 'big')

                        # If the data_info size of the data_entry for the vbuf is 40, means is a UT/Zenkai Battle character
                        if vbuf_data_entry.data_info.data_size == 40:
                            data += vbuf_info.index_offset.to_bytes(4, 'big')

                        data_size += vbuf_data_entry.data_info.data_size

                        # Child offset
                        data_entry += b'\x00\x00\x00\x00'
                        data_entry += b'\x00\x00\x00\x00'
                        data_entry_size += 32

                        # Check if the data, the module of 16 is 0
                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                        # Update offsets for the next entry
                        string_name_offset = 1 + string_table_size
                        data_offset = data_size

                    # Update the entry info
                    entry_info += b'VBUF' + b'\x00\x00\x00\x0A' + \
                                  vbuf_type_entry.data_count.to_bytes(4, 'big')
                    # Update the sizes
                    entry_count += 1
                    entry_info_size += 12

                # ------------------
                # --- Write SCNE ---
                # ------------------
                if b'SCNE' == type_entry:

                    # Get the type entry scne
                    scne_type_entry = VEV.sprp_file.type_entry[b'SCNE']

                    # Get each SCNE entry
                    sub_step_report = step_report / scne_type_entry.data_count
                    for i in range(0, scne_type_entry.data_count):
                        scne_data_entry = scne_type_entry.data_entry[i]

                        # Report progress
                        self.progressText.emit("Saving " + type_entry.decode('utf-8') + ": writting " + scne_data_entry.data_info.name)
                        show_progress_value(self, sub_step_report)

                        # Write children (if any)
                        if scne_data_entry.data_info.child_count > 0:
                            string_table_child, string_table_child_size, string_name_offset, \
                                data_child, data_child_size, data_offset = \
                                write_children(self.main_window, num_material, num_textures,
                                               scne_data_entry.data_info, b'SCNE',
                                               string_table_size + 1, data_size, special_names_dict)

                            # Reset all the [NODES] children name offset calculated
                            nodes = scne_data_entry.data_info.child_info[1].child_info
                            for node in nodes:
                                if node.name_offset_calculated:
                                    node.name_offset_calculated = False

                            # Update the string_name and string_table_size
                            string_table += string_table_child
                            string_table_size += string_table_child_size

                            # Update the data and data_size
                            data += data_child
                            data_size += data_child_size

                        # Write the name for the scne
                        name = "scene_" + self.main_window.fileNameText.text() + ".mb"
                        string_table += b'\x00' + name.encode('utf-8')
                        string_table_size += 1 + len(name)

                        # Write the data_entry
                        data_entry += scne_data_entry.data_type
                        data_entry += i.to_bytes(4, 'big')
                        data_entry += string_name_offset.to_bytes(4, 'big')
                        data_entry += data_offset.to_bytes(4, 'big')
                        data_entry += scne_data_entry.data_info.data_size.to_bytes(4, 'big')
                        data_entry += scne_data_entry.data_info.child_count.to_bytes(4, 'big')
                        data_entry += data_offset.to_bytes(4, 'big')
                        data_entry += b'\x00\x00\x00\x00'
                        data_entry_size += 32

                        # Check if the data, the module of 16 is 0
                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                        # Update offsets for the next entry
                        string_name_offset = 1 + string_table_size
                        data_offset = data_size

                    # Update the entry info
                    entry_info += b'SCNE' + b'\x00\x00\x00\x07' + \
                                  scne_type_entry.data_count.to_bytes(4, 'big')
                    # Update the sizes
                    entry_count += 1
                    entry_info_size += 12

                # ------------------
                # --- Write BONE ---
                # ------------------
                if b'BONE' == type_entry:
                    # Get the type entry bone
                    bone_type_entry = VEV.sprp_file.type_entry[b'BONE']

                    # Get each bone data entry
                    sub_step_report = step_report / bone_type_entry.data_count
                    for i in range(0, bone_type_entry.data_count):
                        # Get the data entry for the BONE
                        bone_data_entry = bone_type_entry.data_entry[i]

                        # Report progress
                        self.progressText.emit("Saving " + type_entry.decode('utf-8') + ": writting " + bone_data_entry.data_info.name)
                        show_progress_value(self, sub_step_report)

                        # Write the name for each bone
                        string_table += b'\x00' + bone_data_entry.data_info.name.encode('utf-8')
                        string_table_size += 1 + len(bone_data_entry.data_info.name)

                        # Write the data_entry for each bone
                        data_entry += bone_data_entry.data_type
                        data_entry += i.to_bytes(4, 'big')
                        data_entry += string_name_offset.to_bytes(4, 'big')
                        data_entry += data_offset.to_bytes(4, 'big')
                        data_entry += bone_data_entry.data_info.data_size.to_bytes(4, 'big')
                        data_entry += bone_data_entry.data_info.child_count.to_bytes(4, 'big')
                        # We write the child offset later

                        # Write the data for each bone
                        data += bone_data_entry.data_info.data
                        data_size += bone_data_entry.data_info.data_size

                        # Write children (if any)
                        if bone_data_entry.data_info.child_count > 0:
                            string_table_child, string_table_child_size, string_name_offset, \
                                    data_child, data_child_size, data_offset = \
                                    write_children(self.main_window, num_material, num_textures,
                                                   bone_data_entry.data_info, b'BONE',
                                                   string_table_size + 1, data_size, special_names_dict)

                            # Update the string_name and string_table_size
                            string_table += string_table_child
                            string_table_size += string_table_child_size

                            # Update the data and data_size
                            data += data_child
                            data_size += data_child_size

                            # Write in the data entry, the children offset
                            data_entry += data_offset.to_bytes(4, 'big')
                        else:
                            # Child offset
                            data_entry += b'\x00\x00\x00\x00'
                        data_entry += b'\x00\x00\x00\x00'
                        data_entry_size += 32

                        # Check if the data, the module of 16 is 0
                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                        # Update offsets for the next entry
                        string_name_offset = 1 + string_table_size
                        data_offset = data_size

                    # Update the entry info
                    entry_info += b'BONE' + b'\x00\x00\x00\x03' + \
                                  bone_type_entry.data_count.to_bytes(4, 'big')
                    # Update the sizes
                    entry_count += 1
                    entry_info_size += 12

                # ------------------
                # --- Write DRVN ---
                # ------------------
                if b'DRVN' == type_entry:
                    # Get the type entry drvn
                    drvn_type_entry = VEV.sprp_file.type_entry[b'DRVN']

                    # Get each drvn data entry
                    sub_step_report = step_report / drvn_type_entry.data_count
                    for i in range(0, drvn_type_entry.data_count):
                        # Get the data entry for the DRVN
                        drvn_data_entry = drvn_type_entry.data_entry[i]

                        # Report progress
                        self.progressText.emit("Saving " + type_entry.decode('utf-8') + ": writting " + drvn_data_entry.data_info.name)
                        show_progress_value(self, sub_step_report)

                        # Write the name for each drvn
                        name = "driven_" + self.main_window.fileNameText.text() + ".mb"
                        string_table += b'\x00' + name.encode('utf-8')
                        string_table_size += 1 + len(name)

                        # Write the data_entry for each devn
                        data_entry += drvn_data_entry.data_type
                        data_entry += i.to_bytes(4, 'big')
                        data_entry += string_name_offset.to_bytes(4, 'big')
                        data_entry += data_offset.to_bytes(4, 'big')
                        data_entry += drvn_data_entry.data_info.data_size.to_bytes(4, 'big')
                        data_entry += drvn_data_entry.data_info.child_count.to_bytes(4, 'big')
                        # We write the child offset later

                        # Write the data for each drvn
                        data += drvn_data_entry.data_info.data
                        data_size += drvn_data_entry.data_info.data_size

                        # Write children (if any)
                        if drvn_data_entry.data_info.child_count > 0:
                            string_table_child, string_table_child_size, string_name_offset, \
                                data_child, data_child_size, data_offset = \
                                write_children(self.main_window, num_material, num_textures,
                                               drvn_data_entry.data_info, b'DRVN',
                                               string_table_size + 1, data_size, special_names_dict)

                            # Update the string_name and string_table_size
                            string_table += string_table_child
                            string_table_size += string_table_child_size

                            # Update the data and data_size
                            data += data_child
                            data_size += data_child_size

                            # Write in the data entry, the children offset
                            data_entry += data_offset.to_bytes(4, 'big')
                        else:
                            # Child offset
                            data_entry += b'\x00\x00\x00\x00'
                        data_entry += b'\x00\x00\x00\x00'
                        data_entry_size += 32

                        # Check if the data, the module of 16 is 0
                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                        # Update offsets for the next entry
                        string_name_offset = 1 + string_table_size
                        data_offset = data_size

                    # Update the entry info
                    entry_info += b'DRVN' + b'\x00\x00\x00\x01' + \
                                  drvn_type_entry.data_count.to_bytes(4, 'big')
                    # Update the sizes
                    entry_count += 1
                    entry_info_size += 12

                # ------------------
                # --- Write TXAN ---
                # ------------------
                if b'TXAN' == type_entry:
                    # Get the type entry txan
                    txan_type_entry = VEV.sprp_file.type_entry[b'TXAN']

                    # Get each txan data entry
                    sub_step_report = step_report / txan_type_entry.data_count
                    for i in range(0, txan_type_entry.data_count):
                        # Get the data entry for the TXAN
                        txan_data_entry = txan_type_entry.data_entry[i]

                        # Report progress
                        self.progressText.emit("Saving " + type_entry.decode('utf-8') + ": writting " + txan_data_entry.data_info.name)
                        show_progress_value(self, sub_step_report)

                        # Write the data_entry for each txan
                        data_entry += txan_type_entry.data_type
                        data_entry += i.to_bytes(4, 'big')

                        if txan_name_offset_assigned[i]:
                            data_entry += txan_data_entry.data_info.new_name_offset.to_bytes(4, 'big')
                        else:
                            # Write the name for each txan
                            string_table += b'\x00' + txan_data_entry.data_info.name.encode('utf-8')
                            string_table_size += 1 + len(txan_data_entry.data_info.name)
                            data_entry += string_name_offset.to_bytes(4, 'big')
                            # Update offset for the string table
                            string_name_offset = 1 + string_table_size

                        data_entry += data_offset.to_bytes(4, 'big')
                        data_entry += txan_data_entry.data_info.data_size.to_bytes(4, 'big')
                        data_entry += txan_data_entry.data_info.child_count.to_bytes(4, 'big')
                        # We write the child offset later

                        # Write the data for each txan
                        data += txan_data_entry.data_info.data
                        data_size += txan_data_entry.data_info.data_size

                        # Write children (if any)
                        if txan_data_entry.data_info.child_count > 0:
                            string_table_child, string_table_child_size, string_name_offset, \
                                data_child, data_child_size, data_offset = \
                                write_children(self.main_window, num_material, num_textures,
                                               txan_data_entry.data_info, b'TXAN',
                                               string_table_size + 1, data_size, special_names_dict)

                            # Update the string_name and string_table_size
                            string_table += string_table_child
                            string_table_size += string_table_child_size

                            # Update the data and data_size
                            data += data_child
                            data_size += data_child_size

                            # Write in the data entry, the children offset
                            data_entry += data_offset.to_bytes(4, 'big')
                        else:
                            # Child offset
                            data_entry += b'\x00\x00\x00\x00'
                        data_entry += b'\x00\x00\x00\x00'
                        data_entry_size += 32

                        # Check if the data, the module of 16 is 0
                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                        # Update offsets for the next entry
                        data_offset = data_size

                    # Update the entry info
                    entry_info += b'TXAN' + b'\x00\x00\x00\x01' + \
                                  txan_type_entry.data_count.to_bytes(4, 'big')
                    # Update the sizes
                    entry_count += 1
                    entry_info_size += 12

                # ------------------
                # --- Write ANIM ---
                # ------------------
                if b'ANIM' == type_entry:
                    # Get the type entry anim
                    anim_type_entry = VEV.sprp_file.type_entry[b'ANIM']

                    # Get each anim data entry
                    sub_step_report = step_report / anim_type_entry.data_count
                    for i in range(0, anim_type_entry.data_count):
                        # Get the data entry for the ANIM
                        anim_data_entry = anim_type_entry.data_entry[i]

                        # Report progress
                        self.progressText.emit("Saving " + type_entry.decode('utf-8') + ": writting " + anim_data_entry.data_info.name)
                        show_progress_value(self, sub_step_report)

                        # Write the name for each anim
                        string_table += b'\x00' + anim_data_entry.data_info.name.encode('utf-8')
                        string_table_size += 1 + len(anim_data_entry.data_info.name)

                        # Write the data_entry for each anim
                        data_entry += anim_data_entry.data_type
                        data_entry += i.to_bytes(4, 'big')
                        data_entry += string_name_offset.to_bytes(4, 'big')
                        data_entry += data_offset.to_bytes(4, 'big')
                        data_entry += anim_data_entry.data_info.data_size.to_bytes(4, 'big')
                        data_entry += anim_data_entry.data_info.child_count.to_bytes(4, 'big')
                        # We write the child offset later

                        # Write the data for each anim
                        data += anim_data_entry.data_info.data
                        data_size += anim_data_entry.data_info.data_size

                        # Write children (if any)
                        if anim_data_entry.data_info.child_count > 0:
                            string_table_child, string_table_child_size, string_name_offset, \
                                data_child, data_child_size, data_offset = \
                                write_children(self.main_window, num_material, num_textures,
                                               anim_data_entry.data_info, b'ANIM',
                                               string_table_size + 1, data_size, special_names_dict)

                            # Update the string_name and string_table_size
                            string_table += string_table_child
                            string_table_size += string_table_child_size

                            # Update the data and data_size
                            data += data_child
                            data_size += data_child_size

                            # Write in the data entry, the children offset
                            data_entry += data_offset.to_bytes(4, 'big')
                        else:
                            # Child offset
                            data_entry += b'\x00\x00\x00\x00'
                        data_entry += b'\x00\x00\x00\x00'
                        data_entry_size += 32

                        # Check if the data, the module of 16 is 0
                        data, data_size, padding_size = check_entry_module(data, data_size, 16)

                        # Update offsets for the next entry
                        string_name_offset = 1 + string_table_size
                        data_offset = data_size

                    # Update the entry info
                    entry_info += b'ANIM' + b'\x00\x00\x00\x03' + \
                                  anim_type_entry.data_count.to_bytes(4, 'big')
                    # Update the sizes
                    entry_count += 1
                    entry_info_size += 12

            # Write the basename, ioram and vram offsets names
            # If the spr doesn't have an ioram file, we won't write the name on it
            if VEV.sprp_file.sprp_header.ioram_data_size > 0:

                # Write the xmb extension
                name_offset = 1 + string_table_size
                name = self.main_window.fileNameText.text() + ".xmb"
                string_table += b'\x00' + name.encode('utf-8')
                string_table_size += 1 + len(name)

                ioram_name_offset = 1 + string_table_size
                ioram_data_size = VEV.sprp_file.sprp_header.ioram_data_size
                name = self.main_window.fileNameText.text() + ".ioram"
                string_table += b'\x00' + name.encode('utf-8')
                string_table_size += 1 + len(name)
            else:

                # Write the spr extension
                name_offset = 1 + string_table_size
                name = self.main_window.fileNameText.text() + ".spr"
                string_table += b'\x00' + name.encode('utf-8')
                string_table_size += 1 + len(name)

                ioram_name_offset = 0
                ioram_data_size = 0
            vram_name_offset = 1 + string_table_size
            name = self.main_window.fileNameText.text() + ".vram"
            string_table += b'\x00' + name.encode('utf-8')
            string_table_size += 1 + len(name)

            # Write the watermark
            string_table += b'\x00' + VEV.watermark_message.encode('utf-8')
            string_table_size += 1 + len(VEV.watermark_message)

            # Check if the entry_info, the module of 16 is 0
            entry_info, entry_info_size, padding_size = check_entry_module(entry_info, entry_info_size,
                                                                           16)

            # Check if the string_table_size, the module of 16 is 0
            string_table, string_table_size, padding_size = check_entry_module(string_table,
                                                                               string_table_size, 16)

            # Create the header
            header = VEV.sprp_file.sprp_header.data_tag + b'\00\01\00\01' + \
                entry_count.to_bytes(4, 'big') + b'\00\00\00\00' + name_offset.to_bytes(4, 'big') + \
                entry_info_size.to_bytes(4, 'big') + \
                string_table_size.to_bytes(4, 'big') + data_entry_size.to_bytes(4, 'big') + \
                data_size.to_bytes(4, 'big') + ioram_name_offset.to_bytes(4, 'big') + \
                ioram_data_size.to_bytes(4, 'big') + vram_name_offset.to_bytes(4, 'big') + \
                vram_data_size.to_bytes(4, 'big') + b'\00\00\00\00\00\00\00\00\00\00\00\00'

        # The spr output will be a copy from the original one, the difference will be only the
        # tx2d entry
        else:

            with open(VEV.spr_file_path, mode='rb') as input_spr_file:

                # Store the entry_info
                input_spr_file.seek(64)
                entry_info = input_spr_file.read(VEV.sprp_file.sprp_header.entry_info_size)

                # Store the string table
                string_table = input_spr_file.read(VEV.sprp_file.sprp_header.string_table_size)
                string_table_size = VEV.sprp_file.sprp_header.string_table_size
                # Write the watermark
                string_table += b'\x00' + VEV.watermark_message.encode('utf-8')
                string_table_size += 1 + len(VEV.watermark_message)
                # Check if the string_table_size, the module of 16 is 0
                string_table, string_table_size, padding_size = check_entry_module(string_table,
                                                                                   string_table_size,
                                                                                   16)

                # Calculate the step for the progress bar
                # Write the data entry
                # Write the TX2D entry only
                null, null, null, null, null, null, null, null, data, null, null, vram_data_size = \
                    generate_tx2d_entry(self, self.end_progress, self.main_window, vram_file_path_modified, entry_info,
                                        entry_info_size, entry_count, string_table,
                                        string_table_size, string_name_offset, data_entry,
                                        data_entry_size, data, data_size, data_offset, self.vram_separator,
                                        num_textures, num_material, special_names_dict)
                data_entry = input_spr_file.read(VEV.sprp_file.sprp_header.data_info_size)

                # Write the data
                tx2d_data_size = 48 * num_textures
                input_spr_file.seek(tx2d_data_size, os.SEEK_CUR)
                data = data + input_spr_file.read()

            # Write the header
            header = VEV.sprp_file.sprp_header.data_tag + b'\00\01\00\01' + \
                VEV.sprp_file.sprp_header.entry_count.to_bytes(4, 'big') + b'\00\00\00\00' + \
                VEV.sprp_file.sprp_header.name_offset.to_bytes(4, 'big') + \
                VEV.sprp_file.sprp_header.entry_info_size.to_bytes(4, 'big') + \
                string_table_size.to_bytes(4, 'big') + \
                VEV.sprp_file.sprp_header.data_info_size.to_bytes(4, 'big') + \
                VEV.sprp_file.sprp_header.data_block_size.to_bytes(4, 'big') + \
                VEV.sprp_file.sprp_header.ioram_name_offset.to_bytes(4, 'big') + \
                VEV.sprp_file.sprp_header.ioram_data_size.to_bytes(4, 'big') + \
                VEV.sprp_file.sprp_header.vram_name_offset.to_bytes(4, 'big') + \
                vram_data_size.to_bytes(4, 'big') + b'\00\00\00\00\00\00\00\00\00\00\00\00'

        # Write the spr
        with open(spr_file_path_modified, mode="wb") as output_spr_file:
            output_spr_file.write(header + entry_info + string_table + data_entry + data)

        # Finish the thread
        self.finished.emit()


def initialize_ve(main_window):

    # Buttons
    main_window.exportAllButton.clicked.connect(lambda: action_export_all_logic(main_window))
    main_window.importAllButton.clicked.connect(lambda: action_import_all_logic(main_window))
    main_window.exportButton.clicked.connect(lambda: action_export_logic(main_window))
    main_window.importButton.clicked.connect(lambda: action_import_logic(main_window))
    main_window.removeButton.clicked.connect(lambda: action_remove_logic(main_window))
    main_window.addButton.clicked.connect(lambda: action_add_logic(main_window))
    main_window.exportAllButton.setEnabled(False)
    main_window.importAllButton.setEnabled(False)
    main_window.exportButton.setEnabled(False)
    main_window.importButton.setEnabled(False)
    main_window.removeButton.setEnabled(False)
    main_window.addButton.setEnabled(False)

    # Material
    main_window.exportMaterialButton.clicked.connect(lambda: action_material_export_logic(main_window))
    main_window.importMaterialButton.clicked.connect(lambda: action_material_import_logic(main_window))
    main_window.exportAllMaterialButton.clicked.connect(lambda: action_material_export_all_logic(main_window))
    main_window.importAllMaterialButton.clicked.connect(lambda: action_material_import_all_logic(main_window))
    main_window.editMaterialChildrenButton.clicked.connect(lambda: action_material_children_logic(main_window))
    main_window.addMaterialButton.clicked.connect(lambda: action_add_material_logic(main_window))
    main_window.removeMaterialButton.clicked.connect(lambda: action_remove_material_logic(main_window))
    main_window.materialVal.setEnabled(False)
    main_window.layerVal.setEnabled(False)
    main_window.typeVal.setEnabled(False)
    main_window.effectVal.setEnabled(False)
    main_window.textureVal.setEnabled(False)
    main_window.exportMaterialButton.setEnabled(False)
    main_window.importMaterialButton.setEnabled(False)
    main_window.exportAllMaterialButton.setEnabled(False)
    main_window.importAllMaterialButton.setEnabled(False)
    main_window.addMaterialButton.setEnabled(False)
    main_window.removeMaterialButton.setEnabled(False)
    main_window.editMaterialChildrenButton.setEnabled(False)

    # Model part
    main_window.modelPartVal.setEnabled(False)
    main_window.materialModelPartVal.setEnabled(False)

    # Labels
    main_window.encodingImageText.setVisible(False)
    main_window.mipMapsImageText.setVisible(False)
    main_window.sizeImageText.setVisible(False)
    main_window.fileNameText.setVisible(False)

    # Create a model for the list view of textures
    model = QStandardItemModel()
    main_window.listView.setModel(model)

    # Connect the listener. Since it breaks the vertical bar if we disconnect it, we won't add it to the listen_events_logic
    main_window.listView.selectionModel().currentChanged.connect(lambda: show_texture(main_window.listView,
                                                                                      main_window.imageTexture,
                                                                                      main_window.encodingImageText,
                                                                                      main_window.mipMapsImageText,
                                                                                      main_window.sizeImageText))


def listen_events_logic(main_window, flag):

    if flag:

        # Material
        main_window.materialVal.currentIndexChanged.connect(lambda: action_material_val_changed(main_window))
        main_window.layerVal.currentIndexChanged.connect(lambda: action_layer_val_changed(main_window))
        main_window.typeVal.currentIndexChanged.connect(lambda: action_type_val_changed(main_window))
        main_window.effectVal.currentIndexChanged.connect(lambda: action_effect_val_changed(main_window))
        main_window.textureVal.currentIndexChanged.connect(lambda: action_texture_val_changed(main_window))

        # Model part
        main_window.modelPartVal.currentIndexChanged.connect(lambda: action_model_part_val_changed(main_window))
        main_window.materialModelPartVal.currentIndexChanged.connect(lambda:
                                                                     action_material_model_part_val_changed(main_window))

        # Load the Material children editor window
        main_window.MaterialChildEditorUI.border_color_R_value.valueChanged \
            .connect(lambda: action_rgb_changed_logic(main_window))
        main_window.MaterialChildEditorUI.border_color_G_value.valueChanged \
            .connect(lambda: action_rgb_changed_logic(main_window))
        main_window.MaterialChildEditorUI.border_color_B_value.valueChanged \
            .connect(lambda: action_rgb_changed_logic(main_window))
        main_window.MaterialChildEditorUI.border_color_A_value.valueChanged \
            .connect(lambda: action_rgb_changed_logic(main_window))
        main_window.MaterialChildEditorUI.save_material_button.clicked \
            .connect(lambda: action_save_material_logic(main_window))
        main_window.MaterialChildEditorUI.cancel_material_button.clicked. \
            connect(lambda: action_cancel_material_logic(main_window))

    else:

        try:
            # Material
            main_window.materialVal.disconnect()
            main_window.layerVal.disconnect()
            main_window.typeVal.disconnect()
            main_window.effectVal.disconnect()
            main_window.textureVal.disconnect()

            # Model part
            main_window.modelPartVal.disconnect()
            main_window.materialModelPartVal.disconnect()

            # Load the Material children editor window
            main_window.MaterialChildEditorUI.border_color_R_value.disconnect()
            main_window.MaterialChildEditorUI.border_color_G_value.disconnect()
            main_window.MaterialChildEditorUI.border_color_B_value.disconnect()
            main_window.MaterialChildEditorUI.border_color_A_value.disconnect()
            main_window.MaterialChildEditorUI.save_material_button.disconnect()
            main_window.MaterialChildEditorUI.cancel_material_button.disconnect()
        except TypeError:
            pass


def open_spr_file(worker_vef, end_progress, main_window, model, spr_path):

    # Clean vars
    VEV.sprp_file = SprpFile()
    VEV.exists_mtrl = False
    VEV.enable_spr_scratch = True

    with open(spr_path, mode='rb') as file:

        # Create SPRP_HEADER
        VEV.sprp_file.sprp_header.data_tag = file.read(VEV.bytes2Read)
        file.seek(4, os.SEEK_CUR)
        VEV.sprp_file.sprp_header.entry_count = int.from_bytes(file.read(VEV.bytes2Read), "big")
        file.seek(4, os.SEEK_CUR)
        VEV.sprp_file.sprp_header.name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.entry_info_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.string_table_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.data_info_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.data_block_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.ioram_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.ioram_data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.vram_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
        VEV.sprp_file.sprp_header.vram_data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")

        # Create SPRP_FILE
        VEV.sprp_file.entry_info_base = 64
        VEV.sprp_file.string_table_base = VEV.sprp_file.entry_info_base + VEV.sprp_file.sprp_header.entry_info_size
        VEV.sprp_file.data_info_base = VEV.sprp_file.string_table_base + VEV.sprp_file.sprp_header.string_table_size
        VEV.sprp_file.data_block_base = VEV.sprp_file.data_info_base + VEV.sprp_file.sprp_header.data_info_size
        VEV.sprp_file.file_size = VEV.sprp_file.data_block_base + VEV.sprp_file.sprp_header.data_block_size

        # Create each SPRP_TYPE_ENTRY
        file.seek(VEV.sprp_file.entry_info_base)
        type_entry_offset = 0
        sub_end_progress = end_progress / VEV.sprp_file.sprp_header.entry_count
        for i in range(0, VEV.sprp_file.sprp_header.entry_count):

            # Load each sprp_type_entry
            sprp_type_entry = SprpTypeEntry()
            sprp_type_entry.data_type = file.read(VEV.bytes2Read)
            file.seek(4, os.SEEK_CUR)
            sprp_type_entry.data_count = int.from_bytes(file.read(VEV.bytes2Read), "big")

            # Create each SPRP_DATA_ENTRY and under that, the SPRP_DATA_INFO
            aux_pointer_type_entry = file.tell()
            file.seek(VEV.sprp_file.data_info_base + type_entry_offset)
            sub_sub_end_progress = sub_end_progress / sprp_type_entry.data_count
            for j in range(0, sprp_type_entry.data_count):

                # Report progress
                worker_vef.progressText.emit("Loading spr: reading " + sprp_type_entry.data_type.decode('utf-8') + " entry (" + str(j + 1) + "/" +
                                             str(sprp_type_entry.data_count) + ")")
                show_progress_value(worker_vef, sub_sub_end_progress)

                sprp_data_entry = SprpDataEntry()
                sprp_data_entry.data_type = file.read(VEV.bytes2Read)
                sprp_data_entry.index = int.from_bytes(file.read(VEV.bytes2Read), "big")

                sprp_data_entry.data_info.name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                sprp_data_entry.data_info.data_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                sprp_data_entry.data_info.data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
                sprp_data_entry.data_info.child_count = int.from_bytes(file.read(VEV.bytes2Read), "big")
                sprp_data_entry.data_info.child_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                file.seek(4, os.SEEK_CUR)

                # Store the actual pointer in the file in order to read the following data_entry
                aux_pointer_data_entry = file.tell()

                # Store the name of the sprp_data_info
                # Everything that is not SPR in the header, has names for each data
                if VEV.sprp_file.sprp_header.data_tag != b"SPR\x00":
                    sprp_data_entry.data_info.name,  sprp_data_entry.data_info.extension = \
                        get_name_from_file(file, VEV.sprp_file.string_table_base + sprp_data_entry.data_info.name_offset)
                    base_name_size = len(sprp_data_entry.data_info.name)
                    extension_size = len(sprp_data_entry.data_info.extension)
                    sprp_data_entry.data_info.name_size = base_name_size + (1 + extension_size
                                                                            if extension_size > 0 else 0)
                # If the data header is SPR, we create custom names
                else:
                    sprp_data_entry.data_info.name = sprp_type_entry.data_type.decode('utf-8') + "_" + str(j)

                # Save the data when is the type BIN
                if sprp_type_entry.data_type == b"BIN ":

                    # Move where the actual information starts
                    file.seek(VEV.sprp_file.data_block_base + sprp_data_entry.data_info.data_offset)

                    # Read all the data
                    sprp_data_entry.data_info.data = file.read(sprp_data_entry.data_info.data_size)

                # Save the data when is the type TX2D
                elif sprp_type_entry.data_type == b"TX2D":

                    # Move where the actual information starts
                    file.seek(VEV.sprp_file.data_block_base + sprp_data_entry.data_info.data_offset)

                    # Create the TX2D info
                    tx2d_info = Tx2dInfo()

                    tx2d_info.related_2_encoding = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    tx2d_info.data_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    tx2d_info.unk0x08 = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    tx2d_info.data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    tx2d_info.width = int.from_bytes(file.read(2), "big")
                    tx2d_info.height = int.from_bytes(file.read(2), "big")
                    tx2d_info.unk0x14 = int.from_bytes(file.read(2), "big")
                    tx2d_info.mip_maps = int.from_bytes(file.read(2), "big")
                    tx2d_info.unk0x18 = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    tx2d_info.unk0x1c = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    tx2d_info.dxt_encoding = int.from_bytes(file.read(1), "big")

                    tx2d_info.tx2d_vram = Tx2dVram()

                    # Add the tx2d_data_entry to the combo box (material section)
                    main_window.textureVal.addItem(sprp_data_entry.data_info.name,
                                                   sprp_data_entry.data_info.name_offset)

                    # Save the tx2d info into the data_entry data
                    sprp_data_entry.data_info.data = tx2d_info

                    # Add the texture to the listView
                    item = QStandardItem(sprp_data_entry.data_info.name)
                    item.setData(sprp_data_entry)
                    item.setEditable(False)
                    model.appendRow(item)

                # Save the data when is the type MTRL
                elif sprp_type_entry.data_type == b"MTRL":

                    # Since the spr hold MTRL entries, we store a flag
                    if not VEV.exists_mtrl:
                        VEV.exists_mtrl = True

                    # Move where the actual information starts
                    file.seek(VEV.sprp_file.data_block_base + sprp_data_entry.data_info.data_offset)

                    # Create the MTRL info
                    mtrl_info = MtrlInfo()

                    # Read unk data
                    mtrl_info.unk_00 = file.read(112)

                    # Read each layer (the max number is 10)
                    for k in range(0, 10):
                        mtrl_layer = MtrlLayer()
                        mtrl_layer.layer_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                        mtrl_layer.source_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")

                        # Store the name of the layer
                        if mtrl_layer.layer_name_offset != 0:
                            aux_pointer_mtrl_layer = file.tell()
                            mtrl_layer.layer_name, nothing = get_name_from_file(file, VEV.sprp_file.string_table_base +
                                                                                mtrl_layer.layer_name_offset)

                            # We have added all the type material in the combobox,
                            # but just in case we find another one that we didn't
                            # store before while we're reading the material entries, then, we add the new type material
                            # to the combobox
                            if main_window.typeVal.findText(mtrl_layer.layer_name) == -1:
                                main_window.typeVal.addItem(mtrl_layer.layer_name, 0)

                            file.seek(aux_pointer_mtrl_layer)
                        # Store the name of the source
                        if mtrl_layer.source_name_offset != 0:
                            aux_pointer_mtrl_layer = file.tell()
                            mtrl_layer.source_name, nothing = get_name_from_file(file, VEV.sprp_file.string_table_base +
                                                                                 mtrl_layer.source_name_offset)
                            file.seek(aux_pointer_mtrl_layer)

                        # Store the layer in the actual material
                        mtrl_info.layers.append(mtrl_layer)

                    # Save the mtrlInfo class into the sprp_data_entry data
                    sprp_data_entry.data_info.data = mtrl_info

                    # Add the material to the combo box
                    main_window.materialVal.addItem(sprp_data_entry.data_info.name, sprp_data_entry)
                    main_window.materialModelPartVal.addItem(sprp_data_entry.data_info.name,
                                                             sprp_data_entry.data_info.name_offset)

                # Save the data when is the type SHAP
                elif sprp_type_entry.data_type == b"SHAP":

                    # Move where the actual information starts
                    file.seek(VEV.sprp_file.data_block_base + sprp_data_entry.data_info.data_offset)

                    # Create the SHAP info
                    shap_info = ShapInfo()

                    # Read unk data
                    shap_info.data = file.read(sprp_data_entry.data_info.data_size)

                    # Save the shap_info class in the data of the spr_data_entry
                    sprp_data_entry.data_info.data = shap_info

                # Save the data when is the type VBUF
                elif sprp_type_entry.data_type == b"VBUF":

                    # Move where the actual information starts
                    file.seek(VEV.sprp_file.data_block_base + sprp_data_entry.data_info.data_offset)

                    # Create the VBUF info
                    vbuf_info = VBufInfo()

                    # Read all the data
                    vbuf_info.unk0x00 = file.read(VEV.bytes2Read)
                    vbuf_info.unk0x04 = file.read(VEV.bytes2Read)
                    vbuf_info.data_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    vbuf_info.data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    vbuf_info.vertex_count = int.from_bytes(file.read(VEV.bytes2Read), "big")

                    # If the data_info size of the data_entry for the vbuf is 40, means is a UT/Zenkai Battle character
                    if sprp_data_entry.data_info.data_size == 40:
                        vbuf_info.index_count = int.from_bytes(file.read(VEV.bytes2Read), "big")

                    vbuf_info.unk0x14 = file.read(2)
                    vbuf_info.unk0x16 = file.read(2)
                    vbuf_info.decl_count_0 = int.from_bytes(file.read(2), "big")
                    vbuf_info.decl_count_1 = int.from_bytes(file.read(2), "big")
                    vbuf_info.decl_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")

                    # If the data_info size of the data_entry for the vbuf is 40, means is a UT/Zenkai Battle character
                    if sprp_data_entry.data_info.data_size == 40:
                        vbuf_info.index_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")

                    # Read the vertexDecl
                    file.seek(VEV.sprp_file.data_block_base + vbuf_info.decl_offset)

                    # Read each vertexDecl
                    for _ in range(0, vbuf_info.decl_count_0):
                        # Create the VertexDecl class
                        vertex_decl = VertexDecl()

                        # Read all the data
                        vertex_decl.unk0x00 = file.read(VEV.bytes2Read)
                        vertex_decl.resource_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                        vertex_decl.vertex_usage = int.from_bytes(file.read(2), "big")
                        vertex_decl.index = int.from_bytes(file.read(2), "big")
                        vertex_decl.vertex_format = file.read(2)
                        vertex_decl.stride = int.from_bytes(file.read(2), "big")
                        vertex_decl.offset = int.from_bytes(file.read(VEV.bytes2Read), "big")

                        # Store the name
                        aux_pointer_file_vertex = file.tell()
                        vertex_decl.resource_name, Nothing = get_name_from_file(file, VEV.sprp_file.string_table_base
                                                                                + vertex_decl.resource_name_offset)
                        # Add the effect of the material in the combobox
                        if main_window.effectVal.findText(vertex_decl.resource_name) == -1:
                            main_window.effectVal.addItem(vertex_decl.resource_name, vertex_decl.resource_name_offset)

                        file.seek(aux_pointer_file_vertex)

                        # Store the vertex_decl in the array
                        vbuf_info.vertex_decl.append(vertex_decl)

                    # Save the vbuf_info class in the data of the spr_data_entry
                    sprp_data_entry.data_info.data = vbuf_info

                # Save the data when is the type BONE
                elif sprp_type_entry.data_type == b"BONE":

                    # Move where the actual information starts
                    file.seek(VEV.sprp_file.data_block_base + sprp_data_entry.data_info.data_offset)

                    # Read all the data
                    sprp_data_entry.data_info.data = file.read(sprp_data_entry.data_info.data_size)

                # Save the data when is the type DRVN
                elif sprp_type_entry.data_type == b"DRVN":

                    # Move where the actual information starts
                    file.seek(VEV.sprp_file.data_block_base + sprp_data_entry.data_info.data_offset)

                    # Read all the data
                    sprp_data_entry.data_info.data = file.read(sprp_data_entry.data_info.data_size)

                # Save the data when is the type TXAN
                elif sprp_type_entry.data_type == b'TXAN':

                    # Move where the actual information starts
                    file.seek(VEV.sprp_file.data_block_base + sprp_data_entry.data_info.data_offset)

                    # Read all the data
                    sprp_data_entry.data_info.data = file.read(sprp_data_entry.data_info.data_size)

                    # Add the txan_data_entry to the combo box (material section) but only the name and name_offset
                    main_window.textureVal.addItem(sprp_data_entry.data_info.name,
                                                   sprp_data_entry.data_info.name_offset)

                # Save the data when is the type VSHD
                elif sprp_type_entry.data_type == b'VSHD':

                    # If the spr hold vshd or pshd, we will active the flag
                    if VEV.enable_spr_scratch:
                        VEV.enable_spr_scratch = False

                    # Move where the actual information starts
                    file.seek(VEV.sprp_file.data_block_base + sprp_data_entry.data_info.data_offset)

                    # Create the VSHD info
                    vshd_info = VshdInfo()

                    # Read the data
                    vshd_info.unk0x00 = file.read(12)
                    vshd_info.data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    vshd_info.unk0x10 = file.read(8)
                    file.seek(VEV.sprp_file.data_block_base + sprp_data_entry.data_info.data_offset -
                              vshd_info.data_size)
                    vshd_info.data = file.read(vshd_info.data_size)

                    # Save the vshd_info class in the data of the spr_data_entry
                    sprp_data_entry.data_info.data = vshd_info

                # Save the data when is the type PSHD
                elif sprp_type_entry.data_type == b'PSHD':

                    # If the spr hold vshd or pshd, we will active the flag
                    if VEV.enable_spr_scratch:
                        VEV.enable_spr_scratch = False

                    # Move where the actual information starts
                    file.seek(VEV.sprp_file.data_block_base + sprp_data_entry.data_info.data_offset)

                    # Create the PSHD info
                    pshd_info = PshdInfo()

                    # Read the data
                    pshd_info.unk0x00 = file.read(12)
                    pshd_info.data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    file.seek(VEV.sprp_file.data_block_base + sprp_data_entry.data_info.data_offset -
                              pshd_info.data_size)
                    pshd_info.data = file.read(pshd_info.data_size)

                    # Save the vshd_info class in the data of the spr_data_entry
                    sprp_data_entry.data_info.data = pshd_info

                # Save the data when is the type ANIM
                elif sprp_type_entry.data_type == b"ANIM":

                    # Move where the actual information starts
                    file.seek(VEV.sprp_file.data_block_base + sprp_data_entry.data_info.data_offset)

                    # Read all the data
                    sprp_data_entry.data_info.data = file.read(sprp_data_entry.data_info.data_size)

                # Get all the children sprp_data_info
                if sprp_data_entry.data_info.child_count > 0:
                    read_children(main_window, file, sprp_data_entry.data_info, sprp_data_entry.data_type)

                # Store all the info in the data_entry array
                sprp_type_entry.data_entry.append(sprp_data_entry)

                # Move to the next data_entry
                file.seek(aux_pointer_data_entry)

            # Store the type_entry to the dictionary of type_entries
            VEV.sprp_file.type_entry[sprp_type_entry.data_type] = sprp_type_entry

            file.seek(aux_pointer_type_entry)

            # Update the type_entry offset
            type_entry_offset += sprp_type_entry.data_count * 32

        # Set the unique temp offset value by using the last position of the string table size
        VEV.unique_temp_name_offset = VEV.sprp_file.sprp_header.string_table_size


def open_vram_file(worker_vef, end_progress, vram_path):

    sub_end_progress = end_progress / VEV.sprp_file.type_entry[b'TX2D'].data_count

    with open(vram_path, mode="rb") as file:

        # Get each texture
        header_1 = bytes.fromhex("44 44 53 20 7C 00 00 00 07 10 00 00")
        header_3_1 = "00000000"
        header_3_3 = "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000"
        for i in range(0, VEV.sprp_file.type_entry[b'TX2D'].data_count):

            # Report progress
            worker_vef.progressText.emit("Loading vram: reading texture " + VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.name)
            show_progress_value(worker_vef, sub_end_progress)

            # Creating DXT5 and DXT1 heading
            if VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.dxt_encoding != 0:

                # Get texture first
                file.seek(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.data_offset)
                data = file.read(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.data_size)
                # Check if the spr file is from XBOX 360. We have to unswizzle the texture if that's so
                if VEV.header_type_spr_file == b'SPR3':
                    # Get the unswizzle texture and update the mip_maps and texture size
                    VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.mip_maps, data = \
                        process(data, VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.width,
                                VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.height,
                                VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.mip_maps,
                                VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.dxt_encoding,
                                'unswizzle')
                    # Update the new size of the texture
                    VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.data_size = len(data)

                # Create the header
                header_2 = VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.height.to_bytes(4, 'little')\
                    + VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.width.to_bytes(4, 'little') + \
                    VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.data_size.to_bytes(4, 'little')

                header_3_2 = VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.mip_maps.\
                    to_bytes(4, 'little')

                header_3 = bytes.fromhex(header_3_1) + header_3_2 + bytes.fromhex(header_3_3)

                header_4, header_5, header_6 = create_header(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i]
                                                             .data_info.data.dxt_encoding)
                header = header_1 + header_2 + header_3 + header_4 + header_5 + header_6

                # Store header and texture data in memory
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.tx2d_vram.data = header + data

            # Creating RGBA heading
            else:

                # Create RGBA header
                header_1_bmp = "42 4D"
                header_2_bmp = (VEV.sprp_file.type_entry[b'TX2D'].data_entry[i]
                                .data_info.data.data_size + 54).to_bytes(4, 'little').hex()
                header_3_bmp = "00 00 00 00 36 00 00 00 28 00 00 00"
                header_4_1_bmp = VEV.sprp_file.type_entry[b'TX2D'].data_entry[i]\
                    .data_info.data.width.to_bytes(4, 'little').hex()
                header_4_2_bmp = VEV.sprp_file.type_entry[b'TX2D'].data_entry[i]\
                    .data_info.data.height.to_bytes(4, 'little').hex()
                header_4_bmp = header_4_1_bmp + header_4_2_bmp
                header_5_bmp = "01 00 20 00 00 00 00 00 00 00 00 00 12 0B 00 00 12 0B 00 00 00 00 00 00 00 00 00 00"
                header = bytes.fromhex(header_1_bmp + header_2_bmp + header_3_bmp + header_4_bmp + header_5_bmp)

                # Get the texture
                file.seek(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.data_offset)
                data = file.read(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.data_size)
                # We're dealing with a shader
                if VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.height == 1:
                    data = change_endian(data)
                # Store header and texture
                VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.tx2d_vram.data = header + data

                # Check if the extension is png, to unswizzle the image
                if VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.extension == "png":

                    # Write in disk the data swizzled
                    with open("tempSwizzledImage", mode="wb") as file_temp:
                        file_temp.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.tx2d_vram.data)

                    # Run the exe file of 'swizzle.exe' with the option '-u' to unswizzle the image
                    args = os.path.join(VEV.swizzle_path) + " \"" + "tempSwizzledImage" + "\" \"" + "-u" + "\""
                    os.system('cmd /c ' + args)

                    # Get the data from the .exe
                    with open("tempUnSwizzledImage", mode="rb") as file_temp:
                        VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info\
                            .data.tx2d_vram.data_unswizzle = file_temp.read()
                    with open("Indexes.txt", mode="r") as file_temp:
                        VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data.tx2d_vram\
                            .indexes_unswizzle_algorithm = file_temp.read().split(";")[:-1]
                        # [:-1] because swizzle.exe saves an '' element in the end

                    # Remove the temp files
                    os.remove("tempSwizzledImage")
                    os.remove("tempUnSwizzledImage")
                    os.remove("Indexes.txt")

                    VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info.data\
                        .tx2d_vram.data_unswizzle = header + VEV.sprp_file.type_entry[b'TX2D'].data_entry[i].data_info\
                        .data.tx2d_vram.data_unswizzle


def generate_tx2d_entry(worker_vef, step_report, main_window, vram_path_modified, entry_info, entry_info_size, entry_count,
                        string_table, string_table_size, string_name_offset, data_entry, data_entry_size, data, data_size, data_offset,
                        vram_separator, num_textures, num_material, special_names_dict):

    with open(vram_path_modified, mode="wb") as output_vram_file:

        # Get each data_entry (TX2D) and store the texture properties
        sub_step_report = step_report / num_textures
        for i in range(0, num_textures):

            # Get the texture from the tool
            tx2d_data_entry = main_window.listView.model().item(i, 0).data()

            # Get the tx2d info
            tx2d_info = tx2d_data_entry.data_info.data

            # Report progress
            worker_vef.progressText.emit("Saving vram: writting texture " + tx2d_data_entry.data_info.name)
            show_progress_value(worker_vef, sub_step_report)

            # Store the offset where the texture will be located in vram
            texture_offset = output_vram_file.tell()

            # Store some texture properties that can differ
            mip_maps = tx2d_info.mip_maps
            texture_data_size = tx2d_info.data_size
            related_2_encoding = tx2d_info.related_2_encoding

            # Write the textures in the vram file
            # It's a DDS image
            if tx2d_info.dxt_encoding != 0:
                # Check if the spr file is from XBOX 360. We have to swizzle if that's so
                if VEV.header_type_spr_file != b'SPR3':
                    data_texture = tx2d_info.tx2d_vram.data[128:]
                else:
                    # Swizzle the texture for Xbox.
                    # As a temporay fix, we use only 1 mipmaps and store the data size of the swizzled texture
                    mip_maps, data_texture = process(tx2d_info.tx2d_vram.data[128:], tx2d_info.width, tx2d_info.height,
                                                     1, tx2d_info.dxt_encoding, 'swizzle')
                    texture_data_size = len(data_texture)
                output_vram_file.write(data_texture)
                # Write the vram separator
                if vram_separator and i < num_textures - 1:
                    write_separator_vram(output_vram_file, tx2d_data_entry)
            # It's a BMP image
            else:

                if tx2d_data_entry.data_info.extension != "png":
                    # We're dealing with a shader. We have to change the endian
                    if tx2d_info.height == 1:
                        # Since is a shader, it if is for a Xbox file, we need to change the 'related2encoding' value
                        # Otherwise will make the character with black shaders
                        if VEV.header_type_spr_file == b'SPR3':
                            related_2_encoding = 130
                        output_vram_file.write(change_endian(tx2d_info.tx2d_vram.data[54:]))
                    else:
                        output_vram_file.write(tx2d_info.tx2d_vram.data[54:])
                else:
                    # Write in disk the data swizzled
                    with open("tempSwizzledImage", mode="wb") as file:
                        file.write(tx2d_info.tx2d_vram.data)

                    # Write in disk the data unswizzled
                    with open("tempUnSwizzledImage", mode="wb") as file:
                        file.write(tx2d_info.tx2d_vram.data_unswizzle[54:])

                    # Write in disk the indexes
                    with open("Indexes.txt", mode="w") as file:
                        for index in tx2d_info.tx2d_vram. \
                                indexes_unswizzle_algorithm:
                            file.write(index + ";")

                    # Run the exe file of 'swizzle.exe'
                    # with the option '-s' to swizzle the image
                    args = os.path.join(VEV.swizzle_path) + " \"" + \
                        "tempSwizzledImage" + "\" \"" + \
                        "tempUnSwizzledImage" + "\" \"" + "Indexes.txt" + "\" \"" + "-s" + \
                        "\""
                    os.system('cmd /c ' + args)

                    # Get the data from the .exe and write it into the vram
                    with open("tempSwizzledImageModified", mode="rb") as file:
                        output_vram_file.write(file.read())

                    # Remove the temp files
                    os.remove("tempSwizzledImage")
                    os.remove("tempUnSwizzledImage")
                    os.remove("Indexes.txt")
                    os.remove("tempSwizzledImageModified")

            # Write the name for each texture in the spr
            name = tx2d_data_entry.data_info.name + "." + \
                tx2d_data_entry.data_info.extension
            string_table += b'\x00' + name.encode('utf-8')
            string_table_size += 1 + len(name)

            # Write the data_entry for each texture
            data_entry += tx2d_data_entry.data_type
            data_entry += i.to_bytes(4, 'big')
            tx2d_data_entry.data_info.new_name_offset = string_name_offset
            data_entry += tx2d_data_entry.data_info.new_name_offset.to_bytes(4, 'big')
            data_entry += data_offset.to_bytes(4, 'big')
            data_entry += tx2d_data_entry.data_info.data_size.to_bytes(4, 'big')
            data_entry += tx2d_data_entry.data_info.child_count.to_bytes(4, 'big')
            # We write the child offset later

            # Write the data for each texture
            data += related_2_encoding.to_bytes(4, 'big')
            data += texture_offset.to_bytes(4, 'big')
            data += tx2d_info.unk0x08.to_bytes(4, 'big')
            data += texture_data_size.to_bytes(4, 'big')
            data += tx2d_info.width.to_bytes(2, 'big')
            data += tx2d_info.height.to_bytes(2, 'big')
            data += tx2d_info.unk0x14.to_bytes(2, 'big')
            data += mip_maps.to_bytes(2, 'big')
            data += tx2d_info.unk0x18.to_bytes(4, 'big')
            data += tx2d_info.unk0x1c.to_bytes(4, 'big')
            data += tx2d_info.dxt_encoding.to_bytes(1, 'big')
            data += b'\00\00\00'
            data_size += tx2d_data_entry.data_info.data_size

            # Write children (if any)
            if tx2d_data_entry.data_info.child_count > 0:
                string_table_child, string_table_child_size, string_name_offset, \
                    data_child, data_child_size, data_offset = \
                    write_children(main_window, num_material, num_textures,
                                   tx2d_data_entry.data_info, b'TX2D',
                                   string_table_size + 1, data_size, special_names_dict)

                # Update the string_name and string_table_size
                string_table += string_table_child
                string_table_size += string_table_child_size

                # Update the data and data_size
                data += data_child
                data_size += data_child_size

                # Write in the data entry, the children offset
                data_entry += data_offset.to_bytes(4, 'big')
            else:
                # Child offset
                data_entry += b'\x00\x00\x00\x00'
            data_entry += b'\x00\x00\x00\x00'
            data_entry_size += 32

            # Check if the data, the module of 16 is 0
            data, data_size, padding_size = check_entry_module(data, data_size, 16)

            # Update offsets for the next entry
            string_name_offset = 1 + string_table_size
            data_offset = data_size

        # Get the new vram size by getting the position of the pointer in the output file
        # since it's in the end of the file
        vram_data_size = output_vram_file.tell()

    # Update the entry info
    entry_info += b'TX2D' + b'\x00\x01\x00\x00' + num_textures.to_bytes(4, 'big')
    # Update the sizes
    entry_count += 1
    entry_info_size += 12

    return entry_info, entry_info_size, entry_count, string_table, string_table_size, string_name_offset, data_entry, \
        data_entry_size, data, data_size, data_offset, vram_data_size


def read_children(main_window, file, sprp_data_info, type_section):

    file.seek(sprp_data_info.child_offset + VEV.sprp_file.data_block_base)

    for _ in range(sprp_data_info.child_count):
        sprp_data_info_child = SprpDataInfo()

        sprp_data_info_child.name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
        sprp_data_info_child.data_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
        sprp_data_info_child.data_size = int.from_bytes(file.read(VEV.bytes2Read), "big")
        sprp_data_info_child.child_count = int.from_bytes(file.read(VEV.bytes2Read), "big")
        sprp_data_info_child.child_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")

        # Get the name for the data_info
        aux_pointer_file = file.tell()
        sprp_data_info_child.name, sprp_data_info_child.extension = \
            get_name_from_file(file, VEV.sprp_file.string_table_base + sprp_data_info_child.name_offset)
        base_name_size = len(sprp_data_info_child.name)
        extension_size = len(sprp_data_info_child.extension)
        sprp_data_info_child.name_size = 1 + base_name_size + (extension_size + 1 if extension_size > 0 else 0)

        # Get the texture data
        if type_section == b'TX2D':

            # Move where the data starts
            file.seek(sprp_data_info_child.data_offset + VEV.sprp_file.data_block_base)

            # Store the data
            sprp_data_info_child.data = file.read(sprp_data_info_child.data_size)

        # Get the material data
        elif type_section == b'MTRL':

            # Move where the info starts
            file.seek(sprp_data_info_child.data_offset + VEV.sprp_file.data_block_base)

            # Save the data of the children from a material in the mtrl_prop var (Raging Blast 2 material)
            if sprp_data_info_child.data_size == VEV.rb2_material_child_size:
                mtrl_prop = MtrlProp()
                mtrl_prop.Ilumination_Shadow_orientation = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Ilumination_Light_orientation_glow = struct.unpack('>f', file.read(4))[0]
                for i in range(len(mtrl_prop.unk0x04)):
                    mtrl_prop.unk0x04[i] = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Brightness_purple_light_glow = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Saturation_glow = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Saturation_base = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Brightness_toonmap_active_some_positions = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Brightness_toonmap = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Brightness_toonmap_active_other_positions = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Brightness_incandescence_active_some_positions = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Brightness_incandescence = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Brightness_incandescence_active_other_positions = struct.unpack('>f', file.read(4))[0]
                for i in range(len(mtrl_prop.Border_RGBA)):
                    mtrl_prop.Border_RGBA[i] = struct.unpack('>f', file.read(4))[0]
                for i in range(len(mtrl_prop.unk0x44)):
                    mtrl_prop.unk0x44[i] = struct.unpack('>f', file.read(4))[0]
                for i in range(len(mtrl_prop.unk0x50)):
                    mtrl_prop.unk0x50[i] = struct.unpack('>f', file.read(4))[0]
            else:
                mtrl_prop = file.read(sprp_data_info_child.data_size)

            sprp_data_info_child.data = mtrl_prop

        # Get the shape data
        elif type_section == b'SHAP':

            # Move where the info starts
            file.seek(sprp_data_info_child.data_offset + VEV.sprp_file.data_block_base)

            # Save the info of the material children in the shap_info var
            shap_info = ShapInfo()

            # Get the data when is DBZEdgeInfo
            if sprp_data_info_child.name == "DbzEdgeInfo":

                # Save the data
                shap_info.data = file.read(64)
                shap_info.source_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                shap_info.type_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                shap_info.unk0x48 = file.read(VEV.bytes2Read)

                # Store the names
                aux_pointer_file_shap = file.tell()
                shap_info.type_name, Nothing = get_name_from_file(file, VEV.sprp_file.string_table_base
                                                                  + shap_info.type_offset)
                # Add the effect of the material in the combobox
                if main_window.effectVal.findText(shap_info.type_name) == -1:
                    main_window.effectVal.addItem(shap_info.type_name, shap_info.type_offset)

                file.seek(aux_pointer_file_shap)

            # Get all the data if is everything else
            else:
                # Save the data
                shap_info.data = file.read(sprp_data_info_child.data_size)

            # Save the shapInfo class in the data of the children
            sprp_data_info_child.data = shap_info

        # Get the scene data
        elif type_section == b'SCNE':

            # If the parent name is NODES, we store the scene model in the child data
            if sprp_data_info.name == "[NODES]":
                file.seek(VEV.sprp_file.data_block_base + sprp_data_info_child.data_offset)

                scne_model = ScneModel()
                scne_model.unk00 = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_model.type_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_model.name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_model.layer_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_model.parent_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")

                # Store the names
                aux_pointer_file_scne = file.tell()
                scne_model.type_name, Nothing = get_name_from_file(file, VEV.sprp_file.string_table_base +
                                                                   scne_model.type_offset)
                scne_model.name_name, Nothing = get_name_from_file(file, VEV.sprp_file.string_table_base +
                                                                   scne_model.name_offset)
                scne_model.layer_name, Nothing = get_name_from_file(file, VEV.sprp_file.string_table_base +
                                                                    scne_model.layer_offset)
                scne_model.parent_name, Nothing = get_name_from_file(file, VEV.sprp_file.string_table_base +
                                                                     scne_model.parent_offset)
                file.seek(aux_pointer_file_scne)

                sprp_data_info_child.data = scne_model

            # If the children name is MATERIAL, we store the scene material in the child data
            elif sprp_data_info_child.name == "[MATERIAL]":
                file.seek(VEV.sprp_file.data_block_base + sprp_data_info_child.data_offset)

                scne_material = ScneMaterial()

                scne_material.name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_material.unk04 = int.from_bytes(file.read(VEV.bytes2Read), "big")
                scne_material.material_info_count = int.from_bytes(file.read(VEV.bytes2Read), "big")

                # Search first the material that this scene is using currently
                found_material = False
                layers = []
                for i in range(main_window.materialVal.count()):
                    mtrl_data_info = main_window.materialVal.itemData(i).data_info
                    if scne_material.name_offset == mtrl_data_info.name_offset:
                        found_material = True
                        layers = mtrl_data_info.data.layers
                        break

                # Store the scne material
                for _ in range(0, scne_material.material_info_count):
                    scne_materia_info = ScneMaterialInfo()

                    scne_materia_info.name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    scne_materia_info.type_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    scne_materia_info.unk08 = int.from_bytes(file.read(VEV.bytes2Read), "big")

                    # Store the name of the type
                    aux_pointer_file_scne = file.tell()
                    scne_materia_info.type_name, nothing = get_name_from_file(file,
                                                                              VEV.sprp_file.string_table_base +
                                                                              scne_materia_info.type_offset)
                    # Add the effect of the material in the combobox. Some effects only can be found in the scene section
                    if main_window.effectVal.findText(scne_materia_info.type_name) == -1:
                        main_window.effectVal.addItem(scne_materia_info.type_name, scne_materia_info.type_offset)

                    file.seek(aux_pointer_file_scne)

                    # Assign to the layer from the material that this scne is using, the effect for that layer
                    if found_material:
                        for i in range(0, 10):
                            mtrl_layer = layers[i]
                            if mtrl_layer.layer_name_offset == scne_materia_info.name_offset:
                                # Store the name of the effect
                                mtrl_layer.effect_name = scne_materia_info.type_name
                                break

                    scne_material.material_info.append(scne_materia_info)

                sprp_data_info_child.data = scne_material

                # Store in the combo box, the sprp_data_info children using as a key, the father's name
                main_window.modelPartVal.addItem(sprp_data_info.name, sprp_data_info_child)

            # If the children name is DbzEyeInfo, we store the scene eye info in the child data
            elif sprp_data_info_child.name == "DbzEyeInfo":
                file.seek(VEV.sprp_file.data_block_base + sprp_data_info_child.data_offset)

                scne_eye_info = ScneEyeInfo()

                # Get each eye_data
                for _ in range(0, 3):
                    eye_data = EyeData()
                    eye_data.unk00_name_offset = int.from_bytes(file.read(VEV.bytes2Read), "big")
                    eye_data.unk04 = file.read(108)

                    scne_eye_info.eyes_data.append(eye_data)

                sprp_data_info_child.data = scne_eye_info

            # By default, we store the unknown info
            else:
                file.seek(VEV.sprp_file.data_block_base + sprp_data_info_child.data_offset)

                sprp_data_info_child.data = file.read(sprp_data_info_child.data_size)

        # Get the bone data
        elif type_section == b'BONE':
            # Move where the data starts
            file.seek(sprp_data_info_child.data_offset + VEV.sprp_file.data_block_base)

            # Store the data
            sprp_data_info_child.data = file.read(sprp_data_info_child.data_size)

        # Restore the pointer of the file in order to read the following children
        file.seek(aux_pointer_file)

        # Get all the children sprp_data_info for the actual children in the loop section
        if sprp_data_info_child.child_count > 0:
            read_children(main_window, file, sprp_data_info_child, type_section)
            file.seek(aux_pointer_file)

        # Store each children to the array
        sprp_data_info.child_info.append(sprp_data_info_child)


def write_children(main_window, num_material, num_textures, data_info_parent, type_entry, string_name_offset,
                   data_size, special_names):

    string_table_child = b''
    string_table_child_size = 0
    name_offset = 0
    data_child, data_child_offset_section = b'', b''
    data_child_size, data_child_offset_section_size = 0, 0
    data_offset = data_size
    data_offset_children = 0

    for i in range(0, data_info_parent.child_count):

        # Get the child
        data_info_child = data_info_parent.child_info[i]

        # The type entry is tx2d
        if type_entry == b'TX2D':

            # Write the name. If it doesn't exists, we create it
            if data_info_child.name_offset != 0:
                if data_info_child.name in special_names:
                    name_offset = special_names[data_info_child.name]
                else:
                    special_names[data_info_child.name] = string_name_offset
                    name_offset = string_name_offset
                    string_table_child += b'\x00' + data_info_child.name.encode('utf-8')
                    string_name_size = 1 + len(data_info_child.name)
                    # Update the offset
                    string_table_child_size += string_name_size
                    string_name_offset += string_name_size
            else:
                name_offset = 0

            # Write the data
            data_child += data_info_child.data

        # The type entry is material
        elif type_entry == b'MTRL':

            # Get the material properties
            mtrl_prop = data_info_child.data

            # Write the data
            # Raging Blast 2 material children
            if data_info_child.data_size == VEV.rb2_material_child_size:
                data_child += struct.pack('>f', mtrl_prop.Ilumination_Shadow_orientation)
                data_child += struct.pack('>f', mtrl_prop.Ilumination_Light_orientation_glow)
                for j in range(len(mtrl_prop.unk0x04)):
                    data_child += struct.pack('>f', mtrl_prop.unk0x04[j])
                data_child += struct.pack('>f', mtrl_prop.Brightness_purple_light_glow)
                data_child += struct.pack('>f', mtrl_prop.Saturation_glow)
                data_child += struct.pack('>f', mtrl_prop.Saturation_base)
                data_child += \
                    struct.pack('>f', mtrl_prop.Brightness_toonmap_active_some_positions)
                data_child += struct.pack('>f', mtrl_prop.Brightness_toonmap)
                data_child += \
                    struct.pack('>f', mtrl_prop.Brightness_toonmap_active_other_positions)
                data_child += \
                    struct.pack('>f', mtrl_prop.Brightness_incandescence_active_some_positions)
                data_child += struct.pack('>f', mtrl_prop.Brightness_incandescence)
                data_child += \
                    struct.pack('>f', mtrl_prop.Brightness_incandescence_active_other_positions)
                for j in range(len(mtrl_prop.Border_RGBA)):
                    data_child += struct.pack('>f', mtrl_prop.Border_RGBA[j])
                for j in range(len(mtrl_prop.unk0x44)):
                    data_child += struct.pack('>f', mtrl_prop.unk0x44[j])
                for j in range(len(mtrl_prop.unk0x50)):
                    data_child += struct.pack('>f', mtrl_prop.unk0x50[j])
            else:
                data_child += mtrl_prop

            # Write the name DbzCharMtrl. If it doesn't exists, we create it
            if data_info_child.name != "":
                if data_info_child.name in special_names:
                    name_offset = special_names[data_info_child.name]
                else:
                    special_names[data_info_child.name] = string_name_offset
                    name_offset = string_name_offset
                    string_table_child += b'\x00' + data_info_child.name.encode('utf-8')
                    string_name_size = 1 + len(data_info_child.name)
                    # Update the offset
                    string_table_child_size += string_name_size
                    string_name_offset += string_name_size
            else:
                name_offset = 0

        # The type entry is shape
        elif type_entry == b'SHAP':

            shap_info = data_info_child.data

            # Write the data
            if data_info_parent.child_count > 1:
                # DbzEdgeInfo
                if data_info_child.data_size == 76:
                    data_child += shap_info.data

                    # If the DbzEdgeInfo child is using a texture, we'll try to find it
                    if shap_info.source_name_offset != 0:
                        found, data_child = search_texture(main_window, data_child, shap_info.source_name_offset,
                                                           num_textures)
                        if not found:
                            data_child += b'\x00\x00\x00\x00'
                    else:
                        data_child += b'\x00\x00\x00\x00'

                    # Check if this shape has a type assigned. We won't assign anything if originally the
                    # shape didn't have a type assigned
                    # Get the new offset for this layer effect
                    if shap_info.type_name != "":
                        if shap_info.type_name in special_names:
                            data_child += special_names[shap_info.type_name].to_bytes(4, 'big')
                        else:
                            special_names[shap_info.type_name] = string_name_offset
                            data_child += special_names[shap_info.type_name].to_bytes(4, 'big')
                            string_table_child += b'\x00' + shap_info.type_name.encode('utf-8')
                            string_name_size = 1 + len(shap_info.type_name)
                            # Update the offset
                            string_table_child_size += string_name_size
                            string_name_offset += string_name_size
                    else:
                        data_child += b'\x00\x00\x00\x00'

                    data_child += shap_info.unk0x48
                # DbzShapeInfo
                else:
                    data_child += shap_info.data
            else:
                data_child += shap_info.data

            # Write the name DbzEdgeInfo or DbzShapeInfo. If it doesn't exists, we create it
            if data_info_child.name_offset != 0:
                if data_info_child.name in special_names:
                    name_offset = special_names[data_info_child.name]
                else:
                    special_names[data_info_child.name] = string_name_offset
                    name_offset = string_name_offset
                    string_table_child += b'\x00' + data_info_child.name.encode('utf-8')
                    string_name_size = 1 + len(data_info_child.name)
                    # Update the offset
                    string_table_child_size += string_name_size
                    string_name_offset += string_name_size
            else:
                name_offset = 0

        # The type entry is scene
        elif type_entry == b'SCNE':

            # Assign the name offset for each children and write the data
            # [LAYERS] children
            if data_info_parent.name == "[LAYERS]":
                # Add to a dictionary, the special names but only if they weren't added before
                if data_info_child.name_offset != 0 and data_info_child.name not in special_names:
                    special_names[data_info_child.name] = string_name_offset
                    name_offset = string_name_offset
                    string_table_child += b'\x00' + data_info_child.name.encode('utf-8')
                    string_name_size = 1 + len(data_info_child.name)
                    # Update the offset
                    string_table_child_size += string_name_size
                    string_name_offset += string_name_size

            # [NODES] children
            elif data_info_parent.name == "[NODES]":

                # Get the scne model
                scne_model = data_info_child.data

                # Write the unk data
                data_child += scne_model.unk00.to_bytes(4, 'big')

                # Write the type
                if scne_model.type_offset != 0:
                    if scne_model.type_name not in special_names:
                        special_names[scne_model.type_name] = string_name_offset
                        string_table_child += b'\x00' + scne_model.type_name.encode('utf-8')
                        string_name_size = 1 + len(scne_model.type_name)
                        # Update the offset
                        string_table_child_size += string_name_size
                        string_name_offset += string_name_size
                    data_child += special_names[scne_model.type_name].to_bytes(4, 'big')
                else:
                    data_child += b'\x00\x00\x00\x00'

                # The type scene is a mesh
                if scne_model.type_name == 'mesh':

                    # Write the name
                    # Search the VBUF that is related to this SCNE and write the new calculated offset
                    found = False
                    vbuf_type_entry = VEV.sprp_file.type_entry[b'VBUF']
                    for j in range(0, vbuf_type_entry.data_count):
                        # Get the data entry for the VBUF
                        vbuf_data_entry = vbuf_type_entry.data_entry[j]
                        if vbuf_data_entry.data_info.name_offset == scne_model.name_offset:
                            # Write the vbuf new name offset that we found
                            data_child += vbuf_data_entry.data_info.new_name_offset.to_bytes(4, 'big')
                            found = True
                            break
                    # If doesn't find anything, we append an empty offset
                    if not found:
                        data_child += b'\x00\x00\x00\x00'

                    # Update the material offset that the current scne is using
                    scne_material = data_info_child.child_info[0].data
                    for j in range(0, num_material):
                        # Search what material is currently using the actual scene node. We will use the materials that are stored from the tool
                        mtrl_data_entry = main_window.materialVal.itemData(j)
                        if mtrl_data_entry.data_info.name_offset == scne_material.name_offset:

                            # Update the scne material offsets
                            scne_material.new_name_offset = mtrl_data_entry.data_info.new_name_offset
                            scne_material.name = mtrl_data_entry.data_info.name

                            # Update the scne material info
                            scne_material.material_info = []
                            material_info_count = 0
                            for layer in mtrl_data_entry.data_info.data.layers:
                                # We only add to the scene the layers that has a name and effect added
                                if layer.layer_name != "" and layer.effect_name != "":
                                    scne_material_info = ScneMaterialInfo()

                                    # Get the new offset type for this layer
                                    scne_material_info.name_offset = special_names[layer.layer_name]

                                    # Get the new offset for this layer effect. Some layer effects could be only used in the scne section, so if the offset of the used effect is not calculated
                                    # previously, we calculate it and add it to the string table
                                    if layer.effect_name not in special_names:
                                        special_names[layer.effect_name] = string_name_offset
                                        string_table_child += b'\x00' + layer.effect_name.encode('utf-8')
                                        string_name_size = 1 + len(layer.effect_name)
                                        # Update the offset
                                        string_table_child_size += string_name_size
                                        string_name_offset += string_name_size
                                    scne_material_info.type_offset = special_names[layer.effect_name]

                                    scne_material_info.unk08 = 0
                                    scne_material.material_info.append(scne_material_info)
                                    material_info_count += 1

                            scne_material.material_info_count = material_info_count

                            break

                    # Write the layer name offset but only when originally there was data
                    if scne_model.layer_offset != 0:
                        if scne_model.layer_name in special_names:
                            name_offset = special_names[scne_model.layer_name]
                        else:
                            special_names[scne_model.layer_name] = string_name_offset
                            name_offset = string_name_offset
                            string_table_child += b'\x00' + scne_model.layer_name.encode('utf-8')
                            string_name_size = 1 + len(scne_model.layer_name)
                            # Update the offset
                            string_table_child_size += string_name_size
                            string_name_offset += string_name_size
                    else:
                        name_offset = 0
                    data_child += name_offset.to_bytes(4, 'big')

                    # Search if the scne_model parent is already in the string table, buy only when it has originally
                    # a parent
                    if scne_model.parent_offset != 0:
                        found, name_offset, data_info_child_2 = check_name_is_string_table(i, scne_model,
                                                                                           data_info_parent)
                        # The parent name value is not in the string table
                        if not found:
                            # Write the name of the parent value
                            name_offset = string_name_offset
                            string_table_child += b'\x00' + scne_model.parent_name.encode('utf-8')
                            string_name_size = 1 + len(scne_model.parent_name)
                            string_table_child_size += string_name_size
                            string_name_offset += string_name_size

                            # Update the other child we have found if the parent name value and the main name of the
                            # other child is the same
                            if scne_model.parent_offset == data_info_child_2.name_offset:
                                data_info_child_2.name_offset_calculated = True
                                data_info_child_2.new_name_offset = name_offset
                    else:
                        name_offset = 0
                    data_child += name_offset.to_bytes(4, 'big')

                    # Write the name offset with the new material
                    if data_info_child.name_offset_calculated:
                        name_offset = data_info_child.new_name_offset
                    else:
                        new_name = scne_model.parent_name + ":" + scne_material.name
                        name_offset = string_name_offset
                        string_table_child += b'\x00' + new_name.encode('utf-8')
                        string_name_size = 1 + len(new_name)
                        string_table_child_size += string_name_size
                        string_name_offset += string_name_size

                # The type scene is a shape
                elif scne_model.type_name == 'shape':

                    # Write the name
                    # Search the SHAP that is related to this SCNE and write the new calculated offset
                    found = False
                    shap_type_entry = VEV.sprp_file.type_entry[b'SHAP']
                    for j in range(0, shap_type_entry.data_count):
                        # Get the data entry for the SHAP
                        shap_data_entry = shap_type_entry.data_entry[j]
                        if shap_data_entry.data_info.name_offset == scne_model.name_offset:
                            # Write the shap new name offset that we found
                            data_child += shap_data_entry.data_info.new_name_offset.to_bytes(4, 'big')
                            found = True
                            break
                    # If doesn't find anything, we append an empty offset
                    if not found:
                        data_child += b'\x00\x00\x00\x00'

                    # Write the layer name offset but only when originally there was data
                    if scne_model.layer_offset != 0:
                        if scne_model.layer_name in special_names:
                            name_offset = special_names[scne_model.layer_name]
                        else:
                            special_names[scne_model.layer_name] = string_name_offset
                            name_offset = string_name_offset
                            string_table_child += b'\x00' + scne_model.layer_name.encode('utf-8')
                            string_name_size = 1 + len(scne_model.layer_name)
                            # Update the offset
                            string_table_child_size += string_name_size
                            string_name_offset += string_name_size
                    else:
                        name_offset = 0
                    data_child += name_offset.to_bytes(4, 'big')

                    # Search if the scne_model parent is already in the string table, buy only when it has originally
                    # a parent
                    if scne_model.parent_offset != 0:
                        found, name_offset, data_info_child_2 = check_name_is_string_table(i, scne_model,
                                                                                           data_info_parent)
                        # The parent name value is not in the string table
                        if not found:
                            # Write the name of the parent value
                            name_offset = string_name_offset
                            string_table_child += b'\x00' + scne_model.parent_name.encode('utf-8')
                            string_name_size = 1 + len(scne_model.parent_name)
                            string_table_child_size += string_name_size
                            string_name_offset += string_name_size

                            # Update the other child we have found if the parent name value and the main name of the
                            # other child is the same
                            if scne_model.parent_offset == data_info_child_2.name_offset:
                                data_info_child_2.name_offset_calculated = True
                                data_info_child_2.new_name_offset = name_offset
                    else:
                        name_offset = 0
                    data_child += name_offset.to_bytes(4, 'big')

                    # Write the name offset with the new material
                    if data_info_child.name_offset_calculated:
                        name_offset = data_info_child.new_name_offset
                    else:
                        name_offset = string_name_offset
                        string_table_child += b'\x00' + data_info_child.name.encode('utf-8')
                        string_name_size = 1 + len(data_info_child.name)
                        string_table_child_size += string_name_size
                        string_name_offset += string_name_size

                # Default (transform, camera)
                else:

                    # Write the name but only when originally there was data
                    if scne_model.name_offset != 0:
                        if scne_model.name_name in special_names:
                            name_offset = special_names[scne_model.name_name]
                        else:
                            special_names[scne_model.name_name] = string_name_offset
                            name_offset = string_name_offset
                            string_table_child += b'\x00' + scne_model.name_name.encode('utf-8')
                            string_name_size = 1 + len(scne_model.name_name)
                            # Update the offset
                            string_table_child_size += string_name_size
                            string_name_offset += string_name_size
                    else:
                        name_offset = 0
                    data_child += name_offset.to_bytes(4, 'big')

                    # Write the layer name offset but only when originally there was data
                    if scne_model.layer_offset != 0:
                        if scne_model.layer_name in special_names:
                            name_offset = special_names[scne_model.layer_name]
                        else:
                            special_names[scne_model.layer_name] = string_name_offset
                            name_offset = string_name_offset
                            string_table_child += b'\x00' + scne_model.layer_name.encode('utf-8')
                            string_name_size = 1 + len(scne_model.layer_name)
                            # Update the offset
                            string_table_child_size += string_name_size
                            string_name_offset += string_name_size
                    else:
                        name_offset = 0
                    data_child += name_offset.to_bytes(4, 'big')

                    # Search if the scne_model parent is already in the string table, buy only when it has originally
                    # a parent
                    if scne_model.parent_offset != 0:
                        found, name_offset, data_info_child_2 = check_name_is_string_table(i, scne_model,
                                                                                           data_info_parent)
                        # The parent name value is not in the string table
                        if not found:
                            # Write the name of the parent value
                            name_offset = string_name_offset
                            string_table_child += b'\x00' + scne_model.parent_name.encode('utf-8')
                            string_name_size = 1 + len(scne_model.parent_name)
                            string_table_child_size += string_name_size
                            string_name_offset += string_name_size

                            # Update the other child we have found if the parent name value and the main name of the
                            # other child is the same
                            if scne_model.parent_offset == data_info_child_2.name_offset:
                                data_info_child_2.name_offset_calculated = True
                                data_info_child_2.new_name_offset = name_offset
                    else:
                        name_offset = 0
                    data_child += name_offset.to_bytes(4, 'big')

                    # Write the name offset with the new material
                    if data_info_child.name_offset_calculated:
                        name_offset = data_info_child.new_name_offset
                    else:
                        name_offset = string_name_offset
                        string_table_child += b'\x00' + data_info_child.name.encode('utf-8')
                        string_name_size = 1 + len(data_info_child.name)
                        string_table_child_size += string_name_size
                        string_name_offset += string_name_size

            # [MATERIAL] children
            elif data_info_child.name == "[MATERIAL]":

                # Write the data
                scne_material = data_info_child.data
                data_child += scne_material.new_name_offset.to_bytes(4, 'big')
                data_child += scne_material.unk04.to_bytes(4, 'big')
                data_child += scne_material.material_info_count.to_bytes(4, 'big')
                data_info_child.data_size = 12
                for j in range(0, scne_material.material_info_count):
                    scene_material_info = scne_material.material_info[j]

                    data_child += scene_material_info.name_offset.to_bytes(4, 'big')
                    data_child += scene_material_info.type_offset.to_bytes(4, 'big')
                    data_child += scene_material_info.unk08.to_bytes(4, 'big')

                    # Update the new size
                    data_info_child.data_size += 12

                # Write the name [MATERIAL]. If it doesn't exists, we create it
                if data_info_child.name in special_names:
                    name_offset = special_names[data_info_child.name]
                else:
                    special_names[data_info_child.name] = string_name_offset
                    name_offset = string_name_offset
                    string_table_child += b'\x00' + data_info_child.name.encode('utf-8')
                    string_name_size = 1 + len(data_info_child.name)
                    # Update the offset
                    string_table_child_size += string_name_size
                    string_name_offset += string_name_size

            # [LAYERS], [NODES], [TRANSFORM] or DbzEdgeInfo
            else:

                # Add a padding of zeros before writting the data
                data_child, n, padding_size = check_entry_module(data_child, data_offset, 16)
                data_child_size += padding_size
                data_offset += padding_size

                # Write the data when is DbzEyeInfo
                if data_info_child.name == "DbzEyeInfo":

                    # Write the data
                    scne_eye_info = data_info_child.data
                    num_eyes_info = int(data_info_child.data_size / 112)
                    for j in range(0, num_eyes_info):
                        eye_data = scne_eye_info.eyes_data[j]
                        if j == 0:
                            if "EYEBALL_R" not in special_names:
                                special_names["EYEBALL_R"] = string_name_offset
                                string_table_child += b'\x00' + "EYEBALL_R".encode('utf-8')
                                string_name_size = 1 + len("EYEBALL_R")
                                # Update the offset
                                string_table_child_size += string_name_size
                                string_name_offset += string_name_size
                            special_name_offset = special_names["EYEBALL_R"]
                        elif j == 1:
                            if "EYEBALL_L" not in special_names:
                                special_names["EYEBALL_L"] = string_name_offset
                                string_table_child += b'\x00' + "EYEBALL_L".encode('utf-8')
                                string_name_size = 1 + len("EYEBALL_L")
                                # Update the offset
                                string_table_child_size += string_name_size
                                string_name_offset += string_name_size
                            special_name_offset = special_names["EYEBALL_L"]
                        else:
                            special_name_offset = 0
                        data_child += special_name_offset.to_bytes(4, 'big')
                        data_child += eye_data.unk04

                # Write the unknown data
                else:

                    # Write the data
                    data_child += data_info_child.data

                # Write the name [LAYERS], [NODES], DbzEyeInfo or another special name.
                # If it doesn't exists, we create it
                if data_info_child.name_offset != 0:
                    if data_info_child.name in special_names:
                        name_offset = special_names[data_info_child.name]
                    else:
                        special_names[data_info_child.name] = string_name_offset
                        name_offset = string_name_offset
                        string_table_child += b'\x00' + data_info_child.name.encode('utf-8')
                        string_name_size = 1 + len(data_info_child.name)
                        # Update the offset
                        string_table_child_size += string_name_size
                        string_name_offset += string_name_size
                else:
                    name_offset = 0

        # The type entry is bone
        elif type_entry == b'BONE':

            # Write the name. If it doesn't exists, we create it
            if data_info_child.name_offset != 0:
                if data_info_child.name in special_names:
                    name_offset = special_names[data_info_child.name]
                else:
                    special_names[data_info_child.name] = string_name_offset
                    name_offset = string_name_offset
                    string_table_child += b'\x00' + data_info_child.name.encode('utf-8')
                    string_name_size = 1 + len(data_info_child.name)
                    # Update the offset
                    string_table_child_size += string_name_size
                    string_name_offset += string_name_size
            else:
                name_offset = 0

            # Write the data
            data_child += data_info_child.data

        # If the child has others child, we write them first
        if data_info_child.child_count > 0:
            string_table_sub_child, string_table_sub_child_size, string_name_offset_children, data_sub_child, \
                data_sub_child_size, data_offset_children = write_children(main_window, num_material, num_textures,
                                                                           data_info_child, type_entry,
                                                                           string_name_offset,
                                                                           data_offset + data_info_child.data_size,
                                                                           special_names)

            # Write children offset section first
            data_child_offset_section += name_offset.to_bytes(4, 'big')
            data_child_offset_section += data_offset.to_bytes(4, 'big')

            # Update the string_table and string_table_size
            string_table_child += string_table_sub_child
            string_table_child_size += string_table_sub_child_size
            string_name_offset += string_table_sub_child_size

            # Update the data and data_size
            data_child += data_sub_child
            data_child_size += data_sub_child_size
            data_offset += data_sub_child_size
        else:
            # Write children offset section
            data_child_offset_section += name_offset.to_bytes(4, 'big')
            data_child_offset_section += data_offset.to_bytes(4, 'big')

        data_child_offset_section += data_info_child.data_size.to_bytes(4, 'big')
        data_child_offset_section += data_info_child.child_count.to_bytes(4, 'big')
        data_child_offset_section += data_offset_children.to_bytes(4, 'big')

        # Update the offsets
        data_child_size += data_info_child.data_size
        data_child_offset_section_size += 20
        data_offset += data_info_child.data_size

    return string_table_child, string_table_child_size, string_name_offset, data_child + data_child_offset_section, \
        data_child_size + data_child_offset_section_size, data_offset


def validation_dds_imported_texture(tx2d_info, width, height, mip_maps, dxt_encoding_text):

    message = ""

    # Check resolution
    if width != tx2d_info.width or height != tx2d_info.height:
        message = "<li> The original size is " + str(tx2d_info.width) \
            + "x" + str(tx2d_info.height) \
            + ". The imported texture is " + str(width) + "x" + str(height) + ".</li>"

    # Check mip_maps
    if tx2d_info.mip_maps != mip_maps:
        message = message + "<li> The original Mipmaps has " + str(tx2d_info.mip_maps) \
            + ". The imported texture has " + str(mip_maps) + ".</li>"

    # Check encoding
    dxt_encoding_text_original = get_encoding_name(tx2d_info.dxt_encoding)
    if dxt_encoding_text_original != dxt_encoding_text:
        message = message + "<li> The original encoding is " + dxt_encoding_text_original \
                  + ". The imported texture is " + dxt_encoding_text + ".</li>"

    return message


def validation_bmp_imported_texture(tx2d_info, width, height, number_bits, mip_maps, dxt_encoding_text):

    message = ""

    # Check resolution
    if width != tx2d_info.width or height != tx2d_info.height:
        message = "<li>The original size is " + str(tx2d_info.width) \
            + "x" + str(tx2d_info.height) \
            + ". The imported texture is " + str(width) + "x" + str(height) + ".</li>"

    # Check number of bits
    if 32 != number_bits:
        message = message + "<li>The original number of bits is " + str(32) \
            + ". The imported texture is " + str(number_bits) + " bits.</li>"

    # Check mip_maps
    if tx2d_info.mip_maps != mip_maps:
        message = message + "<li> The original Mipmaps has " + str(tx2d_info.mip_maps) \
            + ". The imported texture has " + str(mip_maps) + ".</li>"

    # Check encoding
    dxt_encoding_text_original = get_encoding_name(tx2d_info.dxt_encoding)
    if dxt_encoding_text_original != dxt_encoding_text:
        message = message + "<li> The original encoding is " + dxt_encoding_text_original \
                  + ". The imported texture is " + dxt_encoding_text + ".</li>"

    return message


def read_dds_file(file_path):
    try:
        _img = image.load(file_path)

        tex = _img.get_texture()
        tex = tex.get_image_data()
        _format = tex.format
        pitch = tex.width * len(_format)
        pixels = tex.get_data(_format, pitch)

        img = QImage(pixels, tex.width, tex.height, QImage.Format_ARGB32)
        img = img.rgbSwapped()

        return img

    except OSError:
        print("The header of the image is not recognizable")
        raise GLException
    except GLException:
        print("DDS image can't be shown")
        raise GLException
    except Exception:
        print("Unknown exception. DDS image can't be shown")
        raise GLException


def show_dds_image(image_texture, texture_data, width, height, texture_path="temp.dds"):

    try:

        if texture_data is not None:
            # Create the dds in disk and open it
            with open(texture_path, mode="wb") as output:
                output.write(texture_data)

        img = read_dds_file(texture_path)

        mpixmap = QPixmap.fromImage(img)

        # If the image is higher in width or height from the imageTexture,
        # we will reduce the size maintaing the aspect ratio
        if width > height:
            if width > image_texture.width():
                new_height = int((height / width) * image_texture.width())
                mpixmap = mpixmap.scaled(image_texture.width(), new_height)
        else:
            if height > image_texture.height():
                new_width = int((width / height) * image_texture.height())
                mpixmap = mpixmap.scaled(new_width, image_texture.height())

        # Show the image
        image_texture.setPixmap(mpixmap)
    except GLException:
        image_texture.clear()

    if texture_data is not None:
        os.remove(texture_path)


def show_bmp_image(image_texture, texture_data, width, height):

    try:
        mpixmap = QPixmap()
        mpixmap.loadFromData(texture_data, "BMP")

        # If the image is higher in width or height from the imageTexture,
        # we will reduce the size maintaing the aspect ratio
        # Since a shader has height of 1, in order to show it more clearly, we ignore the scaling
        if height == 1:
            mpixmap = mpixmap.scaled(image_texture.width(), width)
        elif width > height:
            if width > image_texture.width():
                new_height = int((height / width) * image_texture.width())
                mpixmap = mpixmap.scaled(image_texture.width(), new_height)
        else:
            if height > image_texture.height():
                new_width = int((width / height) * image_texture.height())
                mpixmap = mpixmap.scaled(new_width, image_texture.height())

        image_texture.setPixmap(mpixmap)
    except OSError:
        image_texture.clear()


def update_tx2d_data(file, index):

    # Change the size
    file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[index].
               data_info.data.data_size.to_bytes(4, byteorder="big"))
    # Change width
    file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[index].
               data_info.data.width.to_bytes(2, byteorder="big"))
    # Change height
    file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[index].
               data_info.data.height.to_bytes(2, byteorder="big"))
    # Change mip_maps
    file.seek(2, os.SEEK_CUR)
    file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[index].
               data_info.data.mip_maps.to_bytes(2, byteorder="big"))
    # Change dxt encoding
    file.seek(8, os.SEEK_CUR)
    file.write(VEV.sprp_file.type_entry[b'TX2D'].data_entry[index].
               data_info.data.dxt_encoding.to_bytes(1, byteorder="big"))


def replace_texture_properties(main_window, data_entry, unk0x00, len_data, width, height, mip_maps, unk0x1c,
                               dxt_encoding):

    # Get the difference in size between actual and modified texture to check if is necessary to update offsets
    difference = len_data - data_entry.data_info.data.data_size

    # Change the var related to the encoding
    if data_entry.data_info.data.related_2_encoding != unk0x00:
        data_entry.data_info.data.related_2_encoding = unk0x00

    # Change size
    if difference != 0:
        data_entry.data_info.data.data_size = len_data

    # Change width
    if data_entry.data_info.data.width != width:
        data_entry.data_info.data.width = width
        main_window.sizeImageText.setText("Resolution: %dx%d" % (width, data_entry.data_info.data.height))
    # Change height
    if data_entry.data_info.data.height != height:
        data_entry.data_info.data.height = height
        main_window.sizeImageText.setText("Resolution: %dx%d" % (data_entry.data_info.data.width, height))

    # Change mipMaps
    if data_entry.data_info.data.mip_maps != mip_maps:
        data_entry.data_info.data.mip_maps = mip_maps
        main_window.mipMapsImageText.setText("Mipmaps: %s" % mip_maps)

    # Change unk0x1c (related to the encoding)
    if data_entry.data_info.data.unk0x1c != unk0x1c:
        data_entry.data_info.data.unk0x1c = unk0x1c

    # Change dxt encoding
    if data_entry.data_info.data.dxt_encoding != dxt_encoding:
        data_entry.data_info.data.dxt_encoding = dxt_encoding
        main_window.encodingImageText.setText("Encoding: %s" % (get_encoding_name(dxt_encoding)))


# main_window -> instance of the main program
# import_file_path -> path where the file is located
# ask_user -> flag that will activate or deactive a pop up message when the imported texture has differences with
# the original texture
def import_texture(main_window, import_file_path, ask_user, show_texture_flag, data_entry):

    with open(import_file_path, mode="rb") as file:
        header = file.read(4)

        # It's a DDS modded image
        if header == b'DDS ':

            # Get the height and width of the modified image
            file.seek(12)
            height = int.from_bytes(file.read(VEV.bytes2Read), 'little')
            width = int.from_bytes(file.read(VEV.bytes2Read), 'little')
            # Get the mipmaps
            file.seek(28)
            mip_maps = int.from_bytes(file.read(1), 'big')
            # Get the dxtencoding
            file.seek(84)
            dxt_encoding_text = file.read(VEV.bytes2Read).decode()
            dxt_encoding = get_dxt_value(dxt_encoding_text)

            message = validation_dds_imported_texture(data_entry.data_info.data, width,
                                                      height, mip_maps, dxt_encoding_text)

            # If the message is empty, there is no differences between original and modified one
            if message:

                # It's an image that originally is swizzled. It's mandatory that the modified texture has the same
                # properties as the original texture due to the swizzled algorithm
                if data_entry.data_info.extension == "png" and data_entry.data_info.data.dxt_encoding == 0:

                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setWindowIcon(main_window.ico_image)
                    msg.setText(VEV.message_base_import_BMP_start + "<ul>" + message + "</ul>")
                    msg.exec()
                    return

                # This will be used to ask the user if he/she wants to replace the texture eventhough it has
                # differences between original texture and modified one
                elif ask_user:
                    msg = QMessageBox()

                    # Concatenate the base message and the differences the tool has found
                    message = VEV.message_base_import_texture_start + "<ul>" + message + "</ul>" + \
                        VEV.message_base_import_texture_end

                    # Ask to the user if he/she is sure that wants to replace the texture
                    msg.setWindowIcon(main_window.ico_image)
                    message_import_result = msg.question(main_window, 'Warning', message, msg.Yes | msg.No)

                    # If the users click on 'No', the modified texture won't be imported
                    if message_import_result == msg.No:
                        return

            # Get all the data
            file.seek(0)
            data = file.read()
            len_data = len(data[128:])

            # --- Importing the texture ---
            # Change texture in the array
            data_entry.data_info.data.tx2d_vram.data = data

            # We don't know about this value, but if the encoding is DXT5, has to be 34. However, if the encoding
            # is DXT1, the value has to be 2
            if dxt_encoding == 24:
                unk0x00 = 34
            else:
                unk0x00 = 2

            # Replace the texture properties in memory
            replace_texture_properties(main_window, data_entry, unk0x00, len_data, width, height, mip_maps, 2804419200,
                                       dxt_encoding)

            # If the flag is activated, we show the texture
            if show_texture_flag:
                try:
                    # Show texture in the program
                    # If we're dealing with a Xbox spr file and the encoding of the texture is ATI2 (normal texture)
                    # we won't show anything in the tool view
                    if VEV.header_type_spr_file != b'SPR3' or dxt_encoding != 32:
                        show_dds_image(main_window.imageTexture, None, width, height, import_file_path)
                    else:
                        main_window.imageTexture.clear()

                except OSError:
                    main_window.imageTexture.clear()

        # it's a BMP modded image
        elif header[:2] == b'BM':

            # Get offset where the data starts
            file.seek(10)
            offset_start_data = int.from_bytes(file.read(VEV.bytes2Read), 'little')
            # If the offset of the texture data is in position 70, the actual data starts in the next byte
            if offset_start_data == 70:
                offset_start_data += 1

            # Get the height and width of the modified image
            file.seek(18)
            width = int.from_bytes(file.read(VEV.bytes2Read), 'little')
            height = int.from_bytes(file.read(VEV.bytes2Read), 'little')

            # Get the number of bits
            file.seek(28)
            number_bits = int.from_bytes(file.read(2), 'little')

            # Validate the BMP imported texture
            message = validation_bmp_imported_texture(data_entry.data_info.data, width, height, number_bits, 1, "RGBA")

            # If there is a message, it has detected differences
            if message:

                # It's an image that originally is swizzled. It's mandatory that the modified texture has the same
                # properties as the original texture due to the swizzled algorithm
                if data_entry.data_info.extension == "png" and data_entry.data_info.data.dxt_encoding == 0:

                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setWindowIcon(main_window.ico_image)
                    msg.setText(VEV.message_base_import_BMP_start + "<ul>" + message + "</ul>")
                    msg.exec()
                    return

                # This will be used to ask the user if he/she wants to replace the texture eventhough it has
                # differences between original texture and modified one
                elif ask_user:
                    msg = QMessageBox()

                    # Concatenate the base message and the differences the tool has found
                    message = VEV.message_base_import_texture_start + "<ul>" + message + "</ul>" + \
                        VEV.message_base_import_texture_end

                    # Ask to the user if he/she is sure that wants to replace the texture
                    msg.setWindowIcon(main_window.ico_image)
                    message_import_result = msg.question(main_window, 'Warning', message, msg.Yes | msg.No)

                    # If the users click on 'No', the modified texture won't be imported
                    if message_import_result == msg.No:
                        return

            # Get all the data
            file.seek(0)
            data = file.read()

            # We get the header, the extra data (some tools export extra info before the
            # data of the texture) and the data itself
            header = data[:54]
            data_extra = data[54:offset_start_data]
            data_texture = data[offset_start_data:]

            # Check if we have to fix the bmp in order to avoid the corrupted texture
            len_data, header, data_texture = fix_bmp_header_data(header, data_extra, data_texture)
            data = header + data_texture

            # --- Importing the texture ---
            # Change texture in the array
            if data_entry.data_info.extension != "png":
                data_entry.data_info.data.tx2d_vram.data = data
            # It's png swizzled texture file
            else:
                data_entry.data_info.data.tx2d_vram.data_unswizzle = data

            # Replace the texture properties in memory
            replace_texture_properties(main_window, data_entry, 2, len_data, width, height, 1, 2804746880, 0)

            # If the flag is activated, we show the texture
            if show_texture_flag:
                try:
                    # Show texture in the program
                    show_bmp_image(main_window.imageTexture, data, width, height)

                except OSError:
                    main_window.imageTexture.clear()

        else:
            # Wrong texture file
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setWindowIcon(main_window.ico_image)
            msg.setText("Invalid texture file.")
            msg.exec()
            return

    return ""


# This method will prepare a new sprp_data_entry (the comun values between dds and bmp image)
def prepare_sprp_data_entry(main_window, import_file_path, sprp_data_entry):

    # Create a new spr_data_entry
    sprp_data_entry.data_type = b'TX2D'
    sprp_data_entry.index = main_window.listView.model().rowCount()

    # Store the data_info from the data_entry
    # The name offset value will be unique and temporal for now
    sprp_data_entry.data_info.name_offset = VEV.unique_temp_name_offset
    VEV.unique_temp_name_offset += 1
    sprp_data_entry.data_info.name = os.path.basename(import_file_path).split(".")[0]
    sprp_data_entry.data_info.extension = "tga"
    sprp_data_entry.data_info.name_size = len(sprp_data_entry.data_info.name) + 1 + \
        len(sprp_data_entry.data_info.extension)
    sprp_data_entry.data_info.data_size = 36

    # Append to the array of textures in the window list
    item = QStandardItem(sprp_data_entry.data_info.name)
    item.setData(sprp_data_entry)
    item.setEditable(False)
    main_window.listView.model().appendRow(item)

    # Append to the array of textures in the material section
    listen_events_logic(main_window, False)
    main_window.textureVal.addItem(sprp_data_entry.data_info.name, sprp_data_entry.data_info.name_offset)
    listen_events_logic(main_window, True)


# Will add a new texture to the list view, creating a new sprp_data_entry
def add_texture(main_window, import_file_path):

    with open(import_file_path, mode="rb") as file:

        # Create a new spr_data_entry
        sprp_data_entry = SprpDataEntry()
        # Create a new tx2d_info instance
        sprp_data_entry.data_info.data = Tx2dInfo()
        # Create a new tx2d_vram instance
        sprp_data_entry.data_info.data.tx2d_vram = Tx2dVram()

        # Read the type of file
        header = file.read(4)

        # It's a DDS modded image
        if header == b'DDS ':

            # Get the height and width of the modified image
            file.seek(12)
            sprp_data_entry.data_info.data.height = int.from_bytes(file.read(VEV.bytes2Read), 'little')
            sprp_data_entry.data_info.data.width = int.from_bytes(file.read(VEV.bytes2Read), 'little')
            # Get the mipmaps
            file.seek(28)
            sprp_data_entry.data_info.data.mip_maps = int.from_bytes(file.read(1), 'big')
            # Get the dxtencoding
            file.seek(84)
            sprp_data_entry.data_info.data.dxt_encoding = get_dxt_value(file.read(VEV.bytes2Read).decode())

            # We don't know about this value, but if the encoding is DXT5, has to be 34. However, if the encoding
            # is DXT1, the value has to be 2
            if sprp_data_entry.data_info.data.dxt_encoding == 24:
                sprp_data_entry.data_info.data.related_2_encoding = 34
            else:
                sprp_data_entry.data_info.data.related_2_encoding = 2
            # When is DXT encoding, this unk value has to be that value
            sprp_data_entry.data_info.data.unk0x1c = 2804419200

            # Get all the data
            file.seek(0)
            data = file.read()

            # Store the data and size
            sprp_data_entry.data_info.data.tx2d_vram.data = data
            sprp_data_entry.data_info.data.data_size = len(data[128:])

            prepare_sprp_data_entry(main_window, import_file_path, sprp_data_entry)

        # it's a BMP modded image
        elif header[:2] == b'BM':

            # Get offset where the data starts
            file.seek(10)
            offset_start_data = int.from_bytes(file.read(VEV.bytes2Read), 'little')
            # If the offset of the texture data is in position 70, the actual data starts in the next byte
            if offset_start_data == 70:
                offset_start_data += 1

            # Get the height and width of the modified image
            file.seek(18)
            sprp_data_entry.data_info.data.width = int.from_bytes(file.read(VEV.bytes2Read), 'little')
            sprp_data_entry.data_info.data.height = int.from_bytes(file.read(VEV.bytes2Read), 'little')
            # Get the mipmaps
            sprp_data_entry.data_info.data.mip_maps = 1
            # Get the dxtencoding
            sprp_data_entry.data_info.data.dxt_encoding = 0

            # We don't know about this value, but for RGBA encoding, has to be 2
            sprp_data_entry.data_info.data.related_2_encoding = 2
            # We don't know about this value, but for RGBA encoding, has to be that value
            sprp_data_entry.data_info.data.unk0x1c = 2804746880

            # Get all the data
            file.seek(0)
            data = file.read()

            # We get the header, the extra data (some tools export extra info before the
            # data of the texture) and the data itself
            header = data[:54]
            data_extra = data[54:offset_start_data]
            data_texture = data[offset_start_data:]

            # Check if we have to fix the bmp in order to avoid the corrupted texture
            len_data, header, data_texture = fix_bmp_header_data(header, data_extra, data_texture)
            data = header + data_texture

            # Store the data and size
            sprp_data_entry.data_info.data.tx2d_vram.data = data
            sprp_data_entry.data_info.data.data_size = len_data

            prepare_sprp_data_entry(main_window, import_file_path, sprp_data_entry)

        else:
            # Wrong texture file
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setWindowIcon(main_window.ico_image)
            msg.setText("Invalid texture file.")
            msg.exec()
            return


# Will add the material children data to the material children editor window
def load_material_children_to_window(main_window, mtrl_child_data):

    main_window.MaterialChildEditorUI.shadow_orienation_value \
        .setValue(int(mtrl_child_data.Ilumination_Shadow_orientation)*100)
    main_window.MaterialChildEditorUI.light_orientation_glow_value \
        .setValue(int(mtrl_child_data.Ilumination_Light_orientation_glow*100))
    main_window.MaterialChildEditorUI.saturation_base_value.setValue(int(mtrl_child_data.Saturation_base*100))
    main_window.MaterialChildEditorUI.saturation_glow_value.setValue(int(mtrl_child_data.Saturation_glow*100))
    main_window.MaterialChildEditorUI.brightness_base_value.setValue(int(mtrl_child_data.Brightness_toonmap*100))
    main_window.MaterialChildEditorUI.brightness_glow_value.setValue(int(mtrl_child_data.Brightness_incandescence*100))

    red_value = int(mtrl_child_data.Border_RGBA[0]*255)
    green_value = int(mtrl_child_data.Border_RGBA[1]*255)
    blue_value = int(mtrl_child_data.Border_RGBA[2]*255)
    alpha_value = int(mtrl_child_data.Border_RGBA[3]*255)
    # If the value of the new RGBA is different from the old one, we change the border color
    if main_window.MaterialChildEditorUI.border_color_R_value.value() != red_value or \
            main_window.MaterialChildEditorUI.border_color_G_value.value() != green_value or \
            main_window.MaterialChildEditorUI.border_color_B_value.value() != blue_value or \
            main_window.MaterialChildEditorUI.border_color_A_value.value() != alpha_value:
        border_rgba = str(mtrl_child_data.Border_RGBA).replace("[", "").replace("]", "")
        main_window.MaterialChildEditorUI.border_color_color.setStyleSheet(
            "background-color: rgba(" + border_rgba + ");")
        main_window.MaterialChildEditorUI.border_color_R_value.setValue(red_value)
        main_window.MaterialChildEditorUI.border_color_G_value.setValue(green_value)
        main_window.MaterialChildEditorUI.border_color_B_value.setValue(blue_value)
        main_window.MaterialChildEditorUI.border_color_A_value.setValue(alpha_value)


# Export the material by giving the output path and mtrl entry
def export_material(export_path, mtrl_data_entry):

    file = open(export_path, mode="wb")
    # Write the unk data (normaly is 112 bytes)
    file.write(mtrl_data_entry.data_info.data.unk_00)
    # If the material has children, we write them too
    if mtrl_data_entry.data_info.child_count > 0:
        mtrl_child = mtrl_data_entry.data_info.child_info[0]
        mtrl_prop = mtrl_child.data
        data_child = b''
        # Raging Blast 2 child
        if mtrl_child.data_size == VEV.rb2_material_child_size:
            data_child += struct.pack('>f', mtrl_prop.Ilumination_Shadow_orientation)
            data_child += struct.pack('>f', mtrl_prop.Ilumination_Light_orientation_glow)
            for j in range(len(mtrl_prop.unk0x04)):
                data_child += struct.pack('>f', mtrl_prop.unk0x04[j])
            data_child += struct.pack('>f', mtrl_prop.Brightness_purple_light_glow)
            data_child += struct.pack('>f', mtrl_prop.Saturation_glow)
            data_child += struct.pack('>f', mtrl_prop.Saturation_base)
            data_child += \
                struct.pack('>f', mtrl_prop.Brightness_toonmap_active_some_positions)
            data_child += struct.pack('>f', mtrl_prop.Brightness_toonmap)
            data_child += \
                struct.pack('>f', mtrl_prop.Brightness_toonmap_active_other_positions)
            data_child += \
                struct.pack('>f', mtrl_prop.Brightness_incandescence_active_some_positions)
            data_child += struct.pack('>f', mtrl_prop.Brightness_incandescence)
            data_child += \
                struct.pack('>f', mtrl_prop.Brightness_incandescence_active_other_positions)
            for j in range(len(mtrl_prop.Border_RGBA)):
                data_child += struct.pack('>f', mtrl_prop.Border_RGBA[j])
            for j in range(len(mtrl_prop.unk0x44)):
                data_child += struct.pack('>f', mtrl_prop.unk0x44[j])
            for j in range(len(mtrl_prop.unk0x50)):
                data_child += struct.pack('>f', mtrl_prop.unk0x50[j])
        else:
            data_child += mtrl_prop

        file.write(data_child)
    file.close()


# Import the material
def import_material(main_window, file_import_path, mtrl_data_entry, multiple_import, show_edited_child):

    with open(file_import_path, mode="rb") as file:

        size_file = len(file.read())
        child_size = size_file - VEV.material_values_size
        # The file of the material has to be 112 bytes length
        if size_file >= VEV.material_values_size:
            file.seek(0)
        else:
            # Wrong material file
            if multiple_import:
                return "<li>" + mtrl_data_entry.data_info.name + ": " + \
                       "Invalid material file. It should have at least 112 bytes" + "</li>"
            else:
                return "Invalid material file. It should have at least 112 bytes"

        # Get the mtrl data
        mtrl_data = mtrl_data_entry.data_info.data

        # Read the main data
        mtrl_data.unk_00 = file.read(VEV.material_values_size)

        # Read children (if any)
        if child_size > 0:
            # The children from the file has 96 of size (RB2 material children)
            if child_size == VEV.rb2_material_child_size:
                mtrl_prop = MtrlProp()
                mtrl_prop.Ilumination_Shadow_orientation = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Ilumination_Light_orientation_glow = struct.unpack('>f', file.read(4))[0]
                for i in range(len(mtrl_prop.unk0x04)):
                    mtrl_prop.unk0x04[i] = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Brightness_purple_light_glow = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Saturation_glow = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Saturation_base = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Brightness_toonmap_active_some_positions = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Brightness_toonmap = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Brightness_toonmap_active_other_positions = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Brightness_incandescence_active_some_positions = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Brightness_incandescence = struct.unpack('>f', file.read(4))[0]
                mtrl_prop.Brightness_incandescence_active_other_positions = struct.unpack('>f', file.read(4))[0]
                for i in range(len(mtrl_prop.Border_RGBA)):
                    mtrl_prop.Border_RGBA[i] = struct.unpack('>f', file.read(4))[0]
                for i in range(len(mtrl_prop.unk0x44)):
                    mtrl_prop.unk0x44[i] = struct.unpack('>f', file.read(4))[0]
                for i in range(len(mtrl_prop.unk0x50)):
                    mtrl_prop.unk0x50[i] = struct.unpack('>f', file.read(4))[0]

                # Only make changes for the material child window if the current material that we're modifying
                # is the actual one that the user is watching
                if show_edited_child:
                    # Enable the material children edition
                    if not main_window.editMaterialChildrenButton.isEnabled():
                        main_window.editMaterialChildrenButton.setEnabled(True)
                    # Load the material children to the window
                    load_material_children_to_window(main_window, mtrl_prop)

            # Generic material children
            else:
                mtrl_prop = file.read(child_size)

                # Only make changes for the material child window if the current material that we're modifying
                # is the actual one that the user is watching
                if show_edited_child and main_window.editMaterialChildrenButton.isEnabled():
                    # Disable the material children edition
                    main_window.editMaterialChildrenButton.setEnabled(False)

            # Check if the actual material has a children section or not
            if mtrl_data_entry.data_info.child_count > 0:
                mtrl_data_entry.data_info.child_info[0].data = mtrl_prop
            else:
                sprp_data_info_child = SprpDataInfo()
                sprp_data_info_child.data = mtrl_prop
                sprp_data_info_child.name = "DbzCharMtrl"
                mtrl_data_entry.data_info.child_info.append(sprp_data_info_child)
                mtrl_data_entry.data_info.child_count = 1

            # Update the size of the children
            mtrl_data_entry.data_info.child_info[0].data_size = child_size

        # The material from the file doesn't have children, so we remove it
        else:
            mtrl_data_entry.data_info.child_count = 0
            mtrl_data_entry.data_info.child_info = []

            # Only make changes for the material child window if the current material that we're modifying
            # is the actual one that the user is watching
            if show_edited_child and main_window.editMaterialChildrenButton.isEnabled():
                # Disable the material children edition
                main_window.editMaterialChildrenButton.setEnabled(False)

    return ""


# Replace current children material values with the values in the material children window
def replace_material_children_values(main_window, mtrl_data_entry):

    # Get the mtrl child data
    mtrl_child_data = mtrl_data_entry.data_info.child_info[0].data

    mtrl_child_data.Ilumination_Shadow_orientation = \
        float(main_window.MaterialChildEditorUI.shadow_orienation_value.value() / 100)
    mtrl_child_data.Ilumination_Light_orientation_glow = \
        float(main_window.MaterialChildEditorUI.light_orientation_glow_value.value() / 100)
    mtrl_child_data.Saturation_base = float(main_window.MaterialChildEditorUI.saturation_base_value.value() / 100)
    mtrl_child_data.Saturation_glow = float(main_window.MaterialChildEditorUI.saturation_glow_value.value() / 100)
    mtrl_child_data.Brightness_toonmap = float(main_window.MaterialChildEditorUI.brightness_base_value.value() / 100)
    mtrl_child_data.Brightness_toonmap_active_some_positions = mtrl_child_data.Brightness_toonmap
    mtrl_child_data.Brightness_toonmap_active_other_positions = mtrl_child_data.Brightness_toonmap
    mtrl_child_data.Brightness_incandescence = \
        float(main_window.MaterialChildEditorUI.brightness_glow_value.value() / 100)
    mtrl_child_data.Brightness_incandescence_active_some_positions = mtrl_child_data.Brightness_incandescence
    mtrl_child_data.Brightness_incandescence_active_other_positions = mtrl_child_data.Brightness_incandescence
    mtrl_child_data.Border_RGBA[0] = float(main_window.MaterialChildEditorUI.border_color_R_value.value() / 255)
    mtrl_child_data.Border_RGBA[1] = float(main_window.MaterialChildEditorUI.border_color_G_value.value() / 255)
    mtrl_child_data.Border_RGBA[2] = float(main_window.MaterialChildEditorUI.border_color_B_value.value() / 255)
    mtrl_child_data.Border_RGBA[3] = float(main_window.MaterialChildEditorUI.border_color_A_value.value() / 255)
