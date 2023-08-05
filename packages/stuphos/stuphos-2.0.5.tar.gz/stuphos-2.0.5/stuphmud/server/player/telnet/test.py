#!python
# Copyright 2011 Clint Banis.  All rights reserved.
#
# Testing.
class Peer:
    def __init__(self, input):
        self._input_q = Queue()
        self.enqueue_input(input)

    def dequeue_input_block(self, mode = 'telnet'):
        while True:
            try: block = self._input_q.get_nowait()
            except Empty:
                return

            if mode == 'telnet':
                if type(block) is not tuple:
                    continue
                if len(block) not in (2, 3):
                    continue

            elif mode == 'line':
                if (type) is not str:
                    continue

            return block

    def input_queue_for(self, mode = 'telnet'):
        while True:
            block = self.dequeue_input_block(mode = 'telnet')
            if block:
                yield block
            else:
                break

    def enqueue_input(self, input):
        for block in input:
            self._input_q.put(block)

from optparse import OptionParser
def parse_cmdln(argv = None):
    parser = OptionParser()
    parser.add_option('-d', '--debug-level', '--debug', action = 'count', default = 0)
    parser.add_option('-m', '--message')
    parser.add_option('-F', '--message-file')
    return parser.parse_args(argv)

def generate_default_message():
    msg = '\n'.join(chr(c) * 40 for c in range(ord('a'), ord('z') + 1))
    msg += '\n'
    msg *= 10
    return msg

def generate_subnegotiation_message(options):
    if options.message:
        msg = options.message
    elif options.message_file:
        msg = open(options.message_file).read()
    else:
        msg = generate_default_message()

    for data in prepare_sudata_segments(msg):
        yield data

def inspect(**ns):
    from code import InteractiveConsole as IC
    try: import readline
    except ImportError: pass
    IC(locals = ns).interact('')

def main(argv = None):
    global DEBUG_LEVEL
    (options, args) = parse_cmdln(argv)
    DEBUG_LEVEL = options.debug_level

    if options.debug_level:
        debug()

    # peer = Peer(generate_subnegotiation_message(options))
    # input = peer.input_queue_for('telnet')

    builder = SuMessageBuilder()
    for data in generate_subnegotiation_message(options):
        msg = builder.receive_sudata(data)
        if msg is not None:
            inspect(msg = msg)

if __name__ == '__main__':
    main()
