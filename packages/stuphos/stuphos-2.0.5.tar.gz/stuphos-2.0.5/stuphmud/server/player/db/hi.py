'High-level struct implementation of player file format.'
from hstruct import *

MAX_NAME_LENGTH  = 20
MAX_EMAIL_LENGTH = 80
MAX_PWD_LENGTH   = 10
MAX_AFFECT       = 32
MAX_COLOR_SET    = 32
HOST_LENGTH      = 40
MAX_SKILLS       = 200
MAX_TONGUE       = 3

class CharSpecialData(Struct):
	alignment     = Type.Int
	idnum         = Type.Long
	actflags      = Type.Long
	affected      = Type.Long
	saving_throws = Type.Short[5]

class PlayerSpecialData(Struct):
	skills          = Type.Byte[MAX_SKILLS+1]
	padding         = Type.Byte
	talks           = Type.Byte[MAX_TONGUE]
	wimp_level      = Type.Int
	freeze_level    = Type.Byte
	invis_level     = Type.Short
	load_room       = Type.Int
	preferences     = Type.Long
	preferences2    = Type.Long
	displayflags    = Type.Long
	bad_password    = Type.UnsignedByte
	conditions      = Type.Byte[3]

	spells_to_learn = Type.Int
	marital_status  = Type.Int
	num_marriages   = Type.Int
	married_to      = Type.Long
	spell_attack    = Type.Int[2]
	remort_points   = Type.Int

class AbilityData(Struct):
	strength           = Type.Byte
	strength_addition  = Type.Byte
	intelligence       = Type.Byte
	wisdom             = Type.Byte
	dexterity          = Type.Byte
	constitution       = Type.Byte
	charisma           = Type.Byte

class PointData(Struct):
	mana       = Type.Short
	max_mana   = Type.Short
	hit        = Type.Short
	max_hit    = Type.Short
	move       = Type.Short
	max_move   = Type.Short

	deaths     = Type.Short
	mkills     = Type.Short
	pkills     = Type.Short
	dts        = Type.Short
	qpoints    = Type.Short
	armor      = Type.Short

	gold       = Type.Int
	bank       = Type.Int
	experience = Type.Int

	hitroll    = Type.Short
	damroll    = Type.Short

class AffectedType(Struct):
	type      = Type.Short
	duration  = Type.Short
	modifier  = Type.Byte
	location  = Type.Byte
	bitvector = Type.Long
	next      = Type.Pointer

class PlayerData(Struct):
	name            = Type.String[MAX_NAME_LENGTH +1]
	email           = Type.String[MAX_EMAIL_LENGTH+1]
	remort          = Type.Int
	race            = Type.Int
	clan            = Type.Int
	clanrank        = Type.Int
	page_length     = Type.Int
	save_room       = Type.Int
	sex             = Type.Byte
	chclass         = Type.Byte
	level           = Type.Byte
	hometown        = Type.Short
	birth           = Type.Int
	played          = Type.Int
	weight          = Type.UnsignedByte
	height          = Type.UnsignedByte

	pwd             = Type.String[MAX_PWD_LENGTH+1]

	char_specials   = Type.Struct(CharSpecialData)
	player_specials = Type.Struct(PlayerSpecialData)
	abilities       = Type.Struct(AbilityData)
	points          = Type.Struct(PointData)
	affected        = Type.Struct(AffectedType)[MAX_AFFECT]
	color           = Type.Int[MAX_COLOR_SET]

	last_login      = Type.Int
	last_logon      = Type.Int
	host            = Type.String[HOST_LENGTH+1]
