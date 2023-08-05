# spatial
from stuphos.runtime import Object

class Space:
	def __init__(self, length, width, height):
		# Exterior dimension.
		self.length = length
		self.width = width
		self.height = height

class Shape(Space):
	pass

class Structure(Object, Shape, list):
	def __init__(self, rooms):
		list.__init__(self, rooms)

	def scanForTransportTargets(self):
		pass

class Ship(Structure):
	pass


class physical:
	# Ideally, this is implemented on metal which also calculates its own timeframe.
	def __init__(self, frame):
		# Construct a new space state.
		pass

	def run(self, timeframe = None):
		# Process physical space for timeframe.

		# Time is calculated by implementation -- which should parallelize
		# and schedule this method call so that it can accurately keep time:
		# doing so by merely pushing invocations of timeframe-runs in a
		# sequentially-executed manner.
		pass
