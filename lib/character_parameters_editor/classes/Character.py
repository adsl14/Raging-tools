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
