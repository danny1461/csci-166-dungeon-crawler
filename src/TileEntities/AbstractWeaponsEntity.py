from TileEntities.Abstract import Abstract
from Aliases import Tile

class AbstractWeaponEntity(Abstract):
    weaponName = "default_weapon"
    weaponDamage = 10
    weaponReach = 1
    weaponAttackPossible = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wepdamage = type(self).weaponDamage
        self.wepdistance = type(self).weaponReach
        self.attackable = type(self).weaponAttackPossible

    # can our weapon reach the target
    def setIfWeaponReachTarget(self, targetPos: Tile):
        if (self.isBlineTraceable(self.pos, targetPos)):
            if (self.isInRange(self.pos, targetPos, self.wepdistance)):
                self.attackable = True
            else:
                self.attackable = False
        else:
            self.attackable = False

    @property
    def weaponDoesHit(self):
        return self.attackable
