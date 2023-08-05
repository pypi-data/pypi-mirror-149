#!/usr/local/bin/python
'Implements command searching with abbreviation management.  See CmdDict.'

# Override UserDict?
class CmdDict:
	'''
	Briefly, it encapsulates a command set dictionary that any command or
	abbreviation of a command will map to value.

	Insert control is provided for expressing abbreviated forms and those
	commands already present in the command set acceptable for overriding.

	And override is where one command abbreviation mapping is replaced with
	another according to the rules of insert[Overriding].

	'''

	# What method to use when using decorator assignment of functions.
	assignmentMethod = 'OverridingAll' # 'Overriding' # ''

	def __init__(self, c = None, assignment = None):
		# Forcing dict type:
		if c is None:
			c = self.c = dict()
		else:
			self.c = c

		self.__getitem__ = c.__getitem__
		self.__setitem__ = c.__setitem__

		# Decide assignment method.
		self.insertAssignment = getattr(self, 'insert' + (assignment or self.assignmentMethod))

	@staticmethod
	def abbreviations(*args):
		'''
		For each positional argument, generate a number of abbreviated
		forms, from longest to shorted, until the end 

		Each argument be either:
			- A 2-tuple:
			  ('command-name', end)
			  Where end is the ending index of the command name to stop abbreviations.

			- A string describing verb abbreviations (from lambda moo):
			  verb*name
			  The abbreviations are generated from the full name down to the asterisk.

			- A plain string.  All possible abbreviations will be generated down to
			  the first letter.  Useful for overriding the movement or violence commands.

		'''

		for m in args:
			if type(m) is tuple and len(m) == 2:
				# Only yield up to explicit column.
				m, end = m
				while len(m) >= end:
					yield m
					m = m[:-1]
			elif '*' in m:
				# Detect end column from 'verb*name' form.
				end = m.index('*') # -1 ?
				m = m.replace('*', '')
				while len(m) >= end:
					yield m
					m = m[:-1]
			else:
				# Use every possible abbreviation.
				while m:
					yield m
					m = m[:-1]

	class Registration(list):
		def __init__(self, cmddict, name):
			self.name = name
		def __repr__(self):
			return '<%s %r (%d assignments)>' % (self.__class__.__name__, self.name, len(self))

		@property
		def current(self):
			return self[-1]

		def __hash__(self):
			h = 0
			for r in self:
				h ^= hash(r)
			return h

		def __add__(self, assignment):
			self.append(assignment)
			return len(self)-1

		def __call__(self, *args, **kwd):
			return self.current(*args, **kwd) # overriding all

		def remove(self, index = None):
			if index is None:
				del self[:]
			else:
				try: list.__delitem__(self, index)
				except IndexError:
					pass

			return len(self) == 0

	def register(self, name, assignment):
		try: c = self.c[name]
		except KeyError:
			self.c[name] = c = self.Registration(self, name)

		return c + assignment

	def insert(self, m, a = None):
		'Insert abbreviations of command name into command set not overriding anything.'

		c = self.c
		a = a or m

		for x in self.abbreviations(m.lower()):
			# Overwrite not desired for any existing entries.
			if x not in c:
				c[x] = a

	def insertOverriding(self, m, a = None, *overriding):
		'''
		Insert only if command is either not already in command-set, or is part of overriding.

		Overriding arguments can be delivered as an abbreviation list:
		insertOverriding('the-*first-command', doCmd, *abbreviations('the-*second-command', 'the-*third-command))

		'''

		c = self.c
		a = a or m

		if overriding:
			s = set(self.abbreviations(overriding))

			for x in self.abbreviations(m.lower()):
				# Override all forms for those specified in trailing arguments.
				if x in s or x not in c:
					c[x] = a
		else:
			for x in self.abbreviations(m.lower()):
				# Reverse order invoking this function no overwrite worry.
				c[x] = a

	def insertOverridingAll(self, m, a = None):
		'Insert abbreviations of command name into command set overriding any and all.'

		c = self.c
		a = a or m

		r = []
		for x in self.abbreviations(m.lower()):
			r.append((x, self.register(x, a)))

		return r

	def lookup(self, cmd, default = None):
		'Looks for command name in the command set dictionary or returns a default value.'

		return self.c.get(cmd, default)

	def assign(self, *verbNames, **req):
		# Decorator for assignment, using free cell variable.
		assign = self.insertAssignment

		def invokeInsert(function):
			r = []
			for form in verbNames:
				for e in assign(str(form), function, **req):
					r.append(e)

			return self.Assignment(self, function, verbNames, *r)
			return function

		return invokeInsert

	assignRemoveable = assign

	class Assignment(list):
		def __init__(self, cmddict, function, verbNames, *registrations):
			list.__init__(self, registrations)
			self.cmddict = cmddict
			self.function = function
			self.verbNames = verbNames

		def __call__(self, *args, **kwd):
			return self.function(*args, **kwd)

		def remove(self): # , index = None):
			for (a, r) in self:
				self.cmddict.remove(a, r)

	@staticmethod
	def parse(cmd):
		'''Parses a MUD command considering non-alphanumeric first characters.
		Returns 2-tuple (command-name, argstr)'''

		cmd = cmd.lstrip()
		if not cmd:
			return (None, None)

		x = cmd[0]
		if not x.isalpha():
			return x, cmd[1:]

		x = cmd.find(' ')
		if x >= 0:
			return cmd[:x].lower(), cmd[x+1:]

		return cmd.lower(), None

	def remove(self, abbrev, index = None):
		try: r = self.c[abbrev]
		except KeyError: pass

		if r.remove(index = index):
			del self.c[abbrev]

	# def remove(self, match):
	# 	c = self.c
	# 	for n in [n for (n, v) in c.iteritems() if v == match]: # v is match?
	# 		c[n].remove(c, n)

	def removeByLookup(self, name):
		cmdfunc = self.lookup(name)
		if cmdfunc is not None:
			self.remove(cmdfunc)

# Testing
if __name__ == '__main__':
	from sys import stdin
	from consoleInteractive import *
	from Timing import Timing

	from pprint import pprint as pp
	from pdb import run, runcall

	cmds = CmdDict()

	@Timing('Multiple Command Load : %(SECONDS)d.%(MICRO)06d')
	def load(n, i = cmds.insertOverriding):
		for x in n:
			i(x)

	@Timing('Command Search : %(SECONDS)d.%(MICRO)06d')
	def lookup(n):
		n, argstr = cmds.parse(n)
		return cmds.lookup(n), argstr

	# Initial load.
	loadedCmds = list(input_cmdln())
	loadedCmds.reverse()

	for x in range(10):
		cmds.c = {}
		load(loadedCmds)

	def matchAll(x):
		buf = __import__('cStringIO').StringIO()
		for (k, v) in cmds.data().items():
			if v.startswith(x):
				print('%-20s' % k, ':', v, file=buf)
		page(buf.getvalue())

	for n in getline():
		if shellCommand(n, globals()):
			continue

		print(lookup(n))
