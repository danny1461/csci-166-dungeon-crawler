from GridWorld import GridWorld

class Console:
	def __init__(self, world: GridWorld):
		self.gridWorld = world

	def render(self):
		print('')
		for y in range(self.gridWorld.height):
			for x in range(self.gridWorld.width):
				for tileItem in self.gridWorld.getTileData( (x, y) ):
					if type(tileItem) == str:
						if tileItem == ' ':
							continue

						print(tileItem, end = '')
						break
					elif type(tileItem) in GridWorld.tileEntityMap:
						print(GridWorld.tileEntityMap[type(tileItem)], end = '')
						break
					
				else:
					print(' ', end = '')

			print('')