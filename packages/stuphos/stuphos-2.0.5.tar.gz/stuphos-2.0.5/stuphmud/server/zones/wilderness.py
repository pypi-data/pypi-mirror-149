# StuphMUD 3.0/4.0 Wilderness System.
from stuphos.runtime.facilities import Facility
from stuphmud.server.player import ACMD

# Each room possesses a grid or a collection of grids (rectangle) that define the wilderness shape.
# Each room may possess a relative exterior dimension.
# Each mobile and item possesses a 'spatial' diagram (instance) for describing their location.

class Shape(list):
	class Grid:
		def __init__(self, start, dimensions):
			(startX, startY) = start
			self.start = (startX, startY)
			(width, height) = dimensions
			self.dimensions = (width, height)

		class Tile:
			def __init__(self, xy, code):
				self.code = code

		def __getitem__(self, xy):
			return self.Tile(xy, self.getTileCode(xy[0], xy[1]))

	def __init__(self, size, *grids):
		list.__init__(self, grids)
		(exteriorWidth, exteriorHeight) = size
		self.exterior = (exteriorWidth, exteriorHeight)

class Terrain(Shape):
	def getDefaultTileCode(self):
		pass

	class Grid(Shape.Grid):
		class Tile(Shape.Grid.Tile):
			pass

		def getDefaultTile(self, x, y):
			pass

class WildernessSystem(Facility):
	NAME = 'MUD::Wilderness'

	class Manager(Facility.Manager):
		VERB_NAME = 'wild*erness'
		MINIMUM_LEVEL = Facility.Manager.IMPLEMENTOR

	def __init__(self):
		self.dirOptionAssigns = [ACMD('n*orth')(self.doGoNorth),
								 ACMD('s*outh')(self.doGoSouth),
								 ACMD('e*ast')(self.doGoEast),
								 ACMD('w*est')(self.doGoWest),
								 ACMD('u*p')(self.doGoUp),
								 ACMD('d*own')(self.doGoDown)]

		from stuphos import on
		on.lookAtRoom(self.lookAtRoom)

    # Movement -- the Heart of Wilderness.

	def doGoNorth(self, peer, cmd, argstr):
		pass
	def doGoSouth(self, peer, cmd, argstr):
		pass
	def doGoEast(self, peer, cmd, argstr):
		pass
	def doGoWest(self, peer, cmd, argstr):
		pass
	def doGoUp(self, peer, cmd, argstr):
		pass
	def doGoDown(self, peer, cmd, argstr):
		pass

	def lookAtRoom(self, player):
		pass
