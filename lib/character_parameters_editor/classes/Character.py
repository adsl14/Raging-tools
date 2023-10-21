class Character:

	def __init__(self):

		# First positions in the file operate_resident_param
		self.position_visual_parameters = 0
		self.health = 0
		self.camera_size = [] * 2  # 0 cutscene, 1 idle
		self.hit_box = 0
		self.aura_size = [] * 3  # 0 is idle, 1 dash, 2 is charge
		self.color_lightning = 0
		self.glow_lightning = 0

		# Seconds positions in the file operate_resident_param
		self.position_trans = 0
		self.character_id = 0
		self.transformation_effect = 0
		self.transformation_partner = 0
		self.transformations = [] * 4
		self.amount_ki_transformations = [] * 4
		self.transformations_animation = [] * 4
		self.fusion_partner = [] * 2
		self.fusions = [] * 4
		self.amount_ki_fusions = [] * 4
		self.fusions_animation = [] * 4

		# Values for the file resident_skill_path
		self.position_skill = 0
		self.signature_values = b''

		# Values for the file db_font_pad_PS3_s.zpak
		self.position_resident_character_param = 0
		self.aura_type = 0
		self.blast_attacks = dict({"Up": 0, "Right": 0, "Down": 0, "Left": 0, "Push": 0})

		# Values for the file cs_main.zpak
		self.position_cs_main = 0
		self.character_name_text_id = 0
		self.character_sub_name_text_id = 0
