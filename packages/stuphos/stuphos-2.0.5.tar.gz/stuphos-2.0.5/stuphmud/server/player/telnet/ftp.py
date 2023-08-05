# FTP Module.
from stuphmud.server.player import playerAlert, getCapitalizedName
from stuphmud.server.player.db.managedfs import getCheckedPlayerFilename, PERSONAL_PLRFILE_DIR, KEYFILE_DIR

from os import rename, unlink, stat, listdir
from os.path import dirname

from errno import EEXIST

class FTPDispatchModule:
    @classmethod
    def getDispatchAction(self, operation):
        actionName = '_do%s' % getCapitalizedName(operation)
        if hasattr(self, actionName):
            return self(actionName)

    def __init__(self, operation):
        self.operation = operation
        self.invoke = getattr(self, operation, None)

    def __call__(self, peer, *params):
        # Do operation.
        if params:
            filename = params[0]
            params = params[1:]
        else:
            filename = ''

        plrname = peer.avatar and peer.avatar.name.lower() or ''
        dirOp = bool(getattr(self.invoke, 'dirOperation', False))
        plrfile = getCheckedPlayerFilename(peer, filename, PERSONAL_PLRFILE_DIR, dirOp)
        self.invoke(peer, plrname, plrfile, *params)

        # Todo: playerAlert this?
        print('Operation [%s] %r complete!' % (self.operation, plrfile), file=peer)

    # Operations.
    def _doCreate(self, peer, plrname, plrfile, content):
        # Todo: expect checksum
        EnsureDirectories(plrfile)
        fl = open(plrfile, 'w')
        fl.write(content)
        fl.flush()
        fl.close()

    def _doAppend(self, peer, plrname, plrfile, content):
        fl = open(plrfile, 'a')
        fl.write(content)
        fl.flush()
        fl.close()

    def _doDelete(self, peer, plrname, plrfile):
        unlink(plrfile)

    def _doRename(self, peer, plrname, plrfile, newname):
        newname = getSecureFilename(newname)
        if not newname:
            playerAlert('Unable to produce secure filename.')

        newname = getPlayerFilename(plrname, newname)
        if not newname:
            playerAlert('Could not obtain player filename.')

        rename(plrfile, newname)

    def _doTouch(self, peer, plrname, plrfile):
        playerAlert('Touch operation not yet supported.')

    def _doTruncate(self, peer, plrname, plrfile):
        fl = open(plrfile, 'w')
        fl.truncate(0)
        fl.flush()
        fl.close()

    def _doList(self, peer, plrname, plrfile = None):
        from stuphos.etc.tools import columnize
        try: files = listdir(plrfile)
        except OSError as e: playerAlert(str(e))
        else: playerAlert(columnize(files, 2, 40))
    _doList.dirOperation = True

    def _doStat(self, peer, plrname, plrfile):
        st = stat(plrfile)
        print('%s: %d' % (plrfile, st.st_size), file=peer)

    def _doView(self, peer, plrname, plrfile):
        peer.page_string(open(plrfile).read())

    def _doLoad(self, peer, plrname, plrfile):
        from pickle import dump
        from io import StringIO
        from pickletools import dis

        from stuphos.language.document import interface as document

        env = document.Environment()
        loader = document.Loader(env)
        loader.loadDocument(document.FileSource(plrfile))

        buf = StringIO()
        buf2 = StringIO()

        dump(env.olc, buf)
        buf.seek(0)

        dis(buf, buf2)
        peer.page_string(buf2.getvalue())

    def _doRender(self, peer, plrname, plrfile):
        # as django template...
        pass

    def _doDecrypt(self, peer, plrname, plrfile):
        # Todo: multithread this! (Decryption takes time)
        keyfile = getCheckedPlayerFilename(peer, 'my.key', KEYFILE_DIR)
        key = LoadKeyfile(keyfile) # Catch IOError and report.
        DecryptFile(key, plrfile, armored = True)
        playerAlert('Decrypted [%s]' % plrfile)

def EnsureDirectories(filename):
    # This creates the directories leading up to the base.
    from os.path import split as splitpath
    (path, fn) = splitpath(filename)
    if not fn:
        raise ValueError('Directory path has no base filename! (%s)' % filename)

    from os import makedirs
    try: makedirs(path)
    except OSError as e:
        if e.args[0] != EEXIST:
            raise

def LoadKeyfile(filename):
    # Format: plain ascii keyphrase...
    return open(filename).read().strip()

def getCipher(key):
    from crypto.cipher.trolldoll import Trolldoll
    alg = Trolldoll(ivSize = 160)
    alg.setPassphrase(key) # .setKey(key)
    return alg

def encrypt(key, content):
    return getCipher(key).encrypt(content)
def decrypt(key, content):
    return getCipher(key).decrypt(content)

def encryptArmored(key, content):
    return encrypt(key, content).encode('base64').replace('\n', '')
def decryptArmored(key, content):
    return decrypt(key, content.decode('base64'))

def DecryptFile(key, filename, armored = False):
    # Decrypt file in place.
    content = open(filename).read()
    decrypted = decryptArmored(key, content) if armored else decrypt(key, content)

    # Todo: decrypt to migrating file in blocks..
    tmp = filename + '.migrating'
    fl = open(tmp, 'wt')
    fl.write(decrypted)
    fl.flush()
    fl.close()
    rename(tmp, filename)
