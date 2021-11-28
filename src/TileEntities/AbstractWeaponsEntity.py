from TileEntities.Abstract import Abstract
from TileEntities.Agent import Agent

class AbstractWeaponEntity(Abstract):
    weaponName = "default_weapon"
    baseDamage = 10
    damageMultiplier = 2.0
    distanceReach = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage = self.baseDamage
        self.multiplier = self.damageMultiplier
        self.distance = self.distanceReach
        self.charge = self.chargeTime

    def isPossible(self, distance, enemy: Agent):
        a=1
