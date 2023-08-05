# Extensions -- Executable.
def nling(function):
    def nl(*args, **kwd):
        return '\n'.join(function(*args, **kwd))

    return nl

def indent(string, tab = '    ', level = 1):
    tab *= level
    return tab + ('\n' + tab).join(string.split('\n'))


class filesystem:
    # Represent a folder tree as structural input to the upload routine.

    def __init__(self, path):
        self.path = path

    def contents(self, path):
        return path.read()

    def __len__(self):
        return len(self.path.listing)

    def __getitem__(self, name):
        if name in ['structures', 'interfaces']:
            try: return dict((p.basename, self.contents(p)) for p in
                             self.path(name).listing if not p.isdir)

            except FileNotFoundError:
                return dict()

        raise KeyError(name)

    def iteritems(self):
        try: i = self.path.listing
        except FileNotFoundError: pass
        else:
            for p in i:
                if p.isdir:
                    yield (p.basename, self.__class__(p))
                else:
                    yield (p.basename, self.contents(p))

    def items(self):
        return list(self.iteritems())


def packageBuild(path):
    @nling
    def w(o):
        if isinstance(o, (dict, filesystem)):
            for (name, value) in o.items():
                if isinstance(value, (list, tuple, dict, filesystem)):
                    yield f'{name}:'
                    yield indent(w(value))

                elif isinstance(value, str):
                    yield f'{name}::'
                    yield indent(value)

                else:
                    yield f'{name}: {repr(value)}'

        elif isinstance(o, (list, tuple)):
            if o:
                for value in o:
                    o = w(o)
                    o = o.split('\n')
                    if len(o) > 1:
                        yield '- ' + o[0]
                        yield indent('\n'.join[1:], tab = '  ')
                    else:
                        yield '- ' + o[0]
            else:
                yield '[]'

        else:
            yield repr(o)

    return w(filesystem(path))


def setActivityProgrammer(core, path, name, progr):
    node = core.root.lookup(*(path + [name]))
    node.programmer = progr # XXX Todo: Programmer(progr)?

ALT_TYPES = ('structures', 'interfaces', 'media')

def uploadStructure(core, path, structure, set_programmers = False):
    structs = []
    media = []

    try: structs.extend(list(structure['structures'].items()))
    except KeyError: pass

    try: structs.extend(list(structure['interfaces'].items()))
    except KeyError: pass

    try: media.extend(list(structure['media'].items()))
    except KeyError: pass

    services = [(name, s) for (name, s) in structure.items()
                if name not in ALT_TYPES]

    def ensure(path):
        path = path.split('/')
        u = core.root.lookup

        for i in range(1, len(path)+1):
            folder = path[:i]

            try: u(*folder)
            except KeyError:
                core.addFolder('/'.join(folder[:i-1]), folder[-1])

    def install(path, struct, add, isMedia = False):
        # head = (path + '/') if path else ''

        if path:
            head = path + '/'
            ensure(path)
        else:
            head = ''

        for (name, s) in struct:
            name = str(name) # Because it gets __sqlrepr__ attr which might be complex.

            if isMedia:
                if isinstance(s, str):
                    s = b64_decode(s)
                    add(path, name, s)

                elif isinstance(s, (dict, filesystem)):
                    try: content = s['content']
                    except KeyError: pass
                    else:
                        try: content_type = s['type']
                        except KeyError: content_type = None

                        content = b64_decode(content)
                        add(path, name, content, content_type)

            else:
                if isinstance(s, str):

                    # print(f'{add.__name__}({path}/{name})')
                    add(path, name, s)

                elif isinstance(s, (dict, filesystem)):
                    try: content = s['program']
                    except KeyError: pass
                    else:
                        # If program is set, programmer must be set or it's added as a folder.
                        try: progr = s['programmer']
                        except KeyError: pass
                        else:
                            if len(s) == 2:
                                ensure(path)

                                # print(f'adding module: {path} {name} [{progr}]')

                                core.addModule(path, name, content)
                                if set_programmers:
                                    setActivityProgrammer(core, path, name, progr)

                                continue

                    # debugOn()

                    # print(f'adding folder: {path}/{name}')
                    # assert not '/' in name
                    if path:
                        ensure(path + '/' + name)
                    else:
                        ensure(name)

                    uploadStructure(core, head + name, s) # recurse


    # debugOn()
    install(path, structs, core.addStructure)
    install(path, services, core.addModule)
    install(path, media, core.addMedia, isMedia = True)


class fsPackageCore:
    # AgentSystem replacement for extracting packages to filesystem.
    class Node:
        pass

    class Folder(Node, dict):
        def lookup(self, path, *args):
            return self[path]

    def __init__(self, path):
        self.path = io.path(path)
        self.root = self.Folder()

    def addFolder(self, *args, **kwd):
        print('addfolder ' + str(args))
    def addModule(self, *args, **kwd):
        print('addmodule ' + str(args))
    def addStructure(self, *args, **kwd):
        print('addstructure ' + str(args))
    def addMedia(self, *args, **kwd):
        print('addmedia ' + str(args))


def packageUnpackTo(structure, dest_dir, mount_point = None):
    if isinstance(structure, str):
        from stuphos.language.document.interface import document
        structure = document(structure)

    core = fsPackageCore(dest_dir)
    uploadStructure(core, mount_point or '', structure)

def packageStreamUnpackTo(input, output, mount_point = None):
    '''
    --admin-script=ph.interpreter.mental.library.extensions.packageStreamUnpackTo \
    -x bin.package -x bin

    '''

    input = open(input).read()
    return packageUnpackTo(input, output, mount_point = mount_point)


def unpackMain(options, args):
    if len(args) != 2:
        print('Usage: unpack <input package> <output path>')
        return

    (input, output) = args

    packageStreamUnpackTo(input, output, options.mount_point)


USAGE = \
'''
export PYTHONPATH=<path-to-common>:<path-to-stuphos>
python -m stuphos.management.packaging -o jhcore.package path/to/LambdaMOO/core.db

'''

def main(argv = None):
    # debugOn()
    from optparse import OptionParser
    parser = OptionParser(usage = USAGE)
    parser.add_option('-o', '--output-file', '--output')
    parser.add_option('-i', '--input-file', '--input')
    parser.add_option('-u', '--unpack', action = 'store_true')
    parser.add_option('--mount-point')
    (options, args) = parser.parse_args(argv)

    if options.unpack:
        return unpackMain(options, args)

    if options.input_file:
        assert not args
        input = options.input_file
    else:
        assert len(args) == 1
        input = args[0]

    if options.output_file:
        output = open(options.output_file, 'w')
    else:
        from sys import stdout as output

    import op

    output.write(str(packageBuild(io.path(input))))

if __name__ == '__main__':
    main()
