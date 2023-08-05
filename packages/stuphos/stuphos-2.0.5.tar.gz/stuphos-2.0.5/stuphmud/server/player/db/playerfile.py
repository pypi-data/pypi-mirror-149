# Copyleft Clint Bains 2006
# Note the hack in PLRFILE.read_player_entries and read_player
'''
DEFAULT_PLRFL = 'lib/etc/players'
DEFAULT_STORE = 'lib/etc/players.db' # ':memory:'

PLRFILE().read_player_entries()
'''

DEFAULT_PLRFL = 'etc/players'
DEFAULT_STORE = 'etc/players.db' # ':memory:'

__all__=['PLRFILE', 'PLRDBIntoSQL', 'DEFAULT_PLRFL', 'DEFAULT_STORE', 'unpack_player', 'tuple2dict', 'cstring', 'trim_cstrings']

# import new

from struct import *
from os.path import exists
from pprint import pprint as pp

try: from stuphos.etc.tools.structfmt import stfmti
except ImportError:
	def stfmti(*args, **kwd):
		raise NotImplementedError

import stuphmud.server.player

# ToDo: incorporate the original pfile-position
# Composite unique key formed by idnum/name and save number/save-time

saving_throw_names=('savingthrow1', 'savingthrow2', 'savingthrow3', 'savingthrow4', 'savingthrow5')

char_specials_names=('alignment', 'idnum', 'act', 'affectedby') +saving_throw_names
player_specials_names=('skills', 'talks', 'wimp', 'freeze', 'invis', 'loadroom',
				'pref', 'pref2', 'disp', 'badpws', 'drunk', 'hunger', 'thirst',
				'spells2learn', 'maritalstatus', 'num_marriages', 'spouse',
				'spellattack1', 'spellattack2', 'remortpoints')

abilities_names=('str', 'stradd', 'intel', 'wis', 'dex', 'con', 'cha')
points_names=('mana', 'maxmana', 'hit','maxhit', 'move', 'maxmove', 'deaths', 'mkills', 'pkills',
		'dts', 'qpoints', 'armor', 'gold', 'bank', 'exp', 'hitroll', 'damroll')

pfilel_names=('name', 'email', 'remort', 'race', 'clan', 'clanrank', 'pagelength', 'saveroom',
		'sex', 'chclass', 'level', 'hometown', 'birth', 'played', 'weight', 'height', 'pwd')\
		+char_specials_names +player_specials_names +abilities_names +points_names\
		+('affected', 'color', 'lastlogin', 'lastlogon', 'host')

#pfilel_types=('varchar(%d)'%MAX_NAME_LENGTH+1, 'varchar(%d)'%MAX_EMAIL_LENGTH+1)+('integer',)*6

pfilel_ncount=len(pfilel_names)
pfilel_types=['']*pfilel_ncount

MAX_NAME_LENGTH=20
MAX_EMAIL_LENGTH=80
MAX_PWD_LENGTH=10
MAX_AFFECT=32
MAX_COLOR_SET=32
HOST_LENGTH=40
MAX_SKILLS=200
MAX_TONGUE=3

char_specials_fmt    = 'i3l5h'
player_specials_fmt  = '%ds' % (calcsize('b') * MAX_SKILLS+1)
player_specials_fmt += 'x'
player_specials_fmt += '%ds' % (calcsize('i') * MAX_TONGUE)
player_specials_fmt += 'ibhI3lB3b3il3i'
abilities_fmt        = '7b'
points_fmt           = '12h3i2b'

affected_fmt         = '2h2bl'
affected_fmt        += '%dx' % calcsize('P') # padd out next pointer

# ending_padding     = '1191x'
ending_padding       = ''

u_header_fmt         = '%ds%ds6i3bh2i2B%ds' % (MAX_NAME_LENGTH+1, MAX_EMAIL_LENGTH+1, MAX_PWD_LENGTH+1)
u_affected_fmt       = '%ds' % (calcsize(affected_fmt) * MAX_AFFECT)	# XXX Do not use string-type
u_color_fmt          = '%ds' % (calcsize('i') * MAX_COLOR_SET)		# XXX Do not use string-type
u_logtime_fmt        = '2i'
u_host_fmt           = '%ds' % (HOST_LENGTH+1)

pfilel_fmt           = u_header_fmt
pfilel_fmt          += char_specials_fmt
pfilel_fmt          += player_specials_fmt
pfilel_fmt          += abilities_fmt
pfilel_fmt          += points_fmt
pfilel_fmt          += u_affected_fmt
pfilel_fmt          += u_color_fmt
pfilel_fmt          += u_logtime_fmt
pfilel_fmt          += u_host_fmt

pfilel_fmt          += ending_padding

def printFormats(formats = ('u_header_fmt',
				'char_specials_fmt',
				'player_specials_fmt',
				'abilities_fmt',
				'points_fmt',
				'u_affected_fmt',
				'u_color_fmt',
				'u_logtime_fmt',
				'u_host_fmt')):

	tmpl = '%-20s %5d %5d %s'

	print('Name                  Size #Atms Format')
	print(tmpl % ('pfilel_fmt', calcsize(pfilel_fmt), len(list(stfmti(pfilel_fmt))), pfilel_fmt))
	
	total_size = 0
	z = 0

	for n in formats:
		f = globals()[n]
		s = calcsize(f)
		t = len(list(stfmti(f)))

		print(tmpl % (n, s, t, (' ' * z) + f))

		total_size += s
		z += len(f)

	# Total size should be the same as calcsize(pfilel_fmt)
	print('Total Size:', total_size)

def printNames(formats = ('pfilel_names',
				'saving_throw_names',
				'char_specials_names',
				'player_specials_names',
				'abilities_names',
				'points_names')):

	print('Name                  Size        Format')
	for n in formats:
		f = globals()[n]
		print('%-20s %5d       %r' % (n, len(f), f))

pfilel_size=calcsize(pfilel_fmt)
pfilel_sqldecl=', '.join([' '.join(p) for p in zip(pfilel_names, pfilel_types)])

NEW_PLAYERS_TABLE='CREATE TABLE players(%s)' % ', '.join(pfilel_names)
NEW_PLAYER='INSERT OR REPLACE INTO players('+pfilel_sqldecl+') VALUES('+', '.join(['?']*pfilel_ncount)+')'

def unpack_player(buf, cleanse_nonstring_buffers = True):
	t = unpack(pfilel_fmt, buf + '\x00') ## XXX Hack

	if cleanse_nonstring_buffers:
		# Kill the affected and colorset buffers because they are not UTF8 friendly.
		# This is dissimilar from trim_cstrings

		t = list(t)  # make mutable
		t[71] = ''   # position of affected buffer
		t[72] = ''   # position of colorset buffer
		# Also, talks, and skills are non-UTF8-friendly buffers
		t = tuple(t) # reformat

	return t

def load_player_stream(stream, unpack = False):
	# iapply
	read = stream.read

	while True:
		buf = read(pfilel_size - 1) ## XXX Hack
		if buf == '':
			return

		if unpack:
			yield unpack_player(buf)
		else:
			yield buf

def read_player_entries(file = None, filename = ''):
	if file:
		if type(file) is str:
			filename = file
		else:
			return load_player_stream(file)

	if filename:
		return load_player_stream(open(filename))

	raise AssertionError

def goto_pfilepos(fl, pfilepos):
	return fl.seek(pfilepos*pfilel_size)

def read_player(playerfl, pfilepos):
	goto_pfilepos(playerfl, pfilepos)
	return unpack_pack(playerfl.read(pfilel_size - 1) + '\x00')  ## XXX Hack

def write_player(playerfl, pfilepos, plrrecord):
	goto_pfilepos(playerfl, pfilepos)
	return playerfile.write(pack(pfilel_fmt, plrrecord))

## Aliases:
class PlayerFileReader(object):
	# XXX Backwards-compatability.
	def __init__(self, players = None):
		self.players = players or DEFAULT_PLRFL

	def __repr__(self):
		return 'players: ' + repr(self.players)

	def read_player_entries(self, filename = None):
		'Wrapper for contained playerfile.read_player_entries.'
		return read_player_entries(filename or self.players)

PLRFILEReader=PLRFILE=PlayerFileReader


class PLRDBIntoSQL(PlayerFileReader):
	"Plugs a PLRFILE into an SQLite database"

	def __init__(self, store=None, loadsource=None):
		# PlayerFileReader.__init__(self)
		self.open_store(type(store) is str and (store,) or store)
		if loadsource:
			self.save_players(self.read_player_entries(loadsource))

	def write_player(self, player, pfilepos = 0):
		'Install player into cursory connection'
		# pp(player)
		# raw_input()
		# print 'len(player[1])', len(player[1])

		self.x(NEW_PLAYER, player)
		# self.x('UPDATE players SET pfilepos=%d WHERE name=%r' % (pfilepos, player[1][0]))

	def save_players(self, players = None, ):
		"Stream all players given by the `players' iterable through write_player -- Also creates self.stmts and self.players."
		plrs=self.players=[]
		append=plrs.append

		stmts=self.stmts=[]
		append2=stmts.append

		pfilepos=0
		for p in players:
			append2(p[0])
			append(p[1])

			self.write_player(p, pfilepos)
			pfilepos+=1

		print('Saved', len(plrs), 'Players ...')

	def open_store(self, store):
		e=not exists(store[0])

		c=self.connection = mud.player.sqlite_connect(*store)
		u=self.u=c.cursor()
		x=self.x=u.execute

		if e:
			x(NEW_PLAYERS_TABLE)
			x('ALTER TABLE players ADD (pfilepos)')

	def commit(self):
		self.connection.commit()

def tuple2dict(t, names = pfilel_names):
	
	d = {}

	for (n, v) in zip(names, t):
		d[n] = v

	return d

def cstring(s):
	i = s.find('\x00')
	if i < 0:
		return s
	return s[:i]

def trim_cstrings(d):
	def reset(n):
		if n in d:
			d[n] = cstring(d[n])

	if type(d) is dict:
		reset('name')
		reset('email')
		reset('host')

	return d

if __name__=='__main__':
	from psyco import full;full()

	plrdb=PLRDBIntoSQL(DEFAULT_STORE)
	plrdb.save_players(plrdb.read_player_entries(DEFAULT_PLRFL))
	plrdb.commit()

	u=plrdb.u
	x=plrdb.x
	a=lambda:x('select * from players')
