from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from GridWorld import GridWorld

from abc import ABC, abstractmethod

class Abstract(ABC):
	nextId = 1

	traversable = True
	team = 'gaia'

	def __init__(self, gridWorld: GridWorld):
		self.id = Abstract.nextId
		Abstract.nextId += 1

		self.gridWorld = gridWorld

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

	# get the current turn of the world 
	@property
	def turn(self):
		return int(self.gridWorld.ticks / len(self.gridWorld.entities)) + 1

	@abstractmethod
	def tick(self):
		pass

	def log(self, *args):
		self.gridWorld.log(*args)

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