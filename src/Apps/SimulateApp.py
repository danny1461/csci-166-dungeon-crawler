from Apps.Abstract import Abstract as AbstractApp
import os
from Apps.TrainingApp import TrainingApp
from GridWorld import GridWorld
from TileEntities.Monster import Monster
from Utils.Cli import commandLineArgs

class SimulateApp(AbstractApp):
	def start(self):
		mapPath = os.path.join(os.getcwd(), '../dungeons/', commandLineArgs.map + '.txt')
		world = GridWorld(fromFile = mapPath, logging = commandLineArgs.logging)
		teamSortOrder = ['agent', 'monster', 'gaia']
		world.teamList.sort(key = lambda item: teamSortOrder.index(item))

		while len(world.teams['agent']) > 0:
			if world.ticks > 100:
				break

			world.tick()

		if len(world.teams['agent']) > 0:
			print('quit because iterations exceeded max')