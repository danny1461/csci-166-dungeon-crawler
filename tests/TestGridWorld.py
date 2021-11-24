from unittest import TestCase
from context import GridWorld

class Test(TestCase):
	def test_loadMapString_width_height(self):
		g = GridWorld('./dungeons/empty.txt')
		self.assertEquals(g.width, 2, 'Width should be 2')
		self.assertEquals(g.height, 2, 'Height should be 2')

	def test_loadMapString_content(self):
		g = GridWorld('./dungeons/empty.txt')
		for i in range(2):
			for j in range(2):
				self.assertEquals(g.getTileData( (i, j) )[0], ' ', '4 Blank spaces')