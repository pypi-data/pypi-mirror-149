from . import ASPELL

def spell(name, value, **kwd):
	@ASPELL(name, value['max_mana'], value['min_mana'], value['mana_change'],
			value.get('minpos', 'Standing'), value['targets'], value['violent'],
			value.get('wearoff', ''), register = False)

	def girlSpell(spell, caster):
		# todo: programmer
		task = value['manual'](environ = dict(),
							   locals = dict(environment = kwd['container'],
											 caster = caster,
											 victim = None))

		# task.name = '%s' % spell

	return girlSpell
