# Tool for enabling breakpoints on django/urlconf views.
from django.core.urlresolvers import get_resolver, get_urlconf, RegexURLResolver, RegexURLPattern

def findUrlPattern(path, resolver = None):
    if resolver is None:
        resolver = get_resolver(get_urlconf())

    match = resolver.regex.search(path)
    if match:
        if isinstance(resolver, RegexURLPattern):
            return resolver

        assert isinstance(resolver, RegexURLResolver)
        path = path[match.end():]
        for pattern in resolver.url_patterns:
            result = findUrlPattern(path, pattern)
            if result is not None:
                return result

_url_breakpoints = []

def doBreakOnUrl(peer, action = None, url = None):
    if action in ('show', None):
        peer.page_string('\r\n'.join(map(str, _url_breakpoints)) + '\r\n')
    else:
        # Enable breakpoint on django urlconf callback.
        pattern = findUrlPattern(url)
        if not pattern:
            print('Url not found: %r' % url, file=peer)

        elif action == 'enable':
            if enableUrlBreakpoint(pattern):
                print('Breaking on: %r' % pattern, file=peer)

        elif action == 'disable':
            if disableUrlBreakpoint(pattern):
                print('No longer breaking on: %r' % pattern, file=peer)

def enableUrlBreakpoint(pattern):
    if not hasattr(pattern, '__unbroken_callback'):
        unbroken = pattern._callback
        pattern._callback = breakOn(unbroken)
        setattr(pattern, '__unbroken_callback', unbroken)

        _url_breakpoints.append(pattern)
        return True

def disableUrlBreakpoint(pattern):
    try: unbroken = getattr(pattern, '__unbroken_callback')
    except AttributeError: pass
    else:
        pattern._callback = unbroken
        delattr(pattern, '__unbroken_callback')

        _url_breakpoints.remove(pattern)
        return True
