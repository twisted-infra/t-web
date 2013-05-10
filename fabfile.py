"""
Support for wwww service installation and management.
"""

from fabric.api import run, settings, env, cd, put, abort, sudo
from fabric.contrib import files

from braid import authbind, bazaar, cron
from braid.twisted import service
from braid.debian import equivs
from braid.utils import tempfile

# TODO: Move these somewhere else and make them easily extendable
from braid import config

_hush_pyflakes = [config]


class TwistedWeb(service.Service):
    def task_install(self):
        """
        Install t-web, a Twisted Web based server.
        """
        # Bootstrap a new service environment
        self.bootstrap()

        # Add to www-data group. Mailman depends on this.
        sudo('/usr/sbin/usermod -a -G www-data {}'.format(self.serviceUser))

        # Setup authbind
        authbind.allow(self.serviceUser, 80)
        authbind.allow(self.serviceUser, 443)
        
        # Install httpd equiv, so apt doesn't try to install apache ever
        equivs.installEquiv(self.serviceName, 'httpd')

        with settings(user=self.serviceUser):
            run('ln -nsf {}/start {}/start'.format(self.configDir, self.binDir))
            self.task_update()
            cron.install(self.serviceUser, '{}/crontab'.format(self.configDir))

            run('mkdir -p ~/data')
            if env.get('installPrivateData'): 
                self.task_installSSLKeys() 
                run('touch {}/production'.format(self.configDir))
            else:
                run('rm -f {}/production'.format(self.configDir))


    def task_installSSLKeys(self, key=None, cert=None):
        """
        Install SSL keys.

        @param key: Local path to key
        @param cert: Local path to cert
        """

        with settings(user=self.serviceUser):
            run('mkdir -p ~/ssl')
            if key is not None:
                put(key, '~/ssl/twistedmatrix.com.key', mode=600)
            elif not files.exist('~/ssl/twistedmatrix.com.key'):
                abort('Missing SSL key.')
            if cert is not None:
                put(cert, '~/ssl/twistedmatrix.com.crt')
            elif not files.exist('~/ssl/twistedmatrix.com.crt'):
                abort('Missing SSL certificate.')


    def task_update(self):
        """
        Update config.
        """
        with settings(user=self.serviceUser):
            # TODO: This is a temp location for testing
            bazaar.branch('lp:~tom.prince/twisted-website/twisted-website-braided', self.configDir)
            # TODO restart


    def task_dump(self, dump):
        """
        Dump non-versioned resources.
        """
        with settings(user=self.serviceUser), \
             tempfile(saveTo=dump) as tar, \
             cd('~/data'):
            run('/usr/bin/tar -c -j -f {} .'.format(tar))


    def task_restore(self, dump):
        """
        Resotre non-versioned resources.
        """
        with settings(user=self.serviceUser), \
             tempfile(saveTo=dump) as tar, \
             cd('~/data'):
            run('/usr/bin/tar -x -j -f {} .'.format(tar))



globals().update(TwistedWeb('t-web').getTasks())
