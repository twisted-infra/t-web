"""
Support for DNS service installation and management.
"""

from fabric.api import run, settings, env

from braid import authbind, bazaar, cron
from braid.twisted import service
from braid.debian import equivs

# TODO: Move these somewhere else and make them easily extendable
from braid import config

_hush_pyflakes = [config]


class TwistedWeb(service.Service):
    def task_install(self):
        """
        Install t-names, a Twisted Names based DNS server.
        """
        # Bootstrap a new service environment
        self.bootstrap()

        # Setup authbind
        authbind.allow(self.serviceUser, 80)
        authbind.allow(self.serviceUser, 443)
        
        # Install httpd equiv, so apt doesn't try to install apache ever
        equivs.installEquiv(self.serviceName, 'httpd')

        with settings(user=self.serviceUser):
            run('ln -nsf {}/start {}/start'.format(self.configDir, self.binDir))
            self.task_update()
            cron.install(self.serviceUser, '{}/crontab'.format(self.configDir))
            
            if env.get('environment') == 'production':
                run('touch {}/production'.format(self.configDir))
            else:
                run('rm -f {}/production'.format(self.configDir))

    def task_update(self):
        """
        Update config.
        """
        with settings(user=self.serviceUser):
            # TODO: This is a temp location for testing
            bazaar.branch('lp:~tom.prince/twisted-website/twisted-website-braided', self.configDir)
            # TODO restart


globals().update(TwistedWeb('t-web').getTasks())
