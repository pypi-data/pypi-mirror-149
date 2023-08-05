# Player Event Framework.
class Trigger:
    def triggeredBy(self, event):
        pass
    def invokeTrigger(self, player):
        pass

class Event:
    def __init__(self, name, *args, **kwd):
        pass

def TriggerPlayerEvent(player, name, *args, **kwd):
    try: programs = player.programs
    except AttributeError: pass
    else:
        # This is lame: it should search through triggers and test them.
        try: trigger = programs[name]
        except (TypeError, KeyError): pass
        else:
            if isinstance(trigger, Trigger):
                # if trigger.triggeredBy(event)
                if player.implementor:
                    trigger.invokeTrigger(player, *args, **kwd)
