# def lookupSkill(name):
# 	import game
# 	game.syslog('lookup-skill: %r' % name)

# 	return name

spellTable = dict()

def manualSpell(caster, spell):
	try: callback = spellTable[spell.number]
	except KeyError: pass
	else:
		try: callback(spell, caster)
		except:
			from ph import logException
			logException(traceback = True)

class MaxSkills(ValueError):
	VALUE = 500000 # MAX_SPELLS

def nextAvailableSkillNr(name):
	import world

	for a in world.magic.all_abilities():
		if a.number == 0:
			continue
		if a.name == name: # todo: make this stronger
			return a.number
		if a.name == '!UNUSED!':
			return a.number

	# d = set(a.number for a in world.magic.all_abilities())

	# i = 0
	# while i < MaxSkills.VALUE:
	# 	if i in d:
	# 		i += 1
	# 		continue

	# 	return i

	raise MaxSkills()

def registerSpell(name, max_mana, min_mana, mana_change, minpos,
				  targets, violent, wearoff, callback):

	from world.magic import spello_manual

	nr = nextAvailableSkillNr(name)
	spello_manual(nr, name, max_mana, min_mana, mana_change,
				  minpos, targets, violent, wearoff)

	spellTable[nr] = callback

spello = registerSpell

class Spell:
	name = ''
	max_mana = 0
	min_mana = 0
	mana_change = 0
	minpos = 'standing'
	targets = []
	violent = False
	wearoff = ''

	def __call__(self):
		registerSpell(self.name, self.max_mana, self.min_mana, self.mana_change,
					  self.minpos, self.targets, self.violent, self.wearoff,
					  self.manual)
		return self

	def manual(self, spell, caster):
		pass

def ASPELL(name, max_mana, min_mana, mana_change, minpos, targets, violent, wearoff,
	       register = True):

	def makeSpell(manual):
		spell = Spell()
		spell.name = name
		spell.max_mana = max_mana
		spell.min_mana = min_mana
		spell.mana_change = mana_change
		spell.minpos = minpos
		spell.targets = targets
		spell.violent = violent
		spell.wearoff = wearoff

		if manual is not None:
			spell.manual = manual

		return spell() if register else spell

	return makeSpell

#@apply
#@apply
class flare(Spell):
	name = 'flare'
	mana_change = 20
	violent = True

	def manual(self, spell, caster):
		# cause elemental damage.
		pass
