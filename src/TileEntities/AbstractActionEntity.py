from TileEntities.Abstract import Abstract

class AbstractActionEntity(Abstract):
    # cost of turns for an action
    actionCost = 1
    chanceSuccess = False

    def __init__(self, *args, **kwargs):
	    super().__init__(*args, **kwargs)
	    self.cost = type(self).actionCost + 1

    # an action counter for the point cost (resets to pointCost at 0)
    def actionCounter(self, pointCost):
        if (self.tookAction):
            self.cost = pointCost + 1
            self.log('Entity {} takes an action'.format(self.__class__.__name__))
        self.cost -= 1

    # sucess of a random action being taken
    def actionChance(self, percentChance):
        self.chanceSuccess = (percentChance >= self.randomPercent)
        self.log('Entity {} takes a chance of {}%'.format(self.__class__.__name__, percentChance * 100))

    @property
    def tookAction(self):
        return bool(self.cost == 0)

    @property
    def chanceSuccessful(self):
        return self.chanceSuccess