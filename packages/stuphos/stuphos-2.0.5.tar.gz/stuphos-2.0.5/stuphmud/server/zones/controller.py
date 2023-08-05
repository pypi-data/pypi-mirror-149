# This should go in circlemud.world.

'''
[Services]
facility.zone-reset = stuphmud.server.zones.controller.ZoneReset

'''

from stuphos.runtime.facilities import Facility
from stuphos.runtime.architecture import newComponent

class ZoneReset(Facility):
    NAME = 'StuphMUD::Zone::Controller'

    @classmethod
    def create(self):
        return newComponent(self)

    # Enable this as a --reset-world alternative.
    # def onResetComplete(self, ctlr):
    #     self.resetWorld(core)

    def resetWorld(self, world, forceAll = False, bridgeApi = True):
        def zreset(zone):
            return self.resetZone(world, zone, force = forceAll,
                                  bridgeApi = bridgeApi)

        from world import zone, iterent
        iterent(zone, callback = zreset,
                map_results = False)

    def shouldReset(self, zone):
        pass

    def resetZone(self, world, zone, force = False, bridgeApi = True):
        if force or self.shouldReset(zone):
            # debugOn()
            if bridgeApi:
                print(f'[resetZone] {StuphMUD.StartZoneReset}')
                StuphMUD.StartZoneReset(zone)

            state = (False, None) # last command, last object
            for (nr, cmd) in enumerate(zone.zcommands):
                if cmd.isConditional and not state[0]:
                    continue

                code = cmd.commandCode
                try:
                    if code == 'M':
                        state = self.loadMobile(world, zone, state, nr, cmd)
                    elif code == 'O':
                        state = self.loadObject(world, zone, state, nr, cmd)
                    elif code == 'E':
                        state = self.equipMobile(world, zone, state, nr, cmd)
                    elif code == 'P':
                        state = self.putObject(world, zone, state, nr, cmd)
                    elif code == 'D':
                        state = self.doorState(world, zone, state, nr, cmd)
                    elif code == 'R':
                        state = self.removeObject(world, zone, state, nr, cmd)
                    elif code == 'G':
                        state = self.giveObject(world, zone, state, nr, cmd)

                except Exception as e:
                    print(f'[Reset Zone #{zone.vnum}:{nr} ({code})] {e.__class__.__name__}: {e}')
                    state = (False, None)

            if bridgeApi:
                StuphMUD.CompleteZoneReset(zone)


    # Zone commands.
    # class command:
    #     arg1 = arg2 = arg3 = None
    #     command = commandName = '?'
    #     commandCode = type = '*'
    #     owner = location = container = None
    #     door = doorState = None
    #     mobile = object = room = None

    #     max = maxExisting = 0
    #     line = ''

    #     isConditional = False

    def loadMobile(self, core, zone, state, nr, cmd):
        if core and core.cmdln['options'].verbose > 1:
            print(f'[Zone Reset {zone.name} #{nr}] Load Mobile #{cmd.arg1} in room #{cmd.arg3}, {cmd.arg2} max')

        from world import mobile, mobile_instance, room
        vnum = int(cmd.arg1)

        # debugOn()
        if len(mobile_instance.instances.get(vnum, [])) < int(cmd.arg2):
            proto = mobile.lookup(vnum)
            room = room.lookup(int(cmd.arg3))

            mob = proto.instantiate(room)

            return (True, mob)

        return (False, None)

    def loadObject(self, world, zone, state, nr, cmd):
     #    case 'O':         /* read an object */
     #      if (obj_index[ZCMD.arg1].number < ZCMD.arg2) {
        # if (ZCMD.arg3 != NOWHERE) {
        #   obj = read_object(ZCMD.arg1, REAL);
        #   obj_to_room(obj, ZCMD.arg3);
        #   last_cmd = 1;

     #    // zone load item

        # } else {
        #   obj = read_object(ZCMD.arg1, REAL);
        #   IN_ROOM(obj) = NOWHERE;
        #   last_cmd = 1;

     #    // zone load item

        # }
     #      } else
        # last_cmd = 0;
     #      break;
        return (False, None)

    def equipMobile(self, world, zone, state, nr, cmd):
     #    case 'E':         /* object to equipment list */
     #      if (!mob) {
        # ZONE_ERROR("trying to equip non-existant mob, command disabled");
        # ZCMD.command = '*';
        # break;
     #      }
     #      if (obj_index[ZCMD.arg1].number < ZCMD.arg2) {
        # if (ZCMD.arg3 < 0 || ZCMD.arg3 >= NUM_WEARS) {
        #   ZONE_ERROR("invalid equipment pos number");
        # } else {
        #   obj = read_object(ZCMD.arg1, REAL);
        #   equip_char(mob, obj, ZCMD.arg3);
        #   last_cmd = 1;

     #    // zone load item

        # }
     #      } else
        # last_cmd = 0;
     #      break;
        return (False, None)

    def putObject(self, world, zone, state, nr, cmd):
     #    case 'P':         /* object to object */
     #      if (obj_index[ZCMD.arg1].number < ZCMD.arg2) {
        # obj = read_object(ZCMD.arg1, REAL);
        # if (!(obj_to = get_obj_num(ZCMD.arg3))) {
        #   ZONE_ERROR("target obj not found, command disabled");
        #   ZCMD.command = '*';
        #   break;
        # }
        # obj_to_obj(obj, obj_to);
        # last_cmd = 1;

     #  // zone load item

     #      } else
        # last_cmd = 0;
     #      break;
        return (False, None)

    def doorState(self, world, zone, state, nr, cmd):
     #    case 'D':         /* set state of door */
     #      if (ZCMD.arg2 < 0 || ZCMD.arg2 >= NUM_OF_DIRS ||
        #   (world[ZCMD.arg1].dir_option[ZCMD.arg2] == NULL)) {
        # ZONE_ERROR("door does not exist, command disabled");
        # ZCMD.command = '*';
     #      } else
        # switch (ZCMD.arg3) {
        # case 0:
        #   REMOVE_BIT(world[ZCMD.arg1].dir_option[ZCMD.arg2]->exit_info,
        #        EX_LOCKED);
        #   REMOVE_BIT(world[ZCMD.arg1].dir_option[ZCMD.arg2]->exit_info,
        #        EX_CLOSED);
        #   break;
        # case 1:
        #   SET_BIT(world[ZCMD.arg1].dir_option[ZCMD.arg2]->exit_info,
        #     EX_CLOSED);
        #   REMOVE_BIT(world[ZCMD.arg1].dir_option[ZCMD.arg2]->exit_info,
        #        EX_LOCKED);
        #   break;
        # case 2:
        #   SET_BIT(world[ZCMD.arg1].dir_option[ZCMD.arg2]->exit_info,
        #     EX_LOCKED);
        #   SET_BIT(world[ZCMD.arg1].dir_option[ZCMD.arg2]->exit_info,
        #     EX_CLOSED);
        #   break;
        # }
     #      last_cmd = 1;
        return (False, None)

    def removeObject(self, world, zone, state, nr, cmd):
        # case 'R': /* rem obj from room */
        #   if ((obj = get_obj_in_list_num(ZCMD.arg2, world[ZCMD.arg1].contents)) != NULL)
        #     extract_obj(obj);
        #   last_cmd = 1;
        #   break;
        return (False, None)

    def giveObject(self, world, zone, state, nr, cmd):
     #    case 'G':         /* obj_to_char */
     #      if (!mob) {
        # ZONE_ERROR("attempt to give obj to non-existant mob, command disabled");
        # ZCMD.command = '*';
        # break;
     #      }
     #      if (obj_index[ZCMD.arg1].number < ZCMD.arg2) {
        # obj = read_object(ZCMD.arg1, REAL);
        # obj_to_char(obj, mob);
        # last_cmd = 1;

     #  // zone load item

     #      } else
        # last_cmd = 0;
     #      break;
        return (False, None)
