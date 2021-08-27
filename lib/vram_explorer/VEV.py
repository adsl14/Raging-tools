from lib.packages import os, np, datetime
from lib.vram_explorer.classes.SprpStruct import SprpStruct
from lib.vram_explorer.classes.StpkStruct import StpkStruct


class VEV:

	# types of spr file
	# STPZ and STPK file
	STPZ = "5354505a"
	STPK = "5354504b"
	stpz_file = False
	single_stpk_header = True  # This flag will tell us if the spr and vram has two STPK header (RB2 to RB1 port)

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
	temp_folder = "temp_" + datetime.now().strftime("_%d-%m-%Y_%H-%M-%S")

	# Paths where are the files
	spr_file_path_original = ""
	spr_file_path = ""
	vram_file_path_original = ""
	vram_file_path = ""
	sprp_struct = SprpStruct()
	stpk_struct = StpkStruct()

	# Meta information (offset to tx2dInfos)
	sprpDatasInfo = []
	# Information of the textures
	tx2d_infos = []
	# The textures itself
	tx2_datas = []
	# Size of the vram file
	vram_file_size_old = 0
	# Indexes of textures edited
	textures_index_edited = []
	# Quanty of difference between the modifed texture and the old one
	offset_quanty_difference = np.array(0)
