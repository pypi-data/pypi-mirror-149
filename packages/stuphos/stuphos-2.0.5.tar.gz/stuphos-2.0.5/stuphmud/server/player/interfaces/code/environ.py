
from contextlib import contextmanager
from types import GeneratorType as generator

def withAs(ctx):
	with ctx as f:
		return f

@contextmanager
def instdict(inst):
	'Create a context variable access out of the variable dictionary.'
	yield inst.__dict__

class Environment(object):
	from new import instance

	class Options:
		from pprint import pformat as pf
		pf = staticmethod(pf)

		def __repr__(self):
			return '<Environment.Options %s>' % self.pf(self.__dict__)

	def __init__(self, avatar, attr = ('env', 'e'), **options):
		self.avatar = avatar

		self.__options = options = dict(options)
		self.options = self.o = self.instance(self.Options, options)

		if type(attr) in (list, tuple, generator):
			for a in attr:
				setattr(avatar, a, self)

		elif type(attr) is str:
			setattr(avatar, attr, self)

	def __getattr__(self, name):
		return self.avatar.find(name, **self.__options)

	def __repr__(self):
		return '<Environment lookup %r>' % self.avatar.find

	def presearch(self, *args):
		'Presearch the environment.'
		return dict((k, getattr(self, k)) for k in args)

	@property
	@contextmanager
	def __context__(self):
		'''
		with mobile.e as e:
			print e.fido, e.wyrm, e.zifnab

		with instdict(mobile.e.presearch(*args)) as p:
			print p # The presearched dictionary result.

		'''
		yield self

ment = Environment
