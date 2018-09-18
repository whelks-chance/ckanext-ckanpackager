import re
import os
import requests
import pylons
import logging
import ckan.model as model

from ckan.lib.cli import CkanCommand
from ckanext.ckanpackager.model.stat import Base as b1
from ckanext.ckanpackager.model.DownloadQueue import Base as b2
from ckanext.ckanpackager.model.QueueContent import Base as b3
from ckanext.ckanpackager.model.UserInfo import Base as b4

log = logging.getLogger()


class CKANPackagerCommand(CkanCommand):
    """
    Create stats from GBIF

    paster --plugin=ckanext-ckanpackager initdb -c /etc/ckan/default/development.ini

    """

    summary = __doc__.split('\n')[0]
    usage = __doc__

    def command(self):
        self._load_config()
        # Create the table if it doesn't exist
        self._create_tables()

    @staticmethod
    def _create_tables():
        b1.metadata.create_all(model.meta.engine)
        b2.metadata.create_all(model.meta.engine)
        b3.metadata.create_all(model.meta.engine)
        b4.metadata.create_all(model.meta.engine)
