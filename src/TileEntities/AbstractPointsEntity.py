from TileEntities.Abstract import Abstract

class AbstractPointsEntity(Abstract):
	pointsTotal = 0

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.points = self.pointsTotal
	
	# reward some entity with points
	def rewardPoints(self, reward: int):
		self.points += reward

	# punish some entity by removing points
	def removePoints(self, remove: int):
		self.points -= remove

	@property
	def currentPoints(self):
		return self.points
