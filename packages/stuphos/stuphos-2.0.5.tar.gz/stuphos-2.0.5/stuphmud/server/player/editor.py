# Line-based In-Game String Content Editor
from types import GeneratorType as generator, MethodType
import re

# First:
def joinString(function):
    def doJoin(*args, **kwd):
        # (But not NL at end-of-block)
        return '\n'.join(function(*args, **kwd))

    return doJoin

def quote(s):
    return ' %  ' + '\n %  '.join(s.split('\n')) + '\n'

CLEAR_SCREEN = '\x1b[H\x1b[J'

def ParseRegExpr(line):
    # Todo: rewrite
    pattern = []
    escape = False
    for x in range(len(line)):
        c = line[x]
        if c == '\\':
            escape = True
            continue

        elif c == '/':
            if not escape:
                break

        escape = False
        pattern.append(c)

    pattern = ''.join(pattern)
    line = line[x+1:]

    i = line.rfind('/')
    if i >= 0:
        action = line[i+1:]
        line = line[:i]
    else:
        action = None

    yield (action, pattern, line)

class LineEditor:
    # Expansive 'state' stack and special command-handling for frameworking,
    # also, exclusive 'paging/viewing' mode.
    class State:
        MAIN = 0
        HELP = 1
        PASTE = 2
        VIEWING = 3

        INITIAL = MAIN

    HELP_SCREEN = CLEAR_SCREEN + "Commands:\n\n     @     Quit Editor               h ?   Help Screen\n" + \
                                              "     n     Next Line                 p     Previous Line\n" + \
                                              "     f     Forward Half Page         b     Backward Half Page \n" + \
                                              "     ff    Forward Full Page         bb    Backward Full Page\n" + \
                                              "     s     Start of Content          e     End of Content\n" + \
                                              "\n" + \
                                              "     --    Delete Current Line\n" + \
                                              "     ...   Begin Paste Mode\n" + \
                                              "\n" + \
                                              "     #<line content>     Change Current Line\n" + \
                                              "     +<line content>     Insert After Current Line\n" + \
                                              "     <<line content>     Insert Before Current Line\n" + \
                                              "     > j<line number>    Jump to Line Number\n" + \
                                              "\n" + \
                                              "     /<pattern>/<substitution>/p|g\n" + \
                                              "\n" + \
                                              "     ;<special command>  See Extended Documentation\n" + \
                                              "\n\n(Hit 'x' to exit help)\n"

    def __init__(self, peer, xxx_todo_changeme1, content = '', finishproc = None,
                 position = None, message = '', header = None, state = None):

        (rows, cols) = xxx_todo_changeme1
        assert isinstance(rows, int) and rows > 2
        assert isinstance(cols, int) and cols > 10

        self.content = self.loadContent(content)
        self.rows = rows
        self.cols = cols

        self.finishproc = finishproc
        self.position = 0 if position is None else self.validatePosition(position)

        self.header = header
        self.message = message
        self.state = []

        self.pushState(state if isinstance(state, int) else self.State.INITIAL)

        # Start prompting.
        PromptFor(peer, self.inputPhase, message = self.getScreen(),
                  write_mode = True, compact_mode = True)

    def loadContent(self, content):
        if isinstance(content, str):
            return content.split('\n')

        assert isinstance(content, (list, tuple, generator))
        return list(content)

    def renderContent(self):
        return '\n'.join(self.content) # + '\n'

    def validatePosition(self, pos):
        pos = int(pos)
        n = len(self.content)
        assert pos <= n and pos > 0, AssertionError('Valid positions are 1-%d' % n)
        return pos

    def setMessage(self, message):
        self.message = str(message)
    def setPrompt(self, prompt):
        # Note it's the prompt's message, not this editor's message.
        self.prompt.message = prompt

    def inputPhase(self, prompt, peer, line):
        self.prompt = prompt
        self.handleCommand(peer, line)

        if self.state:
            self.setPrompt(self.getScreen())
            return True # Regenerate

        if callable(self.finishproc):
            self.finishproc(self, peer)

        return False

    def inState(self, *states):
        return self.state[0] in states
    def pushState(self, state):
        self.state.insert(0, state)
    def popState(self):
        del self.state[0]

    @joinString
    def getScreen(self):
        if self.inState(self.State.PASTE):
            pass # Mainly an input phase.  But up here for optimization.

        elif self.inState(self.State.MAIN, self.State.VIEWING):
            r = self.rows - 1 # in between last line and message/prompt

            r -= 1 # our header
            yield CLEAR_SCREEN # ''

            if self.header:
                r -= 2
                yield self.header
                yield ''

            if self.message:
                r -= 1

            h = r // 2
            s = self.position - h
            e = self.position + h

            if s < 0:
                e -= s

            c = self.content
            n = len(c)
            if e >= n:
                s -= (e - n)
                e = n

            if s < 0:
                s = 0

            window = self.content[s:e]
            w = len(str(e))
            fmt = '%%s %%%dd   %%s' % w

            o = self.cols
            oMinus3 = o - 3
            for x in range(s, e):
                i = fmt % ('>' if x is self.position else ' ', x + 1, c[x])
                if len(i) > o:
                    i = i[:oMinus3] + '...'

                yield i

            if e < n:
                # ! This doesn't make much sense...
                yield (' [%%%dd]' % len(str(e))) % n

            yield ''
            if self.message:
                yield self.message

            yield '> '

        elif self.inState(self.State.HELP):
            yield self.HELP_SCREEN

    def handleCommand(self, peer, line):
        # Um, undo buffer??
        if self.inState(self.State.PASTE):
            if line == '@':
                self.pasteMode(False)
            else:
                self.pasteLine(line)

        elif self.inState(self.State.MAIN, self.State.VIEWING):
            line = line.strip()
            if not self.handlePaging(peer, line) and self.inState(self.State.MAIN):
                if line == '--':
                    self.delete(self.position)
                elif line == '...':
                    self.pasteMode(True)

                elif line:
                    c = line[0]
                    line = line[1:]

                    if c == '#':
                        # Edit/replace the line.
                        self.edit(self.position, line)

                    elif c == '+':
                        self.insert(self.position + 1, line)
                    elif c == '<':
                        self.insert(self.position, line)

                    elif c == '/':
                        # Search & Replace
                        (action, pattern, replace) = ParseRegExpr(line)
                        if action == 'p': # Current line.
                            pattern = re.compile(pattern)

                            line = self.content[self.position]
                            change = pattern.sub(line, replace)

                            self.edit(self.position, change)

                    elif c == ';': # '!'? -- this blocks all other interpreter action.
                        return self.specialCommand(peer, line)
                    else:
                        self.setMessage('NO: %s%s' % (c, line))

        elif self.inState(self.State.HELP):
            if line == 'x':
                self.popState()

        else:
            import ph
            ph.log('Unknown editor state (%s): %s' % (peer, self.state[0]))
            self.popState()

    def handlePaging(self, peer, line):
        if line == '@':
            self.popState()

        # Don't reset.
        # self.setMessage('')

        elif line == 'n':
            self.go(1)
        elif line == 'p':
            self.go(-1)
        elif line == 'f':
            self.go(self.rows // 2)
        elif line == 'b':
            self.go(-self.rows // 2)
        elif line == 'ff':
            self.go(self.rows)
        elif line == 'bb':
            self.go(-self.rows)
        elif line == 's':
            self.position = 0
        elif line == 'e':
            self.position = len(self.content) - 1
        elif line in ['h', 'help', '?']:
            self.pushState(self.State.HELP)
        elif not line and self.inState(self.State.VIEWING):
            # Just page -- like ff.
            self.go(self.rows)

        elif line[:1] in 'j>':
            try: self.jump(int(line[1:].strip()))
            except ValueError as e:
                self.setMessage(str(e))

        else:
            return False

        return True

    # Editing Methods.
    def go(self, nr = 0):
        self.position = min(max(self.position + nr, 0), len(self.content) - 1)
    def delete(self, pos):
        del self.content[self.position]

        n = len(self.content)
        if self.position >= n and n:
            self.position = n - 1

    def edit(self, pos, line):
        if self.content:
            self.content[self.position] = line
        else:
            # We maintain position 0 (line 1), even if it doesn't
            # exist.  So the special case is here, to create it.
            self.content.append(line)

    def insert(self, pos, line):
        if pos > len(self.content):
            self.content.append(line)
        elif pos >= 0:
            self.content.insert(pos, line)

        self.position += 1

    def pasteMode(self, state):
        if state:
            self.insertedNr = 0
            self.pushState(self.State.PASTE)
        else:
            self.setMessage('[Inserted %d lines]' % self.insertedNr)
            self.popState()

    def pasteLine(self, line):
        self.insert(self.position + 1, line)
        self.insertedNr += 1

    def jump(self, pos):
        try: self.position = self.validatePosition(pos) - 1
        except AssertionError as e:
            self.setMessage(e)

    def specialCommand(self, peer, command):
        self.setMessage('???: ;%s' % command)
        return True

class TreeEditor:
    pass # not yet implemented

# Invocation.
def getPeerWindowSize(peer):
    try: cols = peer.avatar.properties.screen.width
    except AttributeError:
        cols = 70

    rows = peer.avatar.page_length
    if rows <= 0:
        rows = 20
    elif rows < 5:
        rows = 5

    return (peer.avatar.page_length, cols)

def HeaderToFit(header, cols):
    n = cols - 6
    return ('&w[&m*&N %%%d.%ds &m*&w]&N' % (n, n)) % ('Editing: ' + header)

def TerminateMessageEditing(editor, peer):
    if peer.messenger:
        peer.messenger(peer, editor.renderContent())

def RichEditString(peer, content, header = None):
    (rows, cols) = getPeerWindowSize(peer)
    LineEditor(peer, (rows, cols), content,
               finishproc = TerminateMessageEditing,
               header = HeaderToFit(header, cols) \
                        if header else '')

def RichPageString(peer, content, header = None):
    (rows, cols) = getPeerWindowSize(peer)
    LineEditor(peer, (rows, cols),
               state = LineEditor.State.VIEWING,
               header = HeaderToFit(header, cols) \
                        if header else '')

def DecisiveEditString(peer, content, *args, **kwd):
    if getattr(peer.avatar, 'useRichEditor', False):
        return RichEditString(peer, content, *args, **kwd)

    return peer._basicEditString(content)

def DecisivePageString(peer, content, header = None):
    if getattr(peer.avatar, 'useRichPager', False):
        # Force needing header for now?  Otherwise, we end up paging
        # when we don't want to -- eventually, skip entering serious
        # paging if there's only one page (unless explicit).
        if header:
            return RichPageString(peer, content, header = header)

    return peer._basicPageString(content)

# thisModule = lambda:__import__(__name__, fromlist = [''])
def bindToThis(object, method):
    return MethodType(method, object)

def HookPeerEditor(peer):
    peer._basicEditString = peer.editString
    peer.editString = bindToThis(peer, DecisiveEditString)

def HookPeerPager(peer):
    peer._basicPageString = peer.page_string
    peer.page = peer.page_string = bindToThis(peer, DecisivePageString)

def Edit(peer, content = '', *args, **kwd):
    # (Parameterized) Decorator that starts the editing process.
    def startEditing(function):
        def terminateWithDisconnect(peer, content):
            peer.messenger = None
            return function(peer, content)

        peer.messenger = terminateWithDisconnect
        peer.editString(content, *args, **kwd)

        return None

    ##    def startEditing(function):
    ##        baseline = md5sum(content)
    ##        def saveIfChanged(peer, content):
    ##            if md5sum(content) != baseline:
    ##                function(peer, content) # prompt-for?
    ##            # else print something
    ##
    ##        peer.messenger = saveIfChanged
    ##        peer.editString(content, *args, **kwd)
    ##
    ##        return None

    return startEditing

# API.
@runtime.api(runtime.Player.Editor.API)
class EditorAPI:
    Edit = StartEditing = staticmethod(Edit)
    RichEditString = staticmethod(RichEditString)
    RichPageString = staticmethod(RichPageString)

# Extension Package.
from stuphmud.server.player import ACMD, ACMDLN, Option # For later.
from stuphos.runtime import Component

@ACMD('rich-editor*-select')
def doSelectRichEditor(peer, cmd, argstr):
    a = peer.avatar
    if a is not None:
        a.useRichEditor = not getattr(a, 'useRichEditor', False)
        print('You will now use the', \
                       'rich' if a.useRichEditor else 'basic', \
                       'text editor.', file=peer)

    return True

@ACMD('rich-pager*-select')
def doSelectRichPager(peer, cmd, argstr):
    a = peer.avatar
    if a is not None:
        a.useRichPager = not getattr(a, 'useRichPager', False)
        print('You will now use the', \
                       'rich' if a.useRichPager else 'basic', \
                       'string pager.', file=peer)

    return True

# Implement as component until it's moved into the core.  Then
# the hook install it can be called directly.
class RichText(Component):
    def onNewConnection(self, cltr, peer):
        try:
            HookPeerEditor(peer)
            HookPeerPager(peer)

        except Exception as e:
            print(f'[rich text:new connection] {e.__class__.__name__}: {e}')


@ACMDLN('libedit', Option('--list-directory', '--directory',
                          '--main', action = 'store_true'),
                   Option('--display', '--show',
                          action = 'store_true'))
def doEditLibrary(peer, command):
    from stuphmud.server.player import policy
    if peer.avatar in policy:
        from stuphlib import directory as stuphdir
        if command.options.list_directory:
            # Show main directory.
            peer.page(str(stuphdir.StuphLIB))

        elif command.args:
            object = command.args[0]

            try: filename = stuphdir.StuphLIB[object]
            except stuphdir.LibDataError as e:
                print('&r%s: %s&N' % (e.__class__.__name__, e), file=peer)
            else:
                if command.options.display:
                    with open(filename) as fl:
                        peer.page(fl.read())
                else:
                    # Edit the file.
                    with open(filename) as fl:
                        @Edit(peer, fl.read(), header = object)
                        def stuphlibObject(peer, content):
                            from shutil import copyfile
                            copyfile(filename, filename + '.bak')

                            with open(filename, 'wb') as fl:
                                fl.write(content)

                            print('Updated %s to %s (with backup)' % \
                                  (object, filename), file=peer)

        else:
            peer.page(command.help())

        return True


# Testing.
# is string.join(list|tuple) faster than string.join(generator)?
def pageLines(peer, s):
    def rebuild():
        x = s.split('\n')
        fmt = ' %%%dd  %%s' % len(str(len(x)))
        for (i, n) in enumerate(s.split('\n')):
            yield fmt % (i+1, n)

    peer.page_string('\n'.join(rebuild()) + '\n')

def main(argv = None):
    global PromptFor
    class PromptFor:
        def __init__(self, peer, callback, message = '', **kwd):
            self.callback = callback
            self.message = message

            peer.interpreter = self
            peer.prompt = message

        def __call__(self, peer, line):
            if self.callback(self, peer, line):
                self.regenerate(peer)
                return True

        def regenerate(self, peer):
            self.__class__(peer, self.callback, self.message)

    class Peer:
        def __init__(self, xxx_todo_changeme):
            (rows, cols) = xxx_todo_changeme
            self.rows = rows
            self.cols = cols
            self.prompt = None

        def interact(self):
            try:
                while self.interpreter(self, input(self.prompt)):
                    pass

            except EOFError:
                print() # self.interpreter(self, <quit-sequence>)

        def editString(self, content, header = None):
            edlin = LineEditor(self, (self.rows, self.cols), content,
                               header = HeaderToFit(header, self.cols) \
                               if header else '')
            self.interact()
            return edlin.content

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('--rows', type = int, default = 20)
    parser.add_option('--columns', type = int, default = 100)
    (options, args) = parser.parse_args(argv)

    dimensions = (options.rows, options.columns)

    content = open(args[0]).read() if args else ''
    Peer(dimensions).editString(content, header = args[0])

if __name__ == '__main__': main()
else: from stuphmud.server.player.shell import PromptFor
