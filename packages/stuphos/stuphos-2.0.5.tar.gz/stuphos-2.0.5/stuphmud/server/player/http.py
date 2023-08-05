# MUD Player HTTP Module.
HTTP_REDIRECT_MESSAGE = \
'''HTTP/1.0 302 Found
Location: %(location)s
Connection: close

No page content to render.
'''

HTTP_REDIRECT_VARS = dict(location = 'http://localhost/stuph/')
CON_CLOSE = 'Disconnecting'

def getHttpRedirectResponse():
    # date = 'Thu, 11 Feb 2010 18:18:44 GMT'
    vars = HTTP_REDIRECT_VARS.copy()

    # Ugh, this whole darn thing could come from config..
    from ph import getConfig
    url = getConfig('http-redirect-url') or ''
    url = url.strip()
    if url:
        vars['location'] = url

    response = HTTP_REDIRECT_MESSAGE % vars
    response = response.replace('\n', '\r\n')

    return response

def handleHttpRedirect(peer, xxx_todo_changeme):
    (method, resource, protocol) = xxx_todo_changeme
    from ph import log as mudlog
    mudlog('HTTP LOGIN REDIRECT [%s]: %r' % (protocol, resource))

    # Send redirect response.  Disconnect.
    peer.write(getHttpRedirectResponse())
    peer.state = CON_CLOSE

    return True

def detectHttpRequest(peer, line):
    if peer.state != 'Get name':
        return False

    try: (method, resource, protocol) = line.split()
    except ValueError:
        return False

    if method.upper() not in ['GET', 'POST', 'OPTIONS', 'HEAD']:
        return False
    if not protocol.upper().startswith('HTTP'):
        return False

    return handleHttpRedirect(peer, (method, resource, protocol))
