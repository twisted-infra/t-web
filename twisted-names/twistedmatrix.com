
from twisted.names.authority import getSerial

name = 'twistedmatrix.com'

from hosts import pyramid, cube, wolfwood, xpdev, planet, nameservers, addSubdomains

subs = {
    pyramid: ['', 'projects.', 'smtp.', 'mail.', 'reality.', 'pyramid.', 'irc.', 'ftp.', 'radix.', 'saph.', 'java.', 'www.'],
    cube: ['cube.'],
    wolfwood: ['cvs.', 'wolfwood.', 'svn.'],
    xpdev: ['xpdev.'],
}

zone = [
    SOA(
        # For whom we are the authority
        name,

        # This nameserver's name
        mname = "ns1.twistedmatrix.com",

        # Mailbox of individual who handles this
        rname = "radix.twistedmatrix.com",

        # Unique serial identifying this SOA data
        # <4-year> <2-month> <2-day> <2-counter>
        serial = getSerial(),

        # Time interval before zone should be refreshed
        refresh = "1H",

        # Interval before failed refresh should be retried
        retry = "15M",

        # Upper limit on time interval before expiry
        expire = "1H",

        # Minimum TTL
        minimum = "1H",

        ttl='1H',
    ),

    MX(name, 5, 'mail.' + name, ttl='1H'),

    CNAME('planet.twistedmatrix.com', planet, ttl='1H'),
] + nameservers(name)

addSubdomains(name, zone, subs)
