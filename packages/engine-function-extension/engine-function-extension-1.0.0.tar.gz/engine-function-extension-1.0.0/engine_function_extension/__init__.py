
import django

from django.conf import settings
from python_hosts import Hosts, HostsEntry
from azure.functions import AppExtensionBase

HOSTS = """
10.1.0.4 live-mongo1.openlearning.local live-mongo1
10.1.0.5 live-mongo2.openlearning.local live-mongo2
10.1.0.6 live-mongo3.openlearning.local live-mongo3
10.2.0.4 staging-rem1.openlearning.local staging-rem1
10.1.0.7 live-cache1.openlearning.local live-cache1
10.1.0.8 live-cache2.openlearning.local live-cache2
10.1.0.9 live-cache3.openlearning.local live-cache3
10.1.0.26 live-cache4.openlearning.local live-cache4
10.1.0.35 live-cache5.openlearning.local live-cache5
10.1.0.37 live-cache6.openlearning.local live-cache6
10.1.0.17 live-es-importers.openlearning.local live-es-importers
10.1.0.14 live-rabbit1.openlearning.local live-rabbit1
10.1.0.18 live-rabbit2.openlearning.local live-rabbit2
10.1.0.10 live-rem1.openlearning.local live-rem1
10.3.0.4 qa-mongo1.openlearning.local qa-mongo1
10.3.0.5 qa-rem1.openlearning.local qa-rem1
10.3.0.6 qa2-rem1.openlearning.local qa2-rem1
10.2.0.8 staging-mongo2.openlearning.local staging-mongo2
10.1.0.63 live-weblog.openlearning.local live-weblog
10.1.0.60 live-notification-mongo1.openlearning.local live-notification-mongo1
10.1.0.31 live-notification-mongo2.openlearning.local live-notification-mongo2
10.1.0.33 live-notification-mongo-backup.openlearning.local live-notification-mongo-backup
10.4.0.4 us-mongo1.openlearning.local us-mongo1
10.4.0.5 us-mongo2.openlearning.local us-mongo2
10.4.0.6 us-mongo3.openlearning.local us-mongo3
10.4.0.15 us-rabbit1.openlearning.local us-rabbit1
10.4.0.13 us-rabbit2.openlearning.local us-rabbit2
10.5.0.4 us-staging-mongo1.openlearning.local us-staging-mongo1
10.5.0.5 us-staging-rem1.openlearning.local us-staging-rem1
10.4.0.14 us-cache1.openlearning.local us-cache1
10.4.0.12 us-es-importers.openlearning.local us-es-importers
"""

class AppExtension(AppExtensionBase):
    """A Python worker extension to setup Engine env
    """

    @classmethod
    def init(cls):
        # This records the starttime of each function
        # setup key vault env file
        # setup django
        django.setup()

        if settings.ENV != 'dev':
            hosts_entries = Hosts(path='/etc/hosts')
            hostnames = HOSTS.strip('\n').split('\n')

            for hostname_line in hostnames:
                hostname_line = hostname_line.strip('\n')
                ip_add, _, hostname = hostname_line.split()

                hosts_entries.remove_all_matching(address=ip_add, name=hostname)
                entry = HostsEntry.str_to_hostentry(hostname_line)
                hosts_entries.add(entries=[entry])

            hosts_entries.write()
