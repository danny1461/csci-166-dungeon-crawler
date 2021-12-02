from Graphics.Abstract import Abstract
from GridWorld import GridWorld
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.Agent import Agent
from TileEntities.Monster import Monster
from TileEntities.SpikeTrap import SpikeTrap
from tkinter import *

class Window(Abstract):
	tileSize = 50

	def __init__(self, gridWorld: GridWorld):
		super().__init__(gridWorld)
		self.layers = []
		self.entities = {}

		self.master = Tk()
		self.board = Canvas(self.master, width = gridWorld.width * self.tileSize, height = gridWorld.height * self.tileSize)
		self.board.grid(row=0, column=0)

		self.renderStatic()

	def start(self):
		self.master.mainloop()

	def renderLayerItem(self, layer, command, coords, **kwargs):
		layer_tag = "layer " + str(layer)
		if layer_tag not in self.layers:
			self.layers.append(layer_tag)
		tags = kwargs.setdefault("tags", [])
		tags.append(layer_tag)

		id = command(coords, **kwargs)
		for layer in sorted(self.layers):
			self.board.lift(layer)

		return id

	def getEntityCoords(self, entity):
		size = 10
		if isinstance(entity, SpikeTrap):
			size = 5

		return (
			entity.x * self.tileSize + size,
			entity.y * self.tileSize + size,
			(entity.x + 1) * self.tileSize - size,
			(entity.y + 1) * self.tileSize - size
		)

	def createEntityReferences(self):
		for entity in self.gridWorld.entities:
			layer = 1
			if isinstance(entity, Agent):
				fill = 'yellow'
			elif isinstance(entity, Monster):
				fill = 'red'
			elif isinstance(entity, SpikeTrap):
				layer = 0
				fill = 'gray'

			rect = self.renderLayerItem(
				layer,
				self.board.create_rectangle,
				self.getEntityCoords(entity),
				fill = fill, width = 1, tag = entity.id
			)

			self.entities[entity] = {
				'main': rect
			}

			if isinstance(entity, AbstractHitpointEntity):
				self.entities[entity.id]['health'] = self.renderLayerItem(
					layer,
					self.board.create_text,
					(
						entity.x * self.tileSize + (self.tileSize / 2),
						entity.y * self.tileSize + (self.tileSize / 2)
					),
					fill = 'black', font = 'Times 14', text = entity.health
				)

	def renderStatic(self):
		for x in range(self.gridWorld.width):
			for y in range(self.gridWorld.height):
				tile = self.gridWorld.getTileData( (x, y) )[0]
				self.drawTile(x, y, tile)

		self.createEntityReferences()

	def render(self):
		toRemove = []

		for entity in self.entities:
			if entity not in self.gridWorld.entities:
				toRemove.append(entity)
				for i in self.entities[entity]:
					self.board.delete(self.entities[entity][i])
			else:
				self.updateTileEntity(entity)

		for entity in toRemove:
			self.entities.pop(entity)
	
	def drawTile(self, x, y, tileItem):
		match tileItem:
			case ' ':
				fill = 'white'
			case 'W':
				fill = 'black'
			case 'E':
				fill = 'green'

		self.board.create_rectangle(x * self.tileSize, y * self.tileSize, (x + 1) * self.tileSize, (y + 1) * self.tileSize, fill = fill, width = 1)

	def updateTileEntity(self, entity):
		data = self.entities[entity]
		self.board.coords(data['main'], *self.getEntityCoords(entity))

		if 'health' in data:
			self.board.coords(data['health'], entity.x * self.tileSize + (self.tileSize / 2), entity.y * self.tileSize + (self.tileSize / 2))
			self.board.itemconfigure(data['health'], text = entity.health)