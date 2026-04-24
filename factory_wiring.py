
from persistence import DefenderRepository, WeaponRepository
from rolling import HitRoller, SaveRoller, WoundRoller
from simulation import create_simulator


class RollerFactory:
    def create_hit_roller(self):
        raise NotImplementedError

    def create_wound_roller(self):
        raise NotImplementedError

    def create_save_roller(self):
        raise NotImplementedError


class StandardRollerFactory(RollerFactory):
    def __init__(self, rng=None):
        self._rng = rng

    def create_hit_roller(self):
        return HitRoller(rng=self._rng)

    def create_wound_roller(self):
        return WoundRoller(rng=self._rng)

    def create_save_roller(self):
        return SaveRoller(rng=self._rng)



class AppWiring:
    def __init__(self, weapon_repo, defender_repo, simulator):
        self.weapon_repo = weapon_repo
        self.defender_repo = defender_repo
        self.simulator = simulator


def build_app_wiring(rng=None):
    roller_factory = StandardRollerFactory(rng=rng)
    simulator = create_simulator(roller_factory)
    return AppWiring(
        weapon_repo=WeaponRepository(),
        defender_repo=DefenderRepository(),
        simulator=simulator,
    )
