# Copyright 2011 Clint Banis.  All rights reserved.
#

from io import StringIO as new_buffer

# Formats.
# import cPickle as pickle
from pickle import dump as save_pickle, dumps as save_pickle_string
from pickle import load as load_pickle, loads as load_pickle_string

def serialize_integer(n):
    return 'I%d.' % int(n)

class UnknownLengthMarker(Exception):
    pass

def deserialize_integer(buf):
    c = buf.read(1)
    if c != 'I':
        raise UnknownLengthMarker(c)

    digits = []
    while True:
        c = buf.read(1)
        if c == '.':
            break

        assert c.isdigit()
        digits.append(c)

    assert digits
    return int(''.join(digits))

# Message Marshalling.
MAX_RAW_INPUT_LENGTH = 512
MAX_SUBUFFER_SIZE    = MAX_RAW_INPUT_LENGTH

PACKET_SIZE          = MAX_SUBUFFER_SIZE - 10

# XXX Escape telnet sequences!
# if IAC in data:
#    data = data.replace(IAC, IAC + IAC)
def prepare_sudata_segments(data, packet_size = PACKET_SIZE):
    # Telnet processing segments overflow data automatically, but it's convenient
    # to packetize it here in the client to control bandwidth.
    assert type(data) is str
    datalength = len(data)

    n = serialize_integer(datalength)
    s = 0

    if packet_size <= 0:
        yield '%s%s' % (n, data)
        return # StopIteration?

    # First packet will be offset by the message size overhead.
    e = packet_size - len(n)
    yield '%s%s' % (n, data[:e])

    s = e
    e += packet_size

    while s < datalength:
        yield data[s:e]
        s = e
        e += packet_size
        if e > datalength:
            e = datalength

from telnetlib import IAC, SB, SE
def embed_segment(part):
    return '%s%s%s%s%s' % (IAC, SB, part, IAC, SE)

def send_sudata(sock, data, **kwd):
    for part in prepare_sudata_segments(data, **kwd):
        sock.sendall(embed_segment(part))

def send_supickle(sock, object, **kwd):
    send_sudata(sock, save_pickle_string(object), **kwd)

# Message Unmarshalling.
class SuMessageBuilder:
    def __init__(self):
        self.readq = new_buffer()
        self.message_buf = None

        self.message_size = 0
        self.message_left = 0

    def receive_command(self, cmd):
        if type(cmd) is tuple:
            # Filter for SE messages.
            if len(cmd) == 3 and cmd[0] == ord(SE):
                return self.receive_sudata(cmd[2])

    # Subnegotiation message building.
    def push_data(self, data):
        pos = self.readq.tell()
        self.readq.write(data)
        self.readq.seek(pos)

    def read_integer(self):
        return deserialize_integer(self.readq)
    def read_message(self, bytes):
        return self.readq.read(bytes)

    def receive_sudata(self, data):
        self.push_data(data)

        if self.message_buf is None:
            self.message_size = self.read_integer()
            assert self.message_size >= 0
            self.message_buf = new_buffer()
            self.message_left = self.message_size

        data = self.read_message(self.message_left)

        self.message_left -= len(data)
        self.message_buf.write(data)

        # Todo: If nothing's left at the end of the readq, truncate it.

        if not self.message_left:
            return self.reset_message()

    def reset_message(self):
        buf = self.message_buf
        self.message_buf = None
        buf.reset()
        # Reset message_size/left?
        return buf

TelnetConversation = SuMessageBuilder
