'Schema for a StuphMUD player save - point.'

from sqlobject import *

class PlayerStore(SQLObject):
	# This is introduced by playerSavePoint - Rename to savepoint.
	save_point_indication = StringCol()

	name            = StringCol() # limit this length
	idnum           = IntCol()
	level           = IntCol(default = 0)
	pwd             = StringCol() # limit this length
	host            = StringCol(default = '') # limit this length
	email           = StringCol(default = '') # limit this length

	color           = BLOBCol(default = '')
	talks           = BLOBCol(default = '')
	skills          = BLOBCol(default = '')
	affected        = BLOBCol(default = '')

	birth           = IntCol(default = 0)
	sex             = IntCol(default = 0)
	exp             = IntCol(default = 0)
	played          = IntCol(default = 0)

	loadroom        = IntCol(default = -1)
	saveroom        = IntCol(default = -1)

	invis           = IntCol(default = 0)
	freeze          = IntCol(default = 0)
	badpws          = IntCol(default = 0)

	lastlogin       = IntCol(default = 0)
	lastlogon       = IntCol(default = 0)

	cha             = IntCol(default = 11)
	con             = IntCol(default = 11)
	dex             = IntCol(default = 11)
	str             = IntCol(default = 11)
	wis             = IntCol(default = 11)
	intel           = IntCol(default = 11)
	stradd          = IntCol(default = 0)

	act             = IntCol(default = 0)
	disp            = IntCol(default = 0)
	pref            = IntCol(default = 0)
	pref2           = IntCol(default = 0)
	affectedby      = IntCol(default = 0)

	dts             = IntCol(default = 0)
	deaths          = IntCol(default = 0)
	mkills          = IntCol(default = 0)
	pkills          = IntCol(default = 0)

	maxhit          = IntCol(default = 10)
	hit             = IntCol(default = 10)
	maxmana         = IntCol(default = 10)
	mana            = IntCol(default = 10)
	move            = IntCol(default = 10)
	maxmove         = IntCol(default = 10)

	bank            = IntCol(default = 0)
	gold            = IntCol(default = 0)

	clan            = IntCol(default = -1)
	clanrank        = IntCol(default = 0)

	race            = IntCol(default = 0)
	chclass         = IntCol(default = 0)

	spouse          = IntCol(default = -1)
	maritalstatus   = IntCol(default = 0)
	num_marriages   = IntCol(default = 0)

	qpoints         = IntCol(default = 0)
	remort          = IntCol(default = 0)
	hometown        = IntCol(default = -1)
	remortpoints    = IntCol(default = 0)

	alignment       = IntCol(default = 0)
	height          = IntCol(default = 120)
	weight          = IntCol(default = 120)

	pagelength      = IntCol(default = 22)

	armor           = IntCol(default = 10)
	damroll         = IntCol(default = 0)
	hitroll         = IntCol(default = 0)
	wimp            = IntCol(default = 0)

	drunk           = IntCol(default = 0)
	hunger          = IntCol(default = 0)
	thirst          = IntCol(default = 0)

	savingthrow1    = IntCol(default = 0)
	savingthrow2    = IntCol(default = 0)
	savingthrow3    = IntCol(default = 0)
	savingthrow4    = IntCol(default = 0)
	savingthrow5    = IntCol(default = 0)

	spellattack1    = IntCol(default = -1)
	spellattack2    = IntCol(default = -1)

	spells2learn    = IntCol(default = 0)
