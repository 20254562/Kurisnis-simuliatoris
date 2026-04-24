import unittest

from domain import Defender, Weapon
from factory_wiring import RollerFactory, StandardRollerFactory
from rolling import HitRoller, RollStrategy
from simulation import CombatSimulator, create_simulator


class FixedRng:
    def __init__(self, value):
        self.value = value

    def randint(self, _a, _b):
        return self.value


class DummyHitRoller(RollStrategy):
    def roll(self, attacks, weapon_skill):
        return attacks


class DummyWoundRoller(RollStrategy):
    def get_wound_threshold(self, strength, toughness):
        return 4

    def roll(self, hits, strength, toughness):
        return hits


class DummySaveRoller(RollStrategy):
    def roll(
        self,
        wounds,
        armor_save,
        armour_penetration=0,
        invulnerable=None,
    ):
        return wounds


class DummyFactory(RollerFactory):
    def create_hit_roller(self):
        return DummyHitRoller()

    def create_wound_roller(self):
        return DummyWoundRoller()

    def create_save_roller(self):
        return DummySaveRoller()


class SimulationCoreTests(unittest.TestCase):
    def test_weapon_validation_rejects_invalid_ws(self):
        with self.assertRaises(ValueError):
            Weapon("Bad Weapon", 2, 1, 4, 0, 1)

    def test_defender_validation_rejects_invalid_save(self):
        with self.assertRaises(ValueError):
            Defender("Bad Defender", 4, 2, 7)

    def test_factory_method_builds_simulator(self):
        simulator = create_simulator(DummyFactory())
        self.assertIsInstance(simulator.hit_roller, DummyHitRoller)
        self.assertIsInstance(simulator.wound_roller, DummyWoundRoller)
        self.assertIsInstance(simulator.save_roller, DummySaveRoller)

    def test_polymorphism_via_strategy_interfaces(self):
        simulator = CombatSimulator(
            DummyHitRoller(),
            DummyWoundRoller(),
            DummySaveRoller(),
        )
        weapon = Weapon("Sword", 2, 3, 4, 0, 1)
        defender = Defender("Marine", 4, 1, 3)
        result = simulator.simulate_combat(
            weapon,
            defender,
            weapon_count=1,
            defender_count=1,
            trials=1,
        )
        self.assertEqual(result["avg_damage"], 2)
        self.assertEqual(result["kill_chance"], 1)

    def test_standard_factory_with_fixed_rng_is_deterministic(self):
        factory = StandardRollerFactory(rng=FixedRng(6))
        simulator = create_simulator(factory)
        weapon = Weapon("Bolter", 2, 3, 4, 0, 1)
        defender = Defender("Guard", 3, 1, 6)
        result = simulator.simulate_combat(
            weapon,
            defender,
            weapon_count=1,
            defender_count=1,
            trials=1,
        )
        self.assertEqual(result["avg_damage"], 0)
        self.assertEqual(result["kill_chance"], 0)

    def test_weapon_supports_requested_roll_formats(self):
        valid_attacks = [
            "D3",
            "D6",
            "2D6",
            "3D3",
            "D6+2",
            "D3+1",
            "2D6+3",
            "4D3+2",
        ]
        for expr in valid_attacks:
            weapon = Weapon("Expr", expr, 3, 4, 0, "1")
            self.assertEqual(weapon.attacks, expr)

        valid_damage = ["D3", "D6", "2D6", "D6+2", "2D3+1"]
        for expr in valid_damage:
            weapon = Weapon("Expr", "1", 3, 4, 0, expr)
            self.assertEqual(weapon.damage, expr)

    def test_weapon_rejects_invalid_roll_formats(self):
        with self.assertRaises(ValueError):
            Weapon("Bad", "D4", 3, 4, 0, 1)
        with self.assertRaises(ValueError):
            Weapon("Bad", "2D8", 3, 4, 0, 1)
        with self.assertRaises(ValueError):
            Weapon("Bad", "D6-1", 3, 4, 0, 1)
        with self.assertRaises(ValueError):
            Weapon("Bad", "abc", 3, 4, 0, 1)

    def test_roll_attacks_and_damage_with_fixed_rng(self):
        weapon = Weapon("Roller", "2D3+1", 3, 4, 0, "D6+2")
        rng = FixedRng(3)
        self.assertEqual(weapon.roll_attacks(rng), 7)
        self.assertEqual(weapon.roll_damage(rng), 5)

    def test_empty_weapon_skill_means_all_hits(self):
        roller = HitRoller(rng=FixedRng(1))
        self.assertEqual(roller.roll(7, None), 7)

        weapon = Weapon("AutoHit", "7", "", 4, 0, "1")
        self.assertIsNone(weapon.weapon_skill)

    def test_multi_profile_armies_simulation(self):
        simulator = create_simulator(DummyFactory())
        melta = Weapon("Melta", "1", 3, 8, 0, "2")
        bolter = Weapon("Bolter", "1", 3, 4, 0, "1")
        defender = Defender("Marine", 4, 1, 3)

        result = simulator.simulate_armies(
            attacker_groups=[(melta, 1), (bolter, 4)],
            defender=defender,
            defender_count=5,
            trials=1,
        )

        self.assertGreater(result["avg_damage"], 0)
        self.assertGreaterEqual(result["kill_chance"], 0)
        self.assertLessEqual(result["kill_chance"], 1)


if __name__ == "__main__":
    unittest.main()
