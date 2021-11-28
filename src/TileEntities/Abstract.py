from __future__ import annotations
from os import stat
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from GridWorld import GridWorld

from abc import ABC, abstractmethod
from copy import copy
from Decorators.Events import classEvents

@classEvents('onAction')
class Abstract(ABC):
	nextId = 1

	traversable = True
	team = 'gaia'

	def __init__(self, gridWorld: GridWorld):
		self.id = Abstract.getNextEntityId()

		self.gridWorld = gridWorld

	def clone(self):
		"""
			Returns a replica instance but with a new Entity Id
		"""
		clone = copy(self)
		clone.id = Abstract.getNextEntityId()
		return clone

	def __hash__(self):
		return self.id

	def __eq__(self, other):
		if isinstance(other, Abstract):
			return self.id == other.id
		return self.id == other

	@property
	def pos(self):
		return self.gridWorld.getTileEntityLocation(self)

	@property
	def x(self):
		return self.gridWorld.getTileEntityLocation(self)[0]

	@property
	def y(self):
		return self.gridWorld.getTileEntityLocation(self)[1]

	@property
	def nearbyTiles(self):
		return self.gridWorld.getNearbyTiles(self.gridWorld.getTileEntityLocation(self))

	@abstractmethod
	def tick(self):
		pass

	def log(self, *args):
		self.gridWorld.log(*args)

	def triggerEvent(self, evtName, **kwargs):
		self.onAction.fire(self, evtName, kwargs)

	def searchTile(self, tileIteratable, predicate):
		if isinstance(predicate, type):
			cls = predicate
			predicate = lambda tile: any([isinstance(tileItem, cls) for tileItem in self.gridWorld.getTileData(tile)])

		for tile in tileIteratable:
			if predicate(tile):
				yield tile

	def searchTileFirst(self, tileIterable, predicate):
		for tile in self.searchTile(tileIterable, predicate):
			return tile

		return None

	def searchTileItem(self, tileIterable, predicate):
		if isinstance(predicate, type):
			cls = predicate
			predicate = lambda tileItem: isinstance(tileItem, cls)
		elif type(predicate) == str:
			tileChar = predicate
			predicate = lambda tileItem: tileItem == tileChar

		for tile in tileIterable:
			for tileItem in self.gridWorld.getTileData(tile):
				if predicate(tileItem):
					yield (tileItem, tile)

	def searchTileItemFirst(self, tileIterable, predicate):
		for data in self.searchTileItem(tileIterable, predicate):
			return data

		return (None, None)

	@property
	def isTrackingActions(self):
		return self.gridWorld.isTrackingActions

	def trackUndoAction(self, undoFn):
		self.gridWorld.trackUndoAction(undoFn)

	@staticmethod
	def getNextEntityId():
		try:
			return Abstract.nextId
		finally:
			Abstract.nextId += 1

	@staticmethod
	def resetNextEntityId():
		Abstract.nextId = 1