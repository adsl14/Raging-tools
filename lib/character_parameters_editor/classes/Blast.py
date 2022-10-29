class Blast:

    def __init__(self):
        self.unk0x00 = b''
        self.glow = 0
        self.number_of_hits = 0
        self.unk0x04 = b''
        self.partner_id = 0
        self.unk0x0D = b''
        self.reach_attack = 0.0
        self.unk0x14 = b''
        self.attack_damage = 0
        self.unk0x1A = b''
        self.cost_attack = 0
        self.unk0x1C = b''
        self.power_ups = dict({"Melee": 0, "Defense": 0, "Super Attack": 0, "Ki": 0})
        self.unk0x22 = b''
        self.unk0x24 = b''
        self.unk0x2A = b''
        self.skill_stackable = 0
        self.unk0x33 = b''
        self.camera = [0, 0, 0, 0]
        self.unk0x4C = b''
        self.activation_skill = 0
        self.chargeable_boost = 0
        self.unk0x50 = b''
        self.speed_of_attack = 0.0
        self.unk0x58 = b''
        self.size_of_attack = 0.0
        self.unk0x60 = b''
        self.modified = False
