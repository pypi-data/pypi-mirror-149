# Heartbeat Profiling.
from .wizard import parameters
from os.path import basename

# My implementation of profile and stats.
##    class Profile:
##        from time import time as timer
##        timer = staticmethod(timer)
##
##        def __init__(self):
##            self.stats = {}
##
##        def runcall(self, function, *args, **kwd):
##            start = self.timer()
##            try: return function(*args, **kwd)
##            finally:
##                self.stats.setdefault(function, []).append(self.timer() - start)
##
##    class Stats:
##        def __init__(self, other, stream = None):
##            if stream is None:
##                from sys import stdout as stream
##
##            self.stats = {}
##            self.stream = stream
##            self.add(other)
##
##        def add(self, other):
##            for (function, durations) in other.stats.iteritems():
##                self.stats.setdefault(function, []).extend(durations)
##
##        def text_stats(self):
##            yield 'NR    TOTAL       AVG         MAX         MIN         FILENAME:FUNCTION'
##            for (function, durations) in self.stats.iteritems():
##                co = function.func_code
##                nr = len(durations)
##                total = sum(durations)
##                total = float(total)
##                avg = total / nr
##                maxt = max(durations)
##                mint = min(durations)
##
##                yield '%-4d  %-10.10s  %-10.10s  %-10.10s  %-10.10s  %s:%s' % \
##                      (nr, '%4.6f' % total, '%4.6f' % avg,
##                       '%4.6f' % max(durations), '%4.6f' % min(durations),
##                       basename(co.co_filename), co.co_name)
##
##        def print_stats(self):
##            try: page = self.stream.page_string
##            except AttributeError:
##                for line in self.text_stats():
##                    print >> self.stream, line
##            else:
##                page('\r\n'.join(self.text_stats()) + '\r\n')

# Standard Profiling Implementation.
from profile import Profile
from pstats import Stats as stdStats

class Stats:
    # HACK: Wraps standard stats to make it comply with pstats.add_callers algorithm.
    def __init__(self, other, stream = None):
        if stream is None:
            from sys import stdout as stream

        self.stdStats = stdStats(self.EmptyStatsHolder(),
                                 stream = stream)

    class EmptyStatsHolder:
        # XXX pstats.Stats.load_stats does not allow empty stats.
        class SeeminglyNonEmptyStats(dict):
            def __bool__(self):
                return True

        stats = SeeminglyNonEmptyStats()
        def create_stats(self):
            pass

    class NonEmptyStatsHolder:
        def __init__(self, stats):
            self.stats = stats
        def create_stats(self):
            pass

    class Transform:
        def __init__(self, other):
            other.create_stats()
            self.stats = other.stats
        def create_stats(self):
            # Transform for add_callers algorithm.
            stats = self.stats
            self.stats = {}

            for (func, (cc, nc, tt, ct, callers)) in stats.items():
                # Transform callers to something add_callers can accept.
                for key in list(callers.keys()):
                    # Basically -- this scalar value is expected to be a singleton.
                    callers[key] = [callers[key]]

                # Fold it back into the stats.
                self.stats[func] = (cc, nc, tt, ct, callers)

    def add(self, other):
        self.stdStats.add(self.Transform(other))

    # Standard Stats Interface Wrapper
    @property
    def stats(self):
        return self.stdStats.stats

    def print_stats(self, *args, **kwd):
        return self.stdStats.print_stats(*args, **kwd)

    def print_callers(self, *args, **kwd):
        # Minor surgery: (XXX)
        os = self.stdStats.stats
        self.stdStats.stats = self.Transform(self.NonEmptyStatsHolder(self.stdStats.stats)).stats

        try: return self.stdStats.print_callers(*args, **kwd)
        finally:
            self.stdStats.stats = os

    def print_callees(self, *args, **kwd):
        return self.stdStats.print_callees(*args, **kwd)
    def strip_dirs(self, *args, **kwd):
        return self.stdStats.strip_dirs(*args, **kwd)
    def sort_stats(self, *args, **kwd):
        return self.stdStats.sort_stats(*args, **kwd)

# The profiling routine.
_stats_collection = Stats(Profile())

def doHeartbeatPulseWithProfiling(heartbeat, *args, **kwd):
    profiler = Profile()
    try: return profiler.runcall(heartbeat, *args, **kwd)
    finally: _stats_collection.add(profiler)

    ##    if _profile_stats_stream is None:
    ##        return heartbeat.pulse(*args, **kwd)
    ##
    ##    profiler = Profile()
    ##    try: return profiler.runcall(heartbeat.pulse, *args, **kwd)
    ##    finally:
    ##        # Extract stats, stream to file (in binary form).
    ##        profiler.create_stats()
    ##        import marshal
    ##        marhsal.dump(profiler.stats, _profile_stats_stream)
    ##        _profile_stats_stream.flush()

from io import StringIO as StringBuffer
class StatsTransferForShow:
    def __init__(self, stats):
        self.stats = stats.stats
    def create_stats(self):
        pass

    class StreamPager(StringBuffer):
        def page(self, peer):
            peer.page_string(self.getvalue())

    @classmethod
    def ShowStats(self, peer, order = None):
        stream = self.StreamPager()
        stats = Stats(self(_stats_collection),
                      stream = stream)

        stats.strip_dirs()
        if order in ['calls', 'cumulative', 'file', 'line', 'module',
                     'name', 'nfl', 'pcalls', 'stdname', 'time']:
            stats.sort_stats(order)

        stats.print_stats()
        stream.page(peer)

    @classmethod
    def ShowCallers(self, peer):
        stream = self.StreamPager()
        stats = Stats(self(_stats_collection),
                      stream = stream)

        stats.strip_dirs()
        stats.print_callers()
        stream.page(peer)

    @classmethod
    def ShowCallees(self, peer):
        stream = self.StreamPager()
        stats = Stats(self(_stats_collection),
                      stream = stream)

        stats.strip_dirs()
        stats.print_callees()
        stream.page(peer)

# Management.
class HeartbeatProfiler:
    Instance = None

    class NotAvailable(RuntimeError):
        pass

    @classmethod
    def IsEnabled(self, heartbeat):
        return self.Instance is not None

    @classmethod
    def Enable(self, heartbeat):
        if self.IsEnabled(heartbeat):
            raise self.NotAvailable

        HeartbeatProfiler.Instance = self(heartbeat)

    @classmethod
    def Disable(self, heartbeat):
        if not self.IsEnabled(heartbeat):
            raise self.NotAvailable

        self.Instance.disable()
        self.Instance = None

    @classmethod
    def ShowStats(self, *args, **kwd):
        StatsTransferForShow.ShowStats(*args, **kwd)

    @classmethod
    def ShowCallers(self, *args, **kwd):
        StatsTransferForShow.ShowCallers(*args, **kwd)

    @classmethod
    def ShowCallees(self, *args, **kwd):
        StatsTransferForShow.ShowCallees(*args, **kwd)

    # Manage instance.
    def __init__(self, heartbeat):
        self.heartbeat = heartbeat
        self.enable()

    # Fail on multithreading core.
    def disable(self):
        self.heartbeat.pulse = self.previous_pulse
    def enable(self):
        self.previous_pulse = self.heartbeat.pulse
        self.heartbeat.pulse = self

    def __call__(self, *args, **kwd):
        return doHeartbeatPulseWithProfiling(self.previous_pulse, *args, **kwd)

def getHeartbeatObject():
    from world import heartbeat
    return heartbeat

@parameters(1, None)
def doProfileHeartbeat(peer, command, arg = None):
    if command == 'on':
        try: HeartbeatProfiler.Enable(getHeartbeatObject())
        except HeartbeatProfiler.NotAvailable:
            print('Already profiling.', file=peer)
        else:
            print('Heartbeat profiling enabled.', file=peer)

    elif command == 'off':
        try: HeartbeatProfiler.Disable(getHeartbeatObject())
        except HeartbeatProfiler.NotAvailable:
            print('Already disabled.', file=peer)
        else:
            print('Heartbeat profiling disabled.', file=peer)

    elif command in ('show', 'stats'):
        try:
            if arg == 'callers':
                HeartbeatProfiler.ShowCallers(peer)
            elif arg == 'callees':
                HeartbeatProfiler.ShowCallees(peer)
            else:
                HeartbeatProfiler.ShowStats(peer, arg)

        except HeartbeatProfiler.NotAvailable:
            print('Heartbeat profiling not enabled.', file=peer)

    elif command in ('load', 'dump'):
        print('Not yet implemented.', file=peer)

# Startup.
from ph import getConfig
if getConfig('heartbeat-profiling') == 'on':
    try: HeartbeatProfiler.Enable(getHeartbeatObject())
    except HeartbeatProfiler.NotAvailable:
        pass
