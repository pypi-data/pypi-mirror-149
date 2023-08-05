'Implements the events invoked from Crash_ in objsave.'

def deleteRentFile(name, info, filename):
    world.corelog('(DeletingRent:%s:%s)' % (name, filename))
    # showRentInfo(info)

from new import instancemethod as bind

class RentManagement:
    msgfmt = '(PC) %(Name)s %(Code)s%(Action)s from %(Filename)r at [%(Timestamp)s]'

    def loadNotifiers(self, a):
        'Load the rent handlers.'
        def logAction(action, player, info, filename):
            info = self.unpackRentInfo(info)
            info = {'Name':player.name, 'Code':info[0], 'Action':action,
                    'Timestamp':info[1], 'Filename':filename}

            world.corelog(self.msgfmt % info)

        a.rentStart       = lambda *args:logAction('SaveStart',    *args)
        a.rentComplete    = lambda *args:logAction('SaveComplete', *args)
        a.unrentStart     = lambda *args:logAction('LoadStart',    *args)
        a.unrentComplete  = lambda *args:logAction('LoadComplete', *args)

    __init__ = loadNotifiers

    from struct import unpack
    unpack = staticmethod(unpack)

    # time, code, perdiem, gold, acct, nitems, <8 spares>
    structfmt_rent_info = '14i'
    rent_info_member_names = ('time', 'code', 'perdiem', 'gold', 'acct', 'nitems')

    rent_codes = { 1: 'Crash', 2: 'Rented', 4: 'Forced', 5: 'Timed-Out' }

    from time import ctime
    ctime = staticmethod(ctime)

    def unpackRentInfo(self, info):
        'Unpack the rent_info buffer and parse rent-code, time.'
        data = self.unpack(self.structfmt_rent_info, str(info))

        # 2-tuple
        return (self.rent_codes.get(data[1]) or ('#%d ' % data[1]), self.ctime(data[0]))

        # [for (x, n) in zip(data[:6], self.rent_info_member_names)]

