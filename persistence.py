import json
import os

from domain import Defender, Weapon


class WeaponRepository:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    def _resolve_path(self, filename):
        if os.path.isabs(filename):
            return filename
        return os.path.join(self.script_dir, filename)

    def save_weapon(self, weapon, filename):
        filepath = self._resolve_path(filename)
        data = {
            "name": weapon.name,
            "attacks": weapon.attacks,
            "weapon_skill": weapon.weapon_skill,
            "strength": weapon.strength,
            "armour_penetration": weapon.armour_penetration,
            "damage": weapon.damage,
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_weapon(self, filename):
        filepath = self._resolve_path(filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        data = self._normalize_weapon_data(data)
        return Weapon(**data)

    def save_weapons(self, weapons, filename):
        filepath = self._resolve_path(filename)
        data = [
            {
                "name": w.name,
                "attacks": w.attacks,
                "weapon_skill": w.weapon_skill,
                "strength": w.strength,
                "armour_penetration": w.armour_penetration,
                "damage": w.damage,
            }
            for w in weapons
        ]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_weapons(self, filename):
        filepath = self._resolve_path(filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Weapon(**self._normalize_weapon_data(d)) for d in data]

    def _normalize_weapon_data(self, data):
        return {
            "name": data["name"],
            "attacks": data.get("attacks", data.get("ats")),
            "weapon_skill": data.get("weapon_skill", data.get("ws")),
            "strength": data.get("strength", data.get("s")),
            "armour_penetration": data.get(
                "armour_penetration",
                data.get("ap"),
            ),
            "damage": data.get("damage", data.get("dmg")),
        }


class DefenderRepository:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    def _resolve_path(self, filename):
        if os.path.isabs(filename):
            return filename
        return os.path.join(self.script_dir, filename)

    def save_defender(self, defender, filename):
        filepath = self._resolve_path(filename)
        data = {
            "name": defender.name,
            "toughness": defender.toughness,
            "wounds": defender.wounds,
            "save": defender.save,
            "invulnerable_save": defender.invulnerable_save,
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_defender(self, filename):
        filepath = self._resolve_path(filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        data = self._normalize_defender_data(data)
        return Defender(**data)

    def save_defenders(self, defenders, filename):
        filepath = self._resolve_path(filename)
        data = [
            {
                "name": d.name,
                "toughness": d.toughness,
                "wounds": d.wounds,
                "save": d.save,
                "invulnerable_save": d.invulnerable_save,
            }
            for d in defenders
        ]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_defenders(self, filename):
        filepath = self._resolve_path(filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Defender(**self._normalize_defender_data(d)) for d in data]

    def _normalize_defender_data(self, data):
        return {
            "name": data["name"],
            "toughness": data.get("toughness", data.get("t")),
            "wounds": data.get("wounds", data.get("w")),
            "save": data.get("save", data.get("sv")),
            "invulnerable_save": data.get(
                "invulnerable_save",
                data.get("inv_sv"),
            ),
        }
