import random


class CombatSimulator:
    def __init__(self, hit_roller, wound_roller, save_roller):
        self.hit_roller = hit_roller
        self.wound_roller = wound_roller
        self.save_roller = save_roller

    def simulate_combat(
        self,
        weapon,
        defender,
        weapon_count=1,
        defender_count=1,
        trials=10000,
    ):
        total_damage = 0
        kills = 0
        rng = getattr(self.hit_roller, "_rng", random)

        for _ in range(trials):
            total_attacks = sum(
                weapon.roll_attacks(rng)
                for _ in range(weapon_count)
            )
            hits = self.hit_roller.roll(
                total_attacks,
                weapon.weapon_skill,
            )
            wounds = self.wound_roller.roll(
                hits, weapon.strength, defender.toughness)
            failed_saves = self.save_roller.roll(
                wounds,
                defender.save,
                weapon.armour_penetration,
                defender.invulnerable_save,
            )
            damage_rolls = [weapon.roll_damage(
                rng) for _ in range(failed_saves)]
            damage = sum(damage_rolls)
            total_damage += damage

            if defender.wounds == 1:
                if failed_saves >= defender_count:
                    kills += 1
            else:
                wounds_per_model = [0 for _ in range(defender_count)]
                for rolled_damage in damage_rolls:
                    for i in range(defender_count):
                        if wounds_per_model[i] < defender.wounds:
                            wounds_per_model[i] += rolled_damage
                            break
                models_killed = sum(
                    1 for w in wounds_per_model if w >= defender.wounds)
                if models_killed == defender_count:
                    kills += 1

        return {
            "avg_damage": total_damage / trials,
            "kill_chance": kills / trials,
        }

    def simulate_armies(self, attacker_groups, defender, defender_count, trials=10000):
        if not attacker_groups:
            raise ValueError("Attacker groups are required.")

        rng = getattr(self.hit_roller, "_rng", random)
        total_damage = 0
        kills = 0

        for _ in range(trials):
            alive_defenders = [
                {
                    "profile": defender,
                    "remaining_wounds": defender.wounds,
                }
                for _ in range(defender_count)
            ]

            trial_damage = 0

            for weapon, count in attacker_groups:
                for _i in range(count):
                    attacks = weapon.roll_attacks(rng)
                    for _j in range(attacks):
                        if not alive_defenders:
                            break

                        target_index = rng.randint(0, len(alive_defenders) - 1)
                        target = alive_defenders[target_index]
                        target_profile = target["profile"]

                        hits = self.hit_roller.roll(1, weapon.weapon_skill)
                        if hits == 0:
                            continue

                        wounds = self.wound_roller.roll(
                            hits,
                            weapon.strength,
                            target_profile.toughness,
                        )
                        if wounds == 0:
                            continue

                        failed_saves = self.save_roller.roll(
                            wounds,
                            target_profile.save,
                            weapon.armour_penetration,
                            target_profile.invulnerable_save,
                        )

                        for _k in range(failed_saves):
                            damage = weapon.roll_damage(rng)
                            trial_damage += damage
                            target["remaining_wounds"] -= damage
                            if target["remaining_wounds"] <= 0:
                                alive_defenders.pop(target_index)
                                break

            total_damage += trial_damage
            if not alive_defenders:
                kills += 1

        return {
            "avg_damage": total_damage / trials,
            "kill_chance": kills / trials,
        }


def create_simulator(roller_factory):
    return CombatSimulator(
        roller_factory.create_hit_roller(),
        roller_factory.create_wound_roller(),
        roller_factory.create_save_roller(),
    )
