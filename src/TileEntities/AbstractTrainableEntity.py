from __future__ import annotations
from abc import abstractmethod
from Aliases import Features
from TileEntities.Abstract import Abstract
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from Apps.TrainingApp import TrainingApp

class AbstractTrainableEntity(Abstract):
	def setTrainer(self, trainer: TrainingApp):
		self.trainer = trainer

	@abstractmethod
	def getAllActions(self):
		pass

	@abstractmethod
	def learnFromExperience(self, priorFeatures: Features, reward: float):
		pass

	def takeAction(self, action):
		fn, args = action
		getattr(self, fn)(*args)

	def simulateActionAndGetFeatures(self, action):
		try:
			self.trainer.startSimulating()
			self.takeAction(action)
			return self.trainer.getFeatures(self)
		finally:
			self.trainer.stopSimulating()
			