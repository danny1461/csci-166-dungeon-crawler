from TileEntities.Abstract import Abstract

class AbstractHitpointEntity(Abstract):
	traversable = False
	maxHitPoints = 100

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.health = type(self).maxHitPoints

	def damage(self, amount):
		if amount > self.health:
			amount = self.health

		self.triggerEvent('health', health = amount * -1)
		self.health -= amount
		self.log('Entity {} takes {} damage. {} remaining'.format(self.__class__.__name__, amount, self.health))

		if self.isTrackingActions:
			self.trackUndoAction(lambda: self.heal(amount))

	def heal(self, amount):
		self.triggerEvent('health', health = amount)
		self.health += amount
		self.log('Entity {} heals for {} health. {} remaining'.format(self.__class__.__name__, amount, self.health))

		if self.isTrackingActions:
			self.trackUndoAction(lambda: self.damage(amount))

	@property
	def isDead(self):
		return self.health <= 0