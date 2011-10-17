
from twisted.names.dns import Record_NS, Record_A

pyramid = '198.49.126.190'
neutrino = '198.49.126.149'
wolfwood = '198.49.126.131'
planet = 'mag.ik.nu'
xpdev = '66.219.41.216'
cube = '66.35.39.65'
tesla = '198.49.126.204'
tmrc = '18.150.1.81'
tesla = '198.49.126.204'
intarweb = '198.49.126.149'
cube = '66.35.39.65'
pyramid = '198.49.126.190'
boson = '216.15.126.201'

def nameservers(host):
    """
    Return NS records and A record glue for the given host.
    """
    return [
        (host, Record_NS('ns1.twistedmatrix.com', ttl='1H')),
        (host, Record_NS('ns2.twistedmatrix.com', ttl='1H')),
        ('ns1.twistedmatrix.com', Record_A(cube, ttl='1H')),
        ('ns2.twistedmatrix.com', Record_A(tmrc, ttl='1H'))]


def addSubdomains(host, zone, subs):
    """
    Add the given subdomain mapping to the given zone list.
    """
    for (ip, hosts) in subs.items():
        for sub in hosts:
            zone.append((sub + host, Record_A(ip, ttl="1H")))
