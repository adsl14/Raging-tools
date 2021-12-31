from lib.packages import os, datetime


class VEV:

	# resources path
	dbrb_compressor_path = os.path.join("lib", "resources", "dbrb_compressor.exe")
	swizzle_path = os.path.join("lib", "vram_explorer", "resources", "swizzle.exe")

	# Warning base message when importing a texture with differences in encoding, size, mipmaps, etc
	message_base_import_texture_start = "The new texture has the following differences from the original:"
	message_base_import_texture_end = "Do you want to continue?"
	message_base_import_BMP_start = "There are some errors while importing the texture:"

	# number of bytes that usually reads the program
	bytes2Read = 4
	# Temp folder name
	temp_folder = "temp_VE" + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S")

	# *** vars that need to be reseted when loading a new spr/vram file ***
	# --- SPR vars ---
	# Path where the spr file is located
	spr_file_path = ""
	# SPRP file class
	sprp_file = None
	# --- VRAM vars ---
	# Path where the vram file is located
	vram_file_path = ""

	enable_combo_box = False
