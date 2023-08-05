# Copyright 2011 Clint Banis.  All rights reserved.
#
from .comm import TelnetConversation, SuMessageBuilder

# Event Handling (Automatic Processing).
# import mud

#@on.telnetCommand
#@mud.tools.breakOn
def process_command(peer, cmd):
    try: conversation = peer.telnet_conversation
    except AttributeError:
        conversation = peer.telnet_conversation = TelnetConversation()

    # This is where to handle other commands.
    ##    if type(cmd) is tuple:
    ##        # Filter for non-SE messages.
    ##        if len(cmd) == 2:
    ##            pass

    msg = conversation.receive_command(cmd)
    if msg is not None:
        return process_message(peer, msg)

def process_message(peer, msg):
    handler = getattr(peer, 'process_telnet_message', process_message_default)
    if callable(handler):
        return handler(peer, msg)

def process_message_default(peer, msg):
    try:
        # Put message in queue if avatar is accepting them.
        try: peer.avatar.telnet_messages.append(load_pickle(msg))
        except AttributeError:
            # Otherwise, just page the message to the player.        
            peer.page_string(str(load_pickle(msg)))

    except:
        from traceback import print_exc
        print_exc(file = peer)


# Manual Processing.
def process_peer(peer):
    builder = SuMessageBuilder()
    while True:
        data = peer.dequeue_input_block()
        if data is None:
            break

        msg = builder.receive_sudata(data)
        if msg is not None:
            return msg

def process_player(player):
    # (for deferred processing when everything's put
    # on a queue for later debugging)
    assert player.peer
    messages = getattr(player, 'telnet_messages', None)
    if messages is None:
        messages = player.telnet_messages = []

    msg = process_peer(player.peer)
    if msg is not None:
        messages.append(msg)
