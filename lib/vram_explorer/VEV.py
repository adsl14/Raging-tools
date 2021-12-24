from lib.packages import os, np, datetime
from lib.vram_explorer.classes.SPRP.SprpFile import SprpFile


class VEV:

	# resources path
	dbrb_compressor_path = os.path.join("lib", "resources", "dbrb_compressor.exe")
	swizzle_path = os.path.join("lib", "vram_explorer", "resources", "swizzle.exe")

	# Warning base message when importing a texture with differences in encoding, size, mipmaps, etc
	message_base_import_DDS_start = "The new texture has the following differences from the original:"
	message_base_import_DDS_end = "The textures could show in the game not propertly. Do you want to continue?"
	message_base_import_BMP_start = "There are some errors while importing the texture:"

	# number of bytes that usually reads the program
	bytes2Read = 4
	# Current selected texture in the list view
	current_selected_texture = 0
	# Temp folder name
	temp_folder = "temp_VE" + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S")

	# Paths where are the files
	spr_file_path = ""
	vram_file_path = ""

	# SPRP file class
	sprp_file = SprpFile()

	# Indexes of textures edited
	textures_index_edited = []
	# Quanty of difference between the modifed texture and the old one
	offset_quanty_difference = np.array(0)
