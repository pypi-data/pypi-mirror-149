# Auto-Slay Senario
# Copyright 2010 Clint Banis.  All rights reserved.
#
from . import Senario, QuestControl, Kitty
from . import MobilePrototype, ItemPrototype, RealRoom
from . import dumpYamlWithIndent

class AutoSlay(Senario):
    def __str__(self):
        def description():
            yield 'Name: %s' % getattr(self, 'name', '--')
            for (name, attribute) in [('Class'       , 'class'       ),
                                      ('Type'        , 'quest-type'  ),
                                      ('Field'       , 'field'       ),
                                      ('Min-Level'   , 'min-level'   ),
                                      ('Max-Level'   , 'max-level'   ),
                                      ('Remort-Level', 'remort-level'),
                                      ('Time-Limit'  , 'time-limit'  ),
                                      ('Availability', 'frequency'   ),
                                      ('Cost'        , 'cost'        ),
                                      ('Requirements', 'requirements'),
                                      ('Rewards'     , 'reward'      )]:

                yield '  %s: %s' % (name, self.get(attribute, '--'))

            try: opponents = self.opponents
            except AttributeError: pass
            else:
                yield '  Opponents:'
                for opp in opponents:
                    yield '    %s' % dumpYamlWithIndent(opp, indent = 4)

            try: rewards = self.rewards
            except AttributeError: pass
            else:
                if isinstance(rewards, str):
                    yield '  Rewards: %s' % rewards
                else:
                    yield '  Rewards:'
                    for r in rewards:
                        yield '    %s' % dumpYamlWithIndent(r, indent = 4)

        return '\r\n'.join(description()) + '\r\n'

    class Activation(Senario.Activation):
        def validate(self):
            Senario.Activation.validate(self)
            self.slayed = []

        # World Events.
        def onSlayMobile(self, victim, killer):
            if victim in self.opponents:
                # What if the killer isn't part of this quest?? (still need to clean up)
                if killer is self.player:
                    self.slayed.append(victim)

                    # Todo: per-opponent slay messages!
                    msg = self.senario.get('slay-message')
                    if msg is not None:
                        peer = self.player.peer
                        if peer is not None:
                            print(msg, file=peer)

                self.opponents.remove(victim)
                self.checkProgress()

        def onDealDamage(self, attacker, victim, dam, wtype):
            # Basically: only allow those involved in the quest to do any damage.
            if victim in self.opponents:
                if attacker is not self.player:
                    # Just regain the damage!
                    victim.hit += dam

        def onPurgeMobile(self, victim, wizard):
            if victim in self.opponents:
                self.opponents.remove(victim)
                self.checkProgress()

        def onDeathTrap(self, victim, cause):
            if victim in self.opponents:
                self.opponents.remove(victim)
                self.checkProgress()

        # House-keeping.
        def deactivate(self, *args, **kwd):
            # Clean up remaining opponents.  Shut down arena.  Burn the remains.
            for opp in self.opponents:
                try: opp.valid
                except ValueError:
                    # Already dead and gone.
                    continue

                # todo: allow corpse-ated rewards.
                opp.act('$n suddenly lights with an inner heat, and then crumbles to dust.')
                eq = opp.equipment
                for o in eq:
                    o = eq[o]
                    if o is not None:
                        o.extract()

                for o in opp.inventory:
                    o.extract()

                # cleanup props
                opp.extract()

            super(self.__class__, self).deactivate(*args, **kwd)

        def checkProgress(self):
            if not self.opponents:
                # Slay senario is done: calculate rewards.
                kitty = self.getKitty()

                qc = QuestControl.get()
                if qc is None:
                    # Fail: dump kitty to disk.
                    pass
                else:
                    # Post kitty to control facility for later redeeming.
                    qc.postReward(self.player, kitty)

                # todo: log victory/defeat
                # todo: announce victory/defeat on the quest channel

                self.deactivate(reason = self.senario.get('end-message', self.senario.DEFAULT_END_MESSAGE))

        def getKitty(self):
            kitty = Kitty()
            for mob in self.slayed:
                opp = self.marks.get(mob)
                if opp is not None:
                    self.addReward(kitty, opp.get('reward'))

            self.addReward(kitty, self.senario.get('reward'))
            return kitty

        def addReward(self, kitty, reward):
            if isinstance(reward, (list, tuple)):
                for reward in reward:
                    if isinstance(reward, dict):
                        for (name, value) in reward.items():
                            if name == 'gold':
                                kitty.addGold(self.pointValue(value))
                            else:
                                point_type = {'qpoints': 'quest',
                                              'quest-points': 'quest',
                                              'silver-points': 'silver',
                                              'gold-points': 'gold',
                                              'platinum-points': 'platinum',
                                              'merit-points': 'merit'}.get(name)
                                if point_type:
                                    kitty.addPoints(point_type, self.pointValue(value))

        def pointValue(self, value):
            if type(value) is int:
                return value

            return evaluate(value, player = self.player) # XXX should this be imported?

        def percentComplete(self):
            return (float(len(self.slayed)) / len(self.opponents)) * 100

    def activate(self, player):
        field = self.get('field', 'world')

        opponents = []
        marks = {}
        for opp in self.get('opponents', []):
            proto = MobilePrototype(opp.get('mark-vnum'))
            for x in range(opp.get('count', 1)):
                mob = self.makeOpponent(player, opp, proto, field)
                marks[mob] = opp
                opponents.append(mob)

        super(self.__class__, self).activate(player, opponents = opponents,
                                             marks = marks)

    VALID_NPCFLAGS = set(['sentinel'])
    VALID_AFFECTFLAGS = set()
    DATA_OVERRIDES = ['level', ('hit-points', 'max_hit'), 'alignment',
                      'experience', 'hitroll', 'damroll', ('armorclass', 'ac'),
                      ('gold', 'gold_on_hand')]

    MAX_LEVEL = 105
    MAX_EXPERIENCE = 10 * 1000 * 1000

    def setFlags(self, bitv, valid, value):
        if isinstance(value, str):
            for f in value.split():
                f = f.lower()

                value = True
                if f[0] == '-':
                    f = f[1:]
                    value = False

                if f in valid:
                    setattr(bitv, f, value)

    def makeOpponent(self, player, opp, proto, field):
        mob = None

        # Select Field.
        if field == 'world':
            for mob in proto:
                break # selecting first.
            else:
                raise RuntimeError('Not in world: %s' % proto)

        elif field == 'roaming':
            mob = proto.instantiate(RealRoom(opp.get('load-room')))
        elif isinstance(field, list):
            try: arena = field[0]['arena']
            except (KeyError, IndexError):
                raise ValueError('Unknown field: %r' % field)

            if arena:
                # arena: load room for mobs, creates self-closing portal.
                # (or just transports).. random arena in arena-group..
                raise NotImplementedError('Arena: %r' % arena)

        assert mob is not None
        npcflags = mob.npcflags

        npcflags.NoCorpse = True # generally desireable
        npcflags.Quest = True

        self.setFlags(npcflags, self.VALID_NPCFLAGS, opp.get('flags'))
        self.setFlags(mob.affectflags, self.VALID_AFFECTFLAGS, opp.get('affect-flags'))

        # Data overrides.
        for name in self.DATA_OVERRIDES:
            if isinstance(name, (tuple, list)) and len(name) == 2:
                (name, attribute) = name
            else:
                attribute = name

            value = opp.get(name)
            if type(value) is int:
                setattr(mob, attribute, value)
            elif value is not None:
                setattr(mob, attribute, evaluate(value, player = player, opponent = mob)) # XXX should this be imported?

        # Note of arrival and equip.
        for msg in opp.get('arrival-messages', []):
            mob.act(msg, object = mob)

        for group in opp.get('equipment', []):
            for (wear_pos, vnum) in group.items():
                item = ItemPrototype(vnum).instantiate(mob)
                mob.equip(item, wear_pos)

        for vnum in opp.get('inventory', []):
            ItemPrototype(vnum).instantiate(mob)

        # todo: make follower chain (using yaml reference syntax, or naming)

        # Normalize:
        mob.level = min(self.MAX_LEVEL, max(0, mob.level))
        mob.hit = mob.max_hit
        mob.experience = min(self.MAX_EXPERIENCE, min(0, mob.experience))
        mob.hitroll = max(0, mob.hitroll)
        mob.damroll = max(0, mob.damroll)

        return mob
