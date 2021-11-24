from .Abstract import Abstract

class AbstractHitpointEntity(Abstract):
	traversable = False
	maxHitPoints = 100

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.health = type(self).maxHitPoints

	def damage(self, amount):
		self.health = max(0, self.health - amount)

	def heal(self, amount):
		self.health = min(type(self).maxHitPoints, self.health + amount)

	@property
	def isDead(self):
		return self.health <= 0