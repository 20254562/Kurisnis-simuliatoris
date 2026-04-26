import random
from abc import ABC, abstractmethod


class RollStrategy(ABC):
    @abstractmethod
    def roll(self, *args, **kwargs):
        pass


class HitRoller(RollStrategy):
    def __init__(self, rng=None):
        self._rng = rng or random

    def roll(self, attacks, weapon_skill):
        if weapon_skill is None:
            return attacks
        rolls = [self._rng.randint(1, 6) for _ in range(attacks)]
        return sum(1 for roll in rolls if roll >= weapon_skill)


class WoundRoller(RollStrategy):
    def __init__(self, rng=None):
        self._rng = rng or random

    
    def get_wound_threshold(self, strength, toughness):
        if strength >= 2 * toughness:
            return 2
        if strength > toughness:
            return 3
        if strength == toughness:
            return 4
        if strength * 2 <= toughness:
            return 6
        return 5

    def roll(self, hits, strength, toughness):
        threshold = self.get_wound_threshold(strength, toughness)
        rolls = [self._rng.randint(1, 6) for _ in range(hits)]
        return sum(1 for roll in rolls if roll >= threshold)


class SaveRoller(RollStrategy):
    def __init__(self, rng=None):
        self._rng = rng or random

    def roll(
            self,
            wounds,
            armor_save,
            armour_penetration=0,
            invulnerable=None):
        effective_save = armor_save + armour_penetration
        if invulnerable is not None:
            effective_save = min(effective_save, invulnerable)
        effective_save = min(effective_save, 7)
        rolls = [self._rng.randint(1, 6) for _ in range(wounds)]
        successful_saves = sum(1 for roll in rolls if roll >= effective_save)
        return wounds - successful_saves
