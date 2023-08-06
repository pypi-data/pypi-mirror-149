# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.dexterity.fti import DexterityFTI
from plone.testing.z2 import Browser

import transaction
import unittest


class TestUtils(unittest.TestCase):

    def _create_dummy_fti(self, behavior=None):
        self.fti = DexterityFTI('test')
        self.portal.portal_types._setObject('test', self.fti)
        self.fti.klass = 'plone.dexterity.content.Container'
        self.fti.filter_content_types = False
        if behavior:
            self.fti.behaviors = (behavior,)

    def _create_obj(self, portal_type='test'):
        api.content.create(
            container=self.portal,
            type=portal_type,
            id='test',
            title='Test',
        )
        transaction.commit()
        self.obj = self.portal['test']

    def _set_browser(self):
        self.app = self.layer['app']
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(
                SITE_OWNER_NAME, SITE_OWNER_PASSWORD,
            ),
        )
