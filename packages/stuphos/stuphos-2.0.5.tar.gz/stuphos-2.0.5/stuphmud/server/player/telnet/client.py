# Tool for uploading/modifying player files via a telnet connection.
# Copyright 2011 Clint Banis.  All rights reserved.
from time import sleep
from configparser import DEFAULTSECT, ConfigParser
from os.path import expanduser
from telnetlib import Telnet
from pdb import set_trace, runcall
from optparse import OptionParser
import sys
import traceback

CONFIG_NAMES = ('username', 'password', 'host', 'port', 'operation',
                'remote-filename', 'local-filename', 'new-filename',
                'message-format', 'delay', 'show-output', 'prefix',
                'key-file')
CONFIG_DEFAULTS = dict((n, '') for n in CONFIG_NAMES)
CONFIG_FILE = '~/.telnetftp_client.cfg'

DEFAULT_TELNET_MODULE = 'mud.player.telnet'

def getCmdlnParser():
    parser = OptionParser()
    parser.add_option('--username')
    parser.add_option('--password')
    parser.add_option('--host')
    parser.add_option('--port')
    parser.add_option('--operation')
    parser.add_option('--remote-filename')
    parser.add_option('--command', dest = 'remote_filename')
    parser.add_option('--local-filename')
    parser.add_option('--new-filename')
    parser.add_option('--key-file', '--keyfile')
    parser.add_option('--telnet-module', default = DEFAULT_TELNET_MODULE)
    parser.add_option('--message-format', default = 'json')
    parser.add_option('-g', '--debug', action = 'store_true')
    parser.add_option('-w', '--delay', type = int, default = 0)
    parser.add_option('-C', '--config', default = CONFIG_FILE)
    parser.add_option('--section')
    parser.add_option('--show-output')
    parser.add_option('--prefix')
    return parser

def parse_cmdln(argv = None, parser = None):
    if parser is None:
        global __parser
        try: parser = __parser
        except NameError:
            parser = __parser = getCmdlnParser()

    return parser.parse_args(argv)

# XXX: This loads file config over cmdline options, instead of the other way around.
def loadConfig(options, config_file, section):
    if options.debug:
        set_trace()

    cfg = ConfigParser(defaults = CONFIG_DEFAULTS)
    cfg.read([config_file])

    for o in CONFIG_NAMES:
        value = cfg.get(section, o)
        if value is not '':
            o = o.replace('-', '_')
            setattr(options, o, value)

    # Validate.
    options.delay = int(options.delay)
    return options

def getConfigFile(config_file):
    i = config_file.rfind(':')
    if i >= 0:
        section = config_file[i+1:]
        config_file = config_file[:i]
    else:
        section = DEFAULTSECT

    return (config_file, section)

# Encryption Routines.
def LoadKeyfile(keyfile):
    return open(keyfile).read().strip()

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

def GetMessageDigest(key_iv, player_name_salt, payload):
    import hmac
    hash = hmac.new(key_iv)
    hash.update(player_name_salt)
    hash.update(payload)
    return hash.hexdigest()

# Session.
def login(options):
    telnet = Telnet(options.host, options.port)
    telnet.write('%s\r\n' % options.username)
    telnet.write('%s\r\n' % options.password)
    if options.delay:
        sleep(options.delay)

    telnet.write('telnet-control manage\r\n')
    return telnet

def logout(telnet):
    telnet.write('quit\r\n0\r\n')

def get_send_sudata_routine(module_name = None):
    module = __import__(module_name or DEFAULT_TELNET_MODULE, globals(), locals(), [''])
    return module.send_sudata

def sendData(conn, data, send_sudata_proc, delay = False):
    send_sudata_proc(conn.sock, data)

    if delay:
        sleep(delay)

def printOutput(output, stream):
    output = output.split('\n')
    output = ' %  ' + '\n %  '.join(output)
    print(output, file=stream)

def getPrefixedOperation(options):
    if options.prefix:
        return '%s:%s' % (options.prefix, options.operation)
    return options.operation

def buildCmdlnOperation(options, args):
    if options.config:
        (config_file, section) = getConfigFile(options.config)
        loadConfig(options, expanduser(options.config), section)

    if options.operation not in ['list']:
        assert options.remote_filename

    assert options.host
    assert options.port
    assert options.username
    assert options.password

    keyfile = options.key_file
    if keyfile:
        key = LoadKeyfile(keyfile)

    # Validate operation.
    if options.operation in ['create', 'append']:
        filename = options.local_filename
        assert filename
        content = open(filename).read()

        if keyfile:
            assert options.operation == 'create'
            content = encryptArmored(key, content)

    elif options.operation == 'rename':
        newname = options.new_filename
        assert newname

    elif options.operation not in ['delete', 'touch', 'truncate', 'list', 'stat', 'view',
                                   'decrypt', 'execute', 'executefile']:

        raise NameError(options.operation)

    if options.operation in ['execute', 'executefile']:
        assert key

    # Validate format.
    if options.message_format == 'json':
        from simplejson import dumps
    elif options.message_format == 'pickle':
        from pickle import dumps
    else:
        raise NameError(options.message_format)

    # Configure Rest.
    if options.debug:
        set_trace()

    if options.show_output == '--':
        stream = sys.stdout
    elif options.show_output:
        stream = open(options.show_output, 'w')

    # Build Operation.
    command = [getPrefixedOperation(options)]

    if options.operation in ['execute', 'executefile']:
        command.append(GetMessageDigest(key, options.username, options.remote_filename))

    if options.operation != 'list' or options.remote_filename:
        command.append(options.remote_filename)

    if options.operation in ['create', 'append']:
        command.append(content)
    elif options.operation == 'rename':
        command.append(newname)

    command = dumps(command)
    command = '%s:%s' % (options.message_format.upper(), command)

    return command

def process_batch_file(filename):
    this = []
    for line in open(filename):
        line = line.rstrip()
        if line.endswith('\\'):
            this.append(line[:-1].rstrip())
        else:
            yield ' '.join(this)
            this = []

    if this:
        yield ' '.join(this)

def main(argv = None):
    # Configure send proc & generate message.
    (options, args) = parse_cmdln(argv)
    commands = [buildCmdlnOperation(options, args)]

    if options.batch_file:
        for cmdln in process_batch_file(options.batch_file):
            commands.append(buildCmdlnOperation(*parse_cmdln(cmdln)))

    # General telnet session.
    send_sudata_proc = get_send_sudata_routine(options.telnet_module)
    telnet = login(options)
    try:
        # Send via Telnet.
        print('Sending %d bytes (%dk/%dM)' % (len(command),
                                                             len(command) / 1024.,
                                                             len(command) / 1024 / 1024.), file=sys.stderr)

        print(repr(command[:80]), file=sys.stderr)

        # Multiple-commands.
        for cmd in commands:
            sendData(telnet, cmd, send_sudata_proc, options.delay)

        # Output.
        if options.show_output:
            while True:
                output = telnet.read_very_eager()
                if not output:
                    break

                printOutput(output, stream)

    except: traceback.print_exc()
    finally:
        logout(telnet)
        if options.show_output:
            printOutput(telnet.read_all(), stream)

if __name__ == '__main__':
    main()
