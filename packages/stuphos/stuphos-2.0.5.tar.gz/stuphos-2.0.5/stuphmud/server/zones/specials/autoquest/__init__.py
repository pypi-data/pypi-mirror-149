# Auto-Quest Generic Senarios Facility & Special Procedure.
# Copyright 2010-2021 Clint Banis.  All rights reserved.
#
from os.path import dirname, join as joinpath
from traceback import print_exc as traceback
from pprint import pformat
from sys import exc_info
from errno import ENOENT
from time import time as now
from io import StringIO as NewBuffer
from random import randint, choice
import re
from string import Template
import imp

try:
    from yaml import dump as dumpYaml
    from yaml import load as loadYaml
except ImportError:
    dumpYaml = loadYaml = False

from stuphos.runtime import newComponent, LookupClassObject as LookupSenarioObject
from stuphos.runtime.facilities import Facility
#from stuphos.zones.specials import SpecialInstantiator
from stuphos.management.config import loadConfig
from stuphmud.server.player import HandleCommandError
from stuphmud.server.player.shell import PromptFor
from stuphos.runtime.registry import getObject, delObject
from stuphos import enqueueHeartbeatTask
from stuphos import invokeTimeoutForHeartbeat

from world import mobile as MobilePrototype
from world import item as ItemPrototype
from world import room as RealRoom

# todo: wagering

class Object(dict):
    def __init__(self, **kwd):
        self.__dict__ = self
        self.update(kwd)
        self.validate()

    def validate(self):
        # Load internally.
        pass

    def __getitem__(self, name):
        return self.get(name)

def evaluate(value, **values):
    # Privileged: Execute as code for value!
    # Todo: utilize mud.runtime.sandbox module!
    co = compile(value, '<value>', 'eval')
    return eval(co, values, values)

def getFileText(filename):
    try: return open(filename).read()
    except IOError as e:
        if e.errno != ENOENT:
            (etype, value, tb) = exc_info()
            raise etype(value).with_traceback(tb)

def dumpYamlWithIndent(object, indent = 0):
    if type(indent) is int:
        indent = indent * ' '

    return '\n'.join(indent + line for line in dumpYaml(object).split('\n'))

def chance(n):
    return randint(1, 100) < n

def reloadThisModule():
    return imp.reload(__import__(__name__, globals(), locals(), ['']))

# Facility.
def getThisDir():
    return dirname(__file__)
def getConfigFile():
    return joinpath(getThisDir(), 'quests.cfg')

class QuestControl(Facility):
    NAME = 'Quest::Control'

    ACTIVATIONS_OBJECT_NAME = '%s::Activations' % NAME
    REWARDS_OBJECT_NAME = '%s::Rewards' % NAME

    class Manager(Facility.Manager):
        MINIMUM_LEVEL = Facility.Manager.IMPLEMENTOR
        VERB_NAME = 'qc*ontrol'

        def do_destroy(self, peer, cmd, args):
            for name in args:
                if name == 'activations':
                    delObject(QuestControl.ACTIVATIONS_OBJECT_NAME)
                    print('Destroyed activations.', file=peer)

                elif name == 'rewards':
                    delObject(QuestControl.REWARDS_OBJECT_NAME)
                    print('Destroyed rewards.', file=peer)

                else:
                    print('Unknown destroy option: %r' % name, file=peer)

        def do_reload(self, peer, cmd, args):
            s = self.facility.get()
            if s is not None:
                for name in args:
                    if name == 'senarios':
                        s.loadSenarios()
                        print('Reloaded senarios.', file=peer)

                    elif name == 'config':
                        s.loadConfig()
                        print('Reloaded configuration.', file=peer)

                    elif name == 'help':
                        s.loadHelp()
                        print('Reloaded help.', file=peer)

                    elif name == 'behavior':
                        s.loadBehavior()
                        print('Reloaded behavior.', file=peer)

                    else:
                        print('Unknown reload option: %r' % name, file=peer)

    @classmethod
    def create(self):
        return newComponent(self)

    def __instance_init__(self):
        self.loadConfig()
        self.loadSenarios()
        self.loadHelp()
        self.loadBehavior()

    def loadConfig(self):
        self.config = loadConfig(getConfigFile())
        self.cfgsection = self.config.getSection('QuestControl', **{'config-dir': getThisDir()})

    def loadSenarios(self):
        self.senarios = list(loadSenarios(self.config))

    def loadHelp(self):
        helpfile = self.getConfig('help-screen')
        screen = getFileText(helpfile) if helpfile else None

        helpfile = self.getConfig('help-topics')
        topics = []

        if helpfile:
            for (keywords, minlevel, text) in parseHelpFile(helpfile):
                topics.append((keywords.split(), text))

        self.help = Object(screen = screen, topics = topics)

    def loadBehavior(self):
        actions = []
        conversation = []
        self.behavior = Object(actions = actions, conversation = conversation)

        behaviorfile = self.getConfig('behavior-file')
        if behaviorfile:
            document = getFileText(behaviorfile)
            if document:
                for section in loadYaml(document):
                    for (name, group) in section.items():
                        if name == 'actions':
                            actions.append(group)
                        elif name == 'conversation':
                            for element in group:
                                conversation.append(ConversationElement(element['match'],
                                                                        element['response']))

    def getStatus(self):
        def analyze():
            yield '&yActivations&N'
            yield '&r===========&N'

            for a in self.activations:
                yield dumpYamlWithIndent(a, indent = 4)

        return '\r\n'.join(analyze()) + '\r\n'

    def getConfig(self, name):
        return self.cfgsection[name]

    def getHelpText(self, topic = None):
        if not topic:
            return self.help.screen
        else:
            if isinstance(topic, str):
                topic = topic.upper().split()
            elif isinstance(topic, (list, tuple)):
                topic = [t.upper() for t in topic]
            else:
                raise ValueError(topic)

            # Search keywords:
            # todo: allow quoted word groups
            for (names, text) in self.help.topics:
                for word in topic:
                    if word not in names:
                        break
                else:
                    return text

    # World Component Routines:
    # Note: technically, as a component, this class should override its __call__
    # method and dispatch through that to the activations, handling any possible
    # future events.
    def onSlayMobile(self, ctlr, victim, killer):
        for a in self.activations:
            o = getattr(a, 'onSlayMobile', None)
            if callable(o):
                o(victim, killer)

    def onDealDamage(self, ctlr, attacker, victim, dam, wtype):
        for a in self.activations:
            o = getattr(a, 'onDealDamage', None)
            if callable(o):
                o(attacker, victim, dam, wtype)

    def onPurgeMobile(self, ctlr, victim, wizard):
        for a in self.activations:
            o = getattr(a, 'onPurgeMobile', None)
            if callable(o):
                o(victim, wizard)

    def onDeathTrap(self, ctlr, victim, cause):
        for a in self.activations:
            o = getattr(a, 'onDeathTrap', None)
            if callable(o):
                o(victim, cause)

    # Senarios.
    def selectAllSenarios(self):
        return Selection(self.senarios)
    def selectSenariosByClass(self, cls):
        return Selection(self.senarios).selectByClass(cls)
    def selectSenariosByName(self, name):
        return Selection(self.senarios).selectByName(name)
    def findSenariosElligibleFor(self, player):
        return Elligibility(self.senarios, player)

    # Activations.
    @property
    def activations(self):
        return getObject(self.ACTIVATIONS_OBJECT_NAME,
                         create = list)

    def addActivation(self, a):
        self.activations.append(a)
    def removeActivation(self, a):
        actvtns = self.activations
        if a in actvtns:
            actvtns.remove(a)

    def getActivationsFor(self, player):
        return [a for a in self.activations if a.player is player]

    # Rewards.
    @property
    def rewards(self):
        return getObject(self.REWARDS_OBJECT_NAME,
                         create = self.loadRewards)

    def loadRewards(self):
        return dict()

    def saveRewards(self):
        # todo: backup
        pass

    def postReward(self, player, kitty):
        self.rewards.setdefault(player.idnum, []).append(kitty)
        self.saveRewards()

    def getRewardsFor(self, player):
        return self.rewards.get(player.idnum, [])

    def removeReward(self, player, kitty):
        try: self.rewards[player.idnum].remove(kitty)
        except (KeyError, IndexError): pass
        self.saveRewards()

    # A little SpecProc behavior.
    def getRandomActionGroup(self):
        actions = self.behavior.actions
        if actions:
            return choice(actions)

        return ()

    def getResponseAction(self, commstr):
        for element in self.behavior.conversation:
            for response in element(commstr):
                yield response

# Install.
QuestControl.manage()
# QuestControl.get(create = True)

class ConversationElement:
    def __init__(self, pattern, response):
        self.pattern = re.compile(pattern)
        self.template = Template(response)

    def __call__(self, commstr):
        match = self.pattern.match(commstr)
        if match is not None:
            # XXX -- what if it's not a dict match?
            yield self.template.substitute(match.groupdict())

# Could very well rely on stuphlib for this:
def parseHelpFile(filename):
    try: fl = open(filename)
    except IOError as e:
        if e.errno is ENOENT:
            return

        (etype, value, tb) = exc_info()
        raise etype(value).with_traceback(tb)

    while True:
        line = fl.readline()
        if line == '':
            break

        strippedLine = line.strip()
        if strippedLine == '$':
            return # end of records/file

        if strippedLine != '#':
            # Format error
            return

        keywords = ' '.join(fl.readline().upper().split())
        minlevel = int(fl.readline())
        content = NewBuffer()

        while True:
            line = fl.readline()
            if line.strip() == '~':
                break

            content.write(line)
            content.write('\r\n')

        content = content.getvalue()
        yield (keywords, minlevel, content)

def pushFlagStatus(flags, name, object, newValue):
    stack = getattr(object, 'flagstack_%s' % name, [])
    stack.append(getattr(flags, name))
    setattr(flags, name, newValue)
def popFlagStatus(flags, name, object, defaultValue):
    try: stack = getattr(object, 'flagstack_%s' % name)
    except AttributeError: pass
    else:
        try: setattr(flags, name, stack.pop())
        except IndexError: setattr(flags, name, defaultValue)

def startQuestStatus(player, object):
    pushFlagStatus(player.preferences, 'Quest', object, True)
def endQuestStatus(player, object):
    popFlagStatus(player.preferences, 'Quest', object, False)

class Kitty(Object):
    # External reward storage container.
    def validate(self):
        self.items = list(self.get('items', []))
        self.gold = int(self.get('gold', 0))
        self.points = dict(self.get('points', Object(quest = 0,
                                                     platinum = 0,
                                                     gold = 0,
                                                     silver = 0,
                                                     merit = 0)))

    def addItem(self, item):
        self.items.append(item)
    def addGold(self, gold):
        self.gold += gold
    def addPoints(self, type, amount):
        self.points[type] = self.points.get(type, 0) + amount

    # Serialization: serialize only item numbers (or obj_file_elem)
    # Gold and points are primitive

# Senarios Model.
SENARIO_SUBSTITUTES = {'builtin': __name__}

def loadQuest(quest, **kwd):
    qtype = quest.get('quest-type')
    if qtype:
        # Resolve name and senario object.
        qtype = Template(qtype).substitute(SENARIO_SUBSTITUTES)

        try: senarioClass = LookupSenarioObject(qtype)
        except ValueError: pass

        # Load document tree into object node.
        else: return senarioClass(**dict(quest, **kwd))

def loadSenarios(cfg):
    # Experimental:
    try: from dom.XML import FormatDocumentSource, XML
    except ImportError: pass
    else:
        XMLDOM = cfg.getSection('XML.DOM', **{'config-dir': getThisDir()})
        for option in XMLDOM:
            if option.startswith('filepath'):
                doc = open(XMLDOM[option]).read()
                doc = FormatDocumentSource(doc)
                doc = XML(doc)

                # Just return raw document.
                yield doc

    try: from yaml import load as loadYaml
    except ImportError: pass
    else:
        YAML = cfg.getSection('YAML', **{'config-dir': getThisDir()})
        for option in YAML:
            if option.startswith('filepath'):
                for quest in loadYaml(open(YAML[option])):
                    q = loadQuest(quest)
                    if q is not None:
                        yield q

# Time-Limits.
def seconds(value):
    return value
def minutes(value):
    return seconds(value) * 60
def hours(value):
    return minutes(value) * 60
def days(value):
    return hours(value) * 24
def weeks(value):
    return days(value) * 7
def months(value):
    return weeks(value) * 4
def years(value):
    return days(value) * 365.25
def mudhours(value):
    return seconds(75)
def muddays(value):
    return mudhours(35)
def mudmonths(value):
    return mudmonths(0)
def mudyears(value):
    return mudmonths(35)

timeFunctions = dict(seconds = seconds, minutes = minutes, hours = hours, days = days,
                     weeks = weeks, months = months, years = years,
                     ticks = mudhours, mudhours = mudhours, muddays = muddays,
                     mudmonths = mudmonths, mudyears = mudyears)

def evaluateTimeLimit(activation, value):
    if isinstance(value, str):
        ns = timeFunctions.copy()
        ns['player'] = activation.player

        return evaluate(value, **ns)

    if type(value) is not int and value is not None:
        raise ValueError(value)

    return value

# Requirements.
class Requirement:
    def __init__(self, code):
        self.code = code
    def __call__(self, player):
        return bool(evaluate(self.code, player = player))

    class Or:
        def __init__(self, decisions):
            self.decisions = decisions
        def __call__(self, player):
            for d in self.decisions:
                if d(player):
                    return True

            return False

    class Comparison:
        class Op:
            def __init__(self, attribute):
                self.attribute = attribute

        def __init__(self, cmp, value):
            self.cmp = cmp
            self.value = value

        def __call__(self, player):
            return self.cmp(player, self.value)

        class Equal(Op):
            def __call__(self, player, value):
                return getattr(player, self.attribute) == value

        class GreaterThan(Op):
            def __call__(self, player, value):
                return getattr(player, self.attribute) > value

        class GreaterThanOrEqual(Op):
            def __call__(self, player, value):
                return getattr(player, self.attribute) >= value

        class LessThan(Op):
            def __call__(self, player, value):
                return getattr(player, self.attribute) < value

        class LessThanOrEqual(Op):
            def __call__(self, player, value):
                return getattr(player, self.attribute) <= value

POPULAR_COMPARISON = {'min-level': Requirement.Comparison.GreaterThanOrEqual('level'),
                      'remort': Requirement.Comparison.GreaterThanOrEqual('remort'),
                      'gold': Requirement.Comparison.GreaterThanOrEqual('gold_on_hand')}

def buildDecisions(structure):
    if isinstance(structure, (list, tuple)):
        for req in structure:
            if isinstance(req, dict):
                for (name, value) in req.items():
                    if name == 'either':
                        yield Requirement.Or(buildDecisions(value))
                    elif name in POPULAR_COMPARISON:
                        yield Requirement.Comparison(POPULAR_COMPARISON[name], value)
                    else:
                        yield Requirement(value)

class Senario(Object):
    # Activation.
    class Activation(Object):
        def validate(self):
            self.__activated = True

        def isActivated(self):
            try: return self.__activated
            except AttributeError:
                return False

        def deactivate(self, reason = None):
            if self.isActivated():
                qc = QuestControl.get()
                if qc is not None:
                    qc.removeActivation(self)
                    endQuestStatus(self.player, self)

                    if reason:
                        peer = self.player.peer
                        if peer is not None:
                            # todo: string interpolation of reason
                            print(reason, file=peer)

                self.__activated = False

        TIMELIMIT_EXPIRATION_MESSAGE = '&M*&N &wThe time limit for the quest has expired!&N &M*&N'

        def onExpiration(self):
            self.deactivate(reason = self.TIMELIMIT_EXPIRATION_MESSAGE)

        def percentComplete(self):
            raise NotImplementedError

    DEFAULT_BEGIN_MESSAGE = '&M*&N &wWelcome to the quest!&N &M*&N\r\n'
    DEFAULT_END_MESSAGE = '&M*&N &wThe %(name)s quest is complete!&N &M*&N\r\n'

    activations = []

    def activate(self, player, **values):
        # Set up internal Activation state.
        a = self.Activation(player = player, senario = self, **values)
        self.setdefault('activations', []).append(a)

        qc = QuestControl.get()
        if qc is not None: # XXX else, error
            qc.addActivation(a)

        startQuestStatus(player, self)
        peer = player.peer
        if peer is not None:
            msg = self.get('begin-message', self.DEFAULT_BEGIN_MESSAGE)
            if msg:
                peer.page_string(msg)

        # timeout = evaluateTimeLimit(a, self.get('time-limit'))
        timeout = None
        a.time_limit = timeout
        a.start_time = now()

        if timeout is not None:
            invokeTimeoutForHeartbeat(timeout, a.onExpiration)

        # Now, charge the player anything set forth in requirements...

        return a

    # Sorting, Naming & Reports
    def nameMatch(self, name):
        return self.get('name', '').lower().split() == name.lower().split()
    def classMatch(self, cls):
        return self.get('class', '').lower().split() == cls.lower().split()

    def isElligible(self, player):
        for check in buildDecisions(self.get('requirements')):
            if not check(player):
                return False

        return True

    def shortName(self):
        cls = self.get('class')
        name = self.get('name', '?')
        return name if cls is None else '%s (%s)' % (name, cls)

    def shortDescription(self):
        return '[%(quest-type)10.10s] %(class)10.10s %(name)20.20s %(min-level)5.5s/%(max-level)5.5s' % self
    def detailedDescription(self):
        d = self.get('description')
        if type(d) in (list, tuple): d = '\r\n'.join(d)
        return '%s\r\n%s' % (d, self) if d else str(self)

    def __str__(self):
        return dumpYamlWithIndent(self, indent = 4)


class SharedSenario:
    name = 'shared'

    def message(self, player, message):
        from email.message import Message
        if isinstance(message, Message):
            if message.get_content_type() == 'text/html':
                return self.htmlMessage(player, message.get_payload())
            else:
                assert message.get_content_type() == 'text/plain'
                message = message.get_payload()

        message = "%s quest says, '%s'" % (player.name, message)
        for a in self.activations:
            if a.player.peer:
                print(message, file=a.player.peer)

    @runtime.available(runtime.Web.Adapter.SessionManager)
    def htmlMessage(adapter, self, player, message):
        # message = scrubMessage(message)

        message = '''\
            <div class="posted-quest">
                <h4><a href="/poke/{player.name}">{player.name}</a></h4>
                <h5>{timestamp} on {quest.name}</h5>
                <table>
                <tr>
                  <td>
                    <img src="/avatar/{player.name}">
                  </td>
                  <td>
                    <pre class="message">
                    {message}
                    </pre>
                  </td>
                </tr>
                </table>
            </div>
            '''.format(player = player, quest = self,
                       timestamp = 'past', message = message)

        for a in self.activations:
            p = a.player.peer
            if p:
                p = adapter.findSessionByPeer(p)
                if p:
                    p.postMessages(['html-panel', message])


from stuphos.runtime.architecture.api import writeprotected
class ProtectedSenario(writeprotected, SharedSenario, Senario):
    def isElligible(self, player):
        # todo: type check
        return Senario.isElligible(self, player._object)
    def activate(self, player, values = dict()):
        # todo: type check
        return Senario.activate(self, player._object, **values)


# todo: move these into the Senario class.
class Selection:
    def __init__(self, senarios):
        self.senarios = list(senarios)

    def __iter__(self):
        return iter(self.senarios)
    def __str__(self):
        return self.shortDescription()
    def __bool__(self):
        return len(self.senarios) > 0

    def subselect(self, senarios):
        return self.__class__(senarios)
    def selectByName(self, name):
        return self.subselect(s for s in self.senarios if s.nameMatch(name))
    def selectByClass(self, cls):
        return self.subselect(s for s in self.senarios if s.classMatch(cls))

    def shortDescription(self):
        return '\r\n'.join(s.shortDescription() for s in self) + '\r\n'
    def detailedDescription(self):
        return '\r\n'.join(s.detailedDescription() for s in self) + '\r\n'
    def numberedDescription(self):
        return '\r\n'.join('#%3d %s' % (nr, self.senarios[nr].shortDescription()) \
                           for nr in range(len(self.senarios)))

class Elligibility(Selection):
    def __init__(self, senarios, player):
        Selection.__init__(self, (s for s in senarios if s.isElligible(player)))
        self.player = player

    def subselect(self, senarios):
        return self.__class__(senarios, self.player)

PROMPT_YESNO = "Please type 'yes' or 'no': "

def joinSenario(player, senario):
    def confirmJoin(peer, line):
        line = line.strip().lower()
        if line == 'yes':
            # Let the prompt cycle lift the writing mask.
            enqueueHeartbeatTask(activateForPlayer, senario, player)

        elif line not in ['n', 'no']:
            return True # re-prompt

    PromptFor(player.peer, confirmJoin, write_mode = True,
              message = PROMPT_YESNO)

def selectSenario(player, senarios):
    def performSelect(peer, line):
        line = line.lower().strip()
        if line.isdigit():
            try: s = senarios[int(line)]
            except IndexError: pass
            else:
                # Now pass to join-senario confirmation.
                joinSenario(player, s)
                return

        if line == 'quit':
            return
        if line:
            print('Invalid selection: %r' % line, file=peer)

        return True # re-prompt

    PromptFor(player.peer, performSelect, write_mode = True,
              message = selection.numberedDescription() + \
              "Enter a number (or 'quit'): ")

def leaveSenarios(player, activations):
    def performLeave(peer, line):
        line = line.lower().strip()
        if line == 'yes':
            for a in activations:
                a.deactivate(reason = 'You have left the %s senario.' % a.senario.name)

        elif line not in ['n', 'no']:
            return True # re-prompt

    PromptFor(player.peer, performLeave, write_mode = True,
              message = PROMPT_YESNO)

def activateForPlayer(senario, player):
    # This routine is kind of pointless: it's a nice alert, but
    # by no means asserts that state is alright, unless activate
    # did in fact clean up before re-raising its error.
    try: senario.activate(player)
    except:
        traceback()
        peer = player.peer
        if peer is not None:
            print('There was an error with the quest:', file=peer)
            HandleCommandError(peer, full_traceback = False)

def redeemReward(player, kitty):
    # bank?
    # messages?
    player.gold_on_hand += kitty.gold
    for item in kitty.items:
        if type(item) is int:
            ItemPrototype(item).instantiate(player)
        elif isinstance(item, ItemPrototype):
            item.location = player

    player.qpoints += kitty.points.get('quest', 0)
    # assert player.qpoints >= 0

# Special Procedures.
def parseArgstr(argstr):
    args = argstr.split() if argstr is not None else ()
    return (args[0].lower(),) + tuple(args[1:]) if args else args

possessive_pronoun = {'Male'   : 'his',
                      'Female' : 'her',
                      'Neutral': 'its'}
informal_pronoun = {'Male'    : 'lad',
                    'Female'  : 'lass',
                    'Neutral' : 'friend'}

def questingClosed(player, me):
    me.sayTo(player, 'Questing services are currently closed.')
    # todo: replace this with a proper act()
    me('emote folds %s arms.' % possessive_pronoun[me.sex])

CHECK_OUT_SYNTAX = "Type 'check out all|<number>' or 'list rewards' to claim your prize."

def getCommFromToString(comm, targetWord):
    return comm.lstrip()[len(targetWord):]

CONVERSATION_DELAY = 2

def QuestMaster(player, me, cmd, argstr):
    args = parseArgstr(argstr)
    if cmd.reserved:
        # Do periodic behavior to give us personality, and hint as tutorial.
        if chance(10):
            qc = QuestControl.get()
            if qc is not None:
                for action in qc.getRandomActionGroup():
                    me(action)

    if cmd.name in ('to', '>'):
        if args and player.find(args[0]) is me:
            qc = QuestControl.get()
            if qc is not None:
                for response in qc.getResponseAction(getCommFromToString(argstr, args[0])):
                    invokeTimeoutForHeartbeat(CONVERSATION_DELAY, me.sayTo, player, response)

        return False

    if cmd.name == 'help':
        qc = QuestControl.get()
        if qc is None:
            questingClosed(player, me)
        else:
            peer = player.peer
            if peer is not None:
                text = qc.getHelpText(args)
                if text is not None:
                    peer.page_string(text)
                    return True

    if cmd.name == 'join':
        qc = QuestControl.get()
        if qc is None:
            questingClosed(player, me)
        else:
            if qc.getActivationsFor(player):
                me.tell('You may only join one quest at a time (currently)', player)
            else:
                named = ' '.join(args)
                if not named:
                    me.tell("Join what, me %s?  Type 'list' for the senarios." % \
                            informal_pronoun[player.sex], player)
                else:
                    senarios = qc.findSenariosElligibleFor(player)
                    found = list(senarios.selectByName(named))
                    if not found:
                        me.tell('There are no %r senarios.' % named, player)
                    elif len(found) > 1:
                        me.tell('These are %r senarios:' % named, player)
                        selectSenario(player, found)
                    else:
                        found = found[0]
                        me.tell('Are you sure you want to join %s?' % found.shortName(), player)
                        joinSenario(player, found)

        return True

    if cmd.name == 'leave':
        qc = QuestControl.get()
        if qc is None:
            questingClosed(player, me)
        else:
            named = ' '.join(args).lower()
            if not named:
                me.tell("Leave which senario?  Type 'list joined' for senarios you've joined.", player)
            else:
                actvtns = []
                for a in qc.getActivationsFor(player):
                    if a.senario.nameMatch(named):
                        actvtns.append(a)

                if not actvtns:
                    me.tell('Not joined %r senarios.' % named, player)
                else:
                    me.tell('Leave this senario?' if len(actvtns) == 1 else 'Leave all these senarios?', player)
                    leaveSenarios(player, actvtns)

            return True

    if cmd.name == 'list':
        qc = QuestControl.get()
        if qc is None:
            questingClosed(player, me)
        else:
            peer = player.peer
            if peer is not None:
                if args:
                    a = args[0].lower()
                    if a in ('joined', 'active'):
                        # Special case: actually, show activated senarios for player.
                        actvtns = qc.getActivationsFor(player)
                        if not actvtns:
                            me.tell('You are not currently participating in any quests.', player)
                            me.tell("Type 'list' to see available senarios.", player)
                        else:
                            peer.page_string('\r\n'.join(a.senario.shortDescription() for a in actvtns) + '\r\n')

                        return True

                    elif a == 'rewards':
                        rewards = qc.getRewardsFor(player)
                        if not rewards:
                            me.tell('You have no pending rewards.', player)
                        else:
                            me.tell("These are your pending rewards.  Type 'check <reward>' to claim.", player)
                            peer.page_string('\r\n'.join('%3d %s' % (nr, rewards[nr]) \
                                                         for nr in range(len(rewards))) + '\r\n')

                        return True

                    elif a == 'all':
                        senarios = qc.selectAllSenarios()
                    elif a.startswith('class:'):
                        senarios = qc.selectSenariosByClass(a[6:])
                    else:
                        senarios = qc.selectSenariosByName(a)

                else:
                    senarios = qc.findSenariosElligibleFor(player)

                if not senarios:
                    me.tell('There are no available senarios.', player)
                else:
                    me.tell('These are the available senarios:', player)
                    peer.page_string(senarios.shortDescription())

        return True

    if cmd.name == 'tell':
        if args[:2] != ('me', 'about'):
            return False

        qc = QuestControl.get()
        if qc is None:
            questingClosed(player, me)
        else:
            peer = player.peer
            if peer is not None:
                named = ' '.join(args[2:])
                if not named:
                    me.tell('Tell you about which senario?', player)
                else:
                    senarios = qc.findSenariosElligibleFor(player).selectByName(named)
                    if not senarios:
                        me.tell('There are no available %r senarios!' % named, player)
                    else:
                        me.tell('These are the available %r senarios:' % named, player)
                        peer.page_string(senarios.detailedDescription())

        return True

    if cmd.name == 'check':
        if len(args) > 1 and args[0].lower() == 'out':
            if len(args) != 2:
                me.tell(CHECK_OUT_SYNTAX, player)
            else:
                qc = QuestControl.get()
                if qc is None:
                    questingClosed(player, me)
                else:
                    rewards = qc.getRewardsFor(player)
                    which = args[1]

                    if which == 'all':
                        for r in rewards:
                            redeemReward(player, r)
                            qc.removeReward(player, r)

                    elif not which.isdigit():
                        me.tell(CHECK_OUT_SYNTAX, player)
                    else:
                        which = int(which)
                        try: r = rewards[which]
                        except IndexError:
                            me.tell("Unknown reward %r.  Type 'list rewards'.", player)
                        else:
                            redeemReward(player, r)
                            qc.removeReward(player, r)

            return True

    if cmd.name == 'reload' and args and args[0] == 'quest-control':
        if player.level >= Facility.Manager.IMPLEMENTOR:
            qc = QuestControl.get()
            if qc is not None and qc.activations:
                # todo: don't allow operation to succeed?
                if player.peer is not None:
                    print('&RThere (were) %d quest-senarios activated!&N' % len(qc.activations), file=player.peer)

            QuestControl.destroy()
            try: me.special = reloadThisModule().QuestMaster
            except:
                if player.peer is not None:
                    HandleCommandError(player.peer)
            else:
                me.sayTo(player, 'RELOADED: %s' % QuestControl.get(create = True))

            return True

# todo: overload 'quest' command:
#   Allows cancelling of quest (if allowed)
#   Allows seeing what quests we're involved with
