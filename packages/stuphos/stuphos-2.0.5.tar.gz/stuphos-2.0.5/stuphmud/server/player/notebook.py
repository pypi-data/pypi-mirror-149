# Player-Oriented File Notebook.
# Todo: adapt this to item-oriented specproc!
#
from stuphmud.server.player import *
from stuphmud.server.player.db.managedfs import *
from stuphmud.server.player.db.managedfs import getPlayerFilename, validatePlayername
from stuphos.etc import columnize, xorString as xor
from stuphos import getConfig

from stuphos.db import dbCore
from stuphos.db.orm import PlayerNotebook

import pickle
import shelve
import string
import re

# Default Notebooks.
PLAYER_NOTEBOOK_FOLDER = 'library'
PLAYER_NOTEBOOK_NAME = 'notebook'

DEFAULT_PAGE_NAME = 'Front-Matter'
PAPER_VNUM = 3

PAGE_NAME_PATTERN = re.compile(r"^a page named: '([^']+)'$")
def parsePageName(name):
    m = PAGE_NAME_PATTERN.match(name)
    if m is not None:
        return m.group(1)

# Disk Usage.
KILOBYTE = 1024
MEGABYTE = KILOBYTE * 1024
GIGABYTE = MEGABYTE * 1024
TERABYTE = GIGABYTE * 1024
EXABYTE  = TERABYTE * 1024
PETABYTE = EXABYTE  * 1024

BYTE_LEVELS = [(PETABYTE, 'Pb'),
               (EXABYTE,  'Eb'),
               (TERABYTE, 'Tb'),
               (GIGABYTE, 'Gb'),
               (MEGABYTE, 'Mb'),
               (KILOBYTE, 'Kb')]

def getHumanBytes(bytes):
    for (level, code) in BYTE_LEVELS:
        if bytes >= level:
            return '%.2f%s' % (bytes / level, code)

    return '%d bytes' % bytes

def calculateAllFileSizes(path):
    from os import stat
    from glob import glob

    total = 0
    for fn in glob(path + '*'):
        try: total += stat(fn).st_size
        except: pass

    return total

# Some support for opening other's notebooks:
def getNotebookFilename(plrname, name = None, folder = None):
    filename = getPlayerFilename(validatePlayername(plrname),
                                 name or PLAYER_NOTEBOOK_NAME,
                                 folder = folder or PLAYER_NOTEBOOK_FOLDER)

    assert filename is not None # , UnconfiguredException
    return filename

class Notebook:
    class FileModel:
        @classmethod
        def Open(self, peer, name = None, folder = None):
            # Uses checked particular variant.
            self.fs_path = getCheckedPlayerFilename(peer, name or PLAYER_NOTEBOOK_NAME,
                                                    folder = folder or PLAYER_NOTEBOOK_FOLDER)

            return self(shelve.open(self.fs_path))

        @classmethod
        def OpenForPlayer(self, plrname, name = None, folder = None):
            return self(shelve.open(getNotebookFilename(plrname, name = name, folder = folder)))

        def __init__(self, shelf):
            self.shelf = shelf
            self.close = shelf.close

    class ORMModel:
        @classmethod
        def Open(self, peer, name = None, folder = None):
            return self(self.ORMShelf(peer.avatar.name, name or PLAYER_NOTEBOOK_NAME,
                                      folder = folder or PLAYER_NOTEBOOK_FOLDER))

        @classmethod
        def OpenForPlayer(self, plrname, name = None, folder = None):
            # ('python.db', managedfs.PROGRAMS_DIR)
            return self(self.ORMShelf(plrname, name or PLAYER_NOTEBOOK_NAME,
                                      folder = folder or PLAYER_NOTEBOOK_FOLDER))

        def __init__(self, shelf):
            self.shelf = shelf

        def close(self):
            return self.shelf.close()

        class ORMShelf:
            def __init__(self, player, recordBaseName, folder = None):
                self.player = player
                self.recordBaseName = recordBaseName
                self.folder = folder

            PAGE_PICKLED = (1 << 0)

            @property
            def dbNamespace(self):
                return getConfig('database', 'Notebook')

            def __getitem__(self, name):
                # Return string content.
                with dbCore.hubThread(self.dbNamespace):
                    try:
                        for page in PlayerNotebook.selectBy(player = self.player, folder = self.folder, name = name):
                            if page.flags & self.PAGE_PICKLED:
                                return pickle.loads(page.content)

                            return page.content

                    except sqlite.module.dberrors.OperationalError:
                        pass

                raise KeyError(name)

            def __setitem__(self, name, value):
                if not isinstance(value, str):
                    value = pickle.dumps(value)
                    flags = self.PAGE_PICKLED
                else:
                    flags = 0

                with dbCore.hubThread(self.dbNamespace):
                    # Upsert.
                    for page in PlayerNotebook.selectBy(player = self.player, folder = self.folder, name = name):
                        page.content = value
                        page.flags = flags
                        break
                    else:
                        page = PlayerNotebook(player = self.player, folder = self.folder,
                                              name = name, content = value, flags = flags)

                    page.sync()

            def __delitem__(self, name):
                with dbCore.hubThread(self.dbNamespace):
                    PlayerNotebook.deleteBy(player = self.player, folder = self.folder, name = name)

            def __contains__(self, name):
                try: self[name]
                except KeyError:
                    return False

                return True

            def iterkeys(self):
                with dbCore.hubThread(self.dbNamespace):
                    for page in PlayerNotebook.selectBy(player = self.player, folder = self.folder):
                        yield page.name

            def iteritems(self):
                with dbCore.hubThread(self.dbNamespace):
                    for page in PlayerNotebook.selectBy(player = self.player, folder = self.folder):
                        yield (page.name, page.content)

            def items(self):
                return list(self.iteritems())

            def keys(self):
                return list(self.iterkeys())

            def close(self):
                pass
            def sync(self):
                pass

    Model = ORMModel

    class PlayerInterface(Model):
        # Command routines: they close the notebook explicitly on change.
        def doShow(self, peer):
            keys = list(self.shelf.keys())
            if not keys:
                playerAlert('No pages have been entered into the notebook.')

            width = max(list(map(len, keys)))
            # width = min(20, width)

            nr_cols = (120 / width)
            nr_cols = max(6, nr_cols)
            nr_cols = min(2, nr_cols)

            string = columnize(keys, nr_cols, width + 2)
            string = string.split('\n')
            string = [_f for _f in string if _f]
            string = '    ' + '\n    '.join(string)
            string = string.replace('\n', '\r\n')
            string += '\r\n'

            try: bytes = self.getDiskSize()
            except: bytes = 0

            bytes = getHumanBytes(bytes)

            string = 'Notebook [%d pages; %s]\r\n%s' % (len(keys), bytes, string)
            peer.page_string(string)

        def doView(self, peer, name = DEFAULT_PAGE_NAME):
            try: peer.page_string(self.shelf[name] or 'No text.\r\n')
            except KeyError:
                playerAlert('&rNo such page name: &w%r&N' % name)

        def doDelete(self, peer, name = DEFAULT_PAGE_NAME):
            try: del self.shelf[name]
            except KeyError:
                playerAlert('&rNo such page name: &w%r&N' % name)
            else:
                self.close()

        def doEdit(self, peer, name = DEFAULT_PAGE_NAME):
            def enterNotebookPage(peer, text):
                self.shelf[name] = text
                self.close()
                print('&w%r&N entered into notebook.' % name, file=peer)

                # delete messenger reference?
                # return True

            try: original = self.shelf[name]
            except KeyError:
                original = ''

            peer.messenger = enterNotebookPage
            if hasattr(peer, 'richEditor'):
                peer.richEditor(original, header = name)
            else:
                peer.editString(original)

        def doCopy(self, peer, source, copy, overwrite = False):
            if copy in self.shelf:
                if overwrite not in ['overwrite']:
                    playerAlert('&rYou must specify "overwrite" afterwards to do this.&N')

                # Note: overwrite could be the name of a piece of paper in inventory, or
                # as a board message!!

            self.shelf[copy] = self.shelf[source]
            self.close()

            playerAlert('Copied page %s to %s.' % (source, copy))

        def doTearOut(self, peer, name):
            try: content = self.shelf[name]
            except KeyError:
                playerAlert('&rUnknown page: %r&N' % name)

            import world
            paper = world.item(PAPER_VNUM).load(peer.avatar)
            paper.detailed_description = content
            paper.keywords = name + ' paper page'
            paper.name = "a page named: '%s'" % name

            # peer.avatar.save()

            del self.shelf[name]
            self.close()

            playerAlert('You tore out page %r' % name)

        def doPasteIn(self, peer, keyword, force = False):
            page = peer.avatar.find(keyword, inventory = True)
            if page is None:
                playerAlert("You don't have a %r to paste in!" % keyword)

            itemName = page.name
            if page.type != 'Note':
                playerAlert('%s is not something you can paste into your notebook.' % \
                            itemName.capitalize())

            pageName = parsePageName(itemName)
            if pageName is None:
                if force is False or not peer.avatar.supreme:
                    playerAlert("You can't seem to figure out how to paste %r into your notebook." % \
                                itemName)

                pageName = force

            if pageName in self.shelf:
                playerAlert('There is already a page named %r in your notebook.' % pageName)

            self.shelf[pageName] = page.detailed_description
            self.close()

            page.extract()

            playerAlert('You paste %s into your notebook.' % itemName)

        def doEncrypt(self, peer, name, key = None):
            try: content = self.shelf[name]
            except KeyError:
                playerAlert('No page named: %r' % name)

            if key is None:
                key = '' # Todo: get personal key??  Or, key by name.

            # Encrypt/Bind.
            ciphertext = xor(content, key)
            bound = ciphertext.encode('zlib').encode('base64')

            from email.message import Message
            msg = Message()
            msg.set_type('text/stuph-binding')

            msg['Content-Transfer-Encoding'] = 'zlib; base64'
            msg.set_payload(bound)

            content = msg.as_string()

            # Put back into notebook.
            self.shelf[name] = content
            self.close()

            playerAlert('Bound %r.' % name)

        def doDecrypt(self, peer, name, key = None):
            try: content = self.shelf[name]
            except KeyError:
                playerAlert('No page named: %r' % name)

            if key is None:
                key = '' # Todo: get personal key??  Or, key by name.

            # Decrypt/Unbind.
            from email import message_from_string
            msg = message_from_string(content)

            if msg.get_content_type() != 'text/stuph-binding':
                playerAlert('The page is not bound.')

            encoding = msg.get('Content-Transfer-Encoding')
            if encoding != 'encrypted; zlib; base64':
                playerAlert('The page is not bound properly: %s.' % encoding)

            content = msg.get_payload()
            ciphertext = content.decode('base64').decode('zlib')

            content = xor(ciphertext, key)

            # Put back into notebook.
            self.shelf[name] = content
            self.close()

            playerAlert('Unbound %r.' % name)

        def doEmail(self, peer):
            # actually, just mud-mail?
            playerAlert('Not yet supported!')

        # About this store (version, format, capabilities, signatures, etc.)
        def getMeta(self):
            try: return self.shelf['__meta__']
            except KeyError:
                return {}

        def getDiskSize(self):
            # We can't know, so we try to add up all files in the directory.
            return calculateAllFileSizes(self.fs_path)

    class ProgrammaticInterface(Model):
        def pageNames(self):
            return iter(self.shelf.keys())

        def getPageContent(self, name):
            return self.shelf[name]
        def setPageContent(self, name, value):
            self.shelf[name] = value

        __iter__ = pageNames
        __getitem__ = getPageContent
        __setitem__ = setPageContent

        def __enter__(self):
            return self
        def __exit__(self, etype = None, value = None, tb = None):
            self.close()

        @classmethod
        def IntelligentOpen(self, player, name = None, folder = None):
            from world import mobile as MobileType, peer as PeerType
            if isinstance(player, MobileType):
                assert player.isPlayer
                player = player.name

            if isinstance(player, str):
                return self.OpenForPlayer(player, name = None, folder = None)

            assert isinstance(player, PeerType)
            return self.Open(player, name = None, folder = None)

    ##    @runtime.api(runtime.Player.Notebook.API)
    ##    class API:
    ##        Open = ProgrammaticInterface.IntelligentOpen

# Install Runtime API.
runtime.Player.Notebook.API.Open(lambda:Notebook        \
                                 .ProgrammaticInterface \
                                 .IntelligentOpen)

@ACMD('note*book')
def doPlayerNotebook(peer, cmd, argstr):
    args = () if not argstr else argstr.split()
    larg = '' if not args else args[0].lower()

    try:
        OpenPlayerNotebook = Notebook.PlayerInterface.Open

        if larg in ['', 'show', 'list']:
            OpenPlayerNotebook(peer).doShow(peer, *args[1:])
        elif larg in ['view']:
            OpenPlayerNotebook(peer).doView(peer, *args[1:])
        elif larg in ['delete']:
            OpenPlayerNotebook(peer).doDelete(peer, *args[1:])
        elif larg in ['edit']:
            OpenPlayerNotebook(peer).doEdit(peer, *args[1:])
        elif larg in ['encrypt', 'bind']:
            OpenPlayerNotebook(peer).doEncrypt(peer, *args[1:])
        elif larg in ['decrypt', 'unbind']:
            OpenPlayerNotebook(peer).doDecrypt(peer, *args[1:])
        elif larg in ['email']:
            OpenPlayerNotebook(peer).doEmail(peer, *args[1:])
        elif larg in ['copy']:
            OpenPlayerNotebook(peer).doCopy(peer, *args[1:])
        elif larg in ['tearout', 'tear-out', 'tear']:
            OpenPlayerNotebook(peer).doTearOut(peer, *args[1:])
        elif larg in ['pastein', 'paste-in', 'paste']:
            OpenPlayerNotebook(peer).doPasteIn(peer, *args[1:])
        else:
            print('Unknown subcommand: %r' % args[0], file=peer)

    except PlayerAlert as e:
        e.deliver(peer)

    return True

# Attempt at specproc.
class SpecialNotebook:
    def __init__(self, filename):
        self.filename = filename

    def Open(self):
        OpenSpecialNotebook = Notebook.PlayerInterface
        return OpenSpecialNotebook(self.filename)

    ACTION_MAP = dict(look = 'doShow', examine = 'doShow',
                      read = 'doView', write = 'doEdit',
                      junk = 'doDelete', mail = 'doEmail')
                      # encrypt/bind
                      # decrypt/unbind
                      # copy
                      # tearout
                      # paste

    def __call__(self, this, ch, cmd, argstr):
        peer = ch.peer
        if peer is not None:
            try: actionName = self.ACTION_MAP[cmd.name]
            except KeyError: pass
            else:
                nb = self.OpenNotebook()
                action = getattr(nb, actionName)

                # Something we recognize, now make sure we're targeting this object.
                args = () if not argstr else argstr.split()
                if len(args) and ch.find(args[0]) is this:
                    try: action(peer, *args)
                    except PlayerAlert as e:
                        e.deliver(peer)

                    return True

# Directory-based notebook access.
##    from stuphlib.directory import Directory
##    PLRFILES = Directory.FromTree('PLRFILES',
##            '''
##            (partition-map):
##                format = 'plrfiles/%(name)s/%(folder)s/%(name)s.db
##            ''')

