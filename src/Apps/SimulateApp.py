from Apps.Abstract import Abstract as AbstractApp
import os
from Apps.TrainingApp import TrainingApp
from GridWorld import GridWorld
from TileEntities.AbstractTrainableEntity import AbstractTrainableEntity
from TileEntities.Monster import Monster
from Graphics.Abstract import Abstract as AbstractGraphics
from Utils.Cli import commandLineArgs
import threading
import time
import json

class SimulateApp(AbstractApp):
	def start(self):
		mapPath = os.path.join(os.getcwd(), '../dungeons/', commandLineArgs.map + '.txt')
		self.world = GridWorld(fromFile = mapPath, logging = commandLineArgs.logging)
		teamSortOrder = ['agent', 'monster', 'gaia']
		self.world.teamList.sort(key = lambda item: teamSortOrder.index(item))
		for entity in self.world.entities:
			if isinstance(entity, AbstractTrainableEntity):
				self.loadAI(entity)

		displayClass = commandLineArgs.display
		self.renderer: AbstractGraphics = displayClass(self.world)

		t = threading.Thread(target = self.runWorld)
		t.daemon = True
		t.start()

		self.createWindow()

	def loadAI(self, entity):
		aiPath = os.path.join(os.getcwd(), '../ai/', commandLineArgs.trainClass.__name__ + '_' + entity.__class__.__name__ + '.json')
		if not os.path.exists(aiPath):
			print(aiPath)
			raise 'AI path not found. Do some training first'

		f = open(aiPath, 'r')
		try:
			weights = json.loads(f.read())
			for i in weights:
				entity.weights[i] = weights[i]

			print('loaded AI file for ', entity.__class__.__name__)
		finally:
			f.close()

	def createWindow(self):
		self.renderer.start()

	def runWorld(self):
		while len(self.world.teams['agent']) > 0:
			if self.world.ticks > 100:
				break

			self.world.tick()
			self.renderer.render()
			time.sleep(commandLineArgs.speed)

		if len(self.world.teams['agent']) > 0:
			print('quit because iterations exceeded max')
		else:
			print('quit because game over')