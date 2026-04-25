import re


class Weapon:
    def __init__(
        self,
        name,
        attacks,
        weapon_skill,
        strength,
        armour_penetration,
        damage,
    ):
        self.name = name
        self.attacks = attacks
        self.weapon_skill = weapon_skill
        self.strength = strength
        self.armour_penetration = armour_penetration
        self.damage = damage

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not str(value).strip():
            raise ValueError("Weapon name is required.")
        self._name = str(value).strip()

    @property
    def attacks(self):
        return self._attacks

    @attacks.setter
    def attacks(self, value):
        self._attacks = self._validate_roll_expression(value, "Attacks")

    @property
    def weapon_skill(self):
        return self._weapon_skill

    @weapon_skill.setter
    def weapon_skill(self, value):
        self._weapon_skill = self._validate_weapon_skill(value)

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, value):
        self._strength = self._validate_positive_int(value, "Strength")

    @property
    def armour_penetration(self):
        return self._armour_penetration

    @armour_penetration.setter
    def armour_penetration(self, value):
        self._armour_penetration = int(value)

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = self._validate_roll_expression(value, "Damage")

    def roll_attacks(self, rng):
        return self._roll_expression(self.attacks, rng)

    def roll_damage(self, rng):
        return self._roll_expression(self.damage, rng)

    
    def _validate_positive_int(self,value, field_name):
        value = int(value)
        if value < 1:
            raise ValueError(f"{field_name} must be a positive integer.")
        return value

    
    def _validate_weapon_skill(self, value):
        if value is None:
            return None
        text = str(value).strip()
        if text == "":
            return None
        value = int(text)
        if value < 2 or value > 6:
            raise ValueError("Weapon Skill must be between 2 and 6.")
        return value

    
    def _validate_roll_expression(self, value, field_name):
        text = str(value).strip().upper().replace(" ", "")
        if not text:
            raise ValueError(f"{field_name} must not be empty.")

        if text.isdigit():
            if int(text) < 1:
                raise ValueError(f"{field_name} must be at least 1.")
            return text

        pattern = r"^(?:(\d+)?D(3|6))(?:\+(\d+))?$"
        match = re.fullmatch(pattern, text)
        if not match:
            raise ValueError(
                f"{field_name} must be in one of these formats: "
                "D3, D6, 2D3, 3D6, D6+1, 2D6+3."
            )

        count_text, die_text, bonus_text = match.groups()
        count = int(count_text) if count_text else 1
        die = int(die_text)
        bonus = int(bonus_text) if bonus_text else 0
        if count < 1:
            raise ValueError(f"{field_name} dice count must be at least 1.")
        if die not in (3, 6):
            raise ValueError(f"{field_name} die must be D3 or D6.")
        if bonus < 0:
            raise ValueError(f"{field_name} bonus must be non-negative.")
        return text

    
    def _roll_expression(self, expression, rng):
        text = str(expression).strip().upper().replace(" ", "")
        if text.isdigit():
            return int(text)

        match = re.fullmatch(r"^(?:(\d+)?D(3|6))(?:\+(\d+))?$", text)
        if not match:
            raise ValueError(f"Invalid roll expression: {expression}")

        count_text, die_text, bonus_text = match.groups()
        count = int(count_text) if count_text else 1
        die = int(die_text)
        bonus = int(bonus_text) if bonus_text else 0

        return sum(rng.randint(1, die) for _ in range(count)) + bonus

    def __str__(self):
        weapon_skill_display = (
            "Auto" if self.weapon_skill is None else self.weapon_skill
        )
        return (
            f"{self.name} (Attacks={self.attacks}, "
            f"WS={weapon_skill_display}, S={self.strength}, "
            f"AP={self.armour_penetration}, Dmg={self.damage})"
        )


class Defender:
    def __init__(self, name, toughness, wounds, save, invulnerable_save=None):
        self.name = name
        self.toughness = toughness
        self.wounds = wounds
        self.save = save
        self.invulnerable_save = invulnerable_save

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not str(value).strip():
            raise ValueError("Defender name is required.")
        self._name = str(value).strip()

    @property
    def toughness(self):
        return self._toughness

    @toughness.setter
    def toughness(self, value):
        self._toughness = self._validate_positive_int(value, "Toughness")

    @property
    def wounds(self):
        return self._wounds

    @wounds.setter
    def wounds(self, value):
        self._wounds = self._validate_positive_int(value, "Wounds")

    @property
    def save(self):
        return self._save

    @save.setter
    def save(self, value):
        self._save = self._validate_save(value)

    @property
    def invulnerable_save(self):
        return self._invulnerable_save

    @invulnerable_save.setter
    def invulnerable_save(self, value):
        if value is None or value == "":
            self._invulnerable_save = None
            return
        value = int(value)
        if value < 2 or value > 6:
            raise ValueError("Invulnerable save must be between 2 and 6.")
        self._invulnerable_save = value

    
    def _validate_positive_int(self,value, field_name):
        value = int(value)
        if value < 1:
            raise ValueError(f"{field_name} must be a positive integer.")
        return value

    def _validate_d6_target(self, value, field_name):
        value = int(value)
        if value < 2 or value > 6:
            raise ValueError(f"{field_name} must be between 2 and 6.")
        return value

    def _validate_save(self, value):
        value = int(value)
        if value < 2:
            raise ValueError("Save must be at least 2.")
        return value

    def __str__(self):
        inv = f", Inv={
            self.invulnerable_save}+" if self.invulnerable_save else ""
        return f"{
            self.name} (T={
            self.toughness}, W={
            self.wounds}, Sv={
                self.save}+{inv})"
