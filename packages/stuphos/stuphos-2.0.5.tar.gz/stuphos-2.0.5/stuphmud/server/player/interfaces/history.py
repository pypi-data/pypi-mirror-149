class HistoryManager:
	## All history subroutines work on the peer history buffer so require the peer be passed as argument.
	def historyObject(self, peer, create = True):
		# debugOn()
		history = getattr(peer, 'history', None)
		if not history:
			assert create, AttributeError('history')
			history = peer.history = []

		return history

	def historyOverride(self, peer, cmd, argstr):
		'''
		Implements a variety of history-handling functions, executing inline with shellCommand
		by modifying its arguments prior to interpreting them, so as to avoid recursion.

		Returns new parsed command elements or those given.

		These commands are currently parsed only by the shell interpreter and apply only to
		commands invoked therein.  Commands overridden do not effect the outside calling mud
		context.

		'''

		if cmd != '!':
			# Save to history.
			self.historyAdd(peer, cmd, argstr)
			return cmd, argstr

		# args is stripped form of argstr
		args = argstr.strip()

		if not args:
			# Maybe execute last command history -- Or pass to underlying mud code.
			return self.historyLast(peer) or (cmd, args)

		if args[0] == '!':
			# Show history given arguments.
			self.historyShow(peer, args[1:])
			return (None, None)

		elif args.isdigit():
			# Search for command in history and return.
			return self.historyLast(peer, int(args))

		# Todo: allow set by name, and lookup by name, history management.
		i = args.find('=')
		if i >= 0:
			name = args[:i].strip()
			args = args[i+1:].strip()

			if name.isdigit():
				# Replace history position.
				pos = int(name)

				# Make sure position is appropriate within range.
				history = self.historyObject(peer)
				n = len(history)

				if pos < 0 or pos > n:
					print('Position %d out of range! (%d max)' % (pos, n))
				else:
					history[-pos] = self.parseCommand(args)
					print('History %d replaced with %r.' % (pos, args), file=peer)

			elif name:
				# Player's variables
				variables = getattr(peer, 'variables', None)
				if variables is None:
					variables = peer.variables = dict()

				print('Replacing peer variables %s with %s' % (name, args), file=peer)
				variables[name] = args

			else:
				print('Unknown form: = %s' % (args), file=peer)

			return (None, None)

		# Not recognized.
		return cmd, argstr

	def historyLast(self, peer, n = 1):
		if type(n) is int or type(n) is str and n.isdigit():
			return self.historyObject(peer)[-int(n)]

	def historyAdd(self, peer, cmd, argstr):
		history = self.history = self.historyObject(peer)
		history.append((str(cmd or ''), str(argstr or '')))

	def historyShow(self, peer, args, history = None):
		if history is None:
			history = self.historyObject(peer)

		if history:
			end = len(history)

			def historyIterate():
				for x in range(end): # + 1?
					yield x, history[x]

			def joinParse(cmd, argstr):
				if cmd in '0123456789`~!@#$%^&*()-_=+{[}]:;"\'<,>.?/|\\':
					return cmd + argstr

				# Put a space in between.
				return '%s %s' % (cmd, argstr)

			peer.page('\r\n'.join('%-3d : %.80s' % (end - x, joinParse(*h)) for (x, h) in historyIterate()) + '\r\n')

	def historyFilter(self, peer, name = None, onlyArguments = False):
		history = self.historyObject(peer)
		if name is None:
			for (cmd, args) in history:
				yield onlyArguments and args or (cmd, args)

		elif type(name) is str:
			for (cmd, args) in history:
				if cmd == name:
					yield onlyArguments and args or (cmd, args)

		elif type(name) in (tuple, list):
			for (cmd, args) in history:
				if cmd in name:
					yield onlyArguments and args or (cmd, args)

	def historySubstitution(self, peer, line):
		'Eventually parse $<int> $name and $(complex.name) and ${expression block} lines to include the variables/history numbers.'

		def parseHistory(n):
			# Join the command and argument strings.
			return ''.join(self.historyLast(peer, n))

		return self.substitute(line, lookup = parseHistory)
