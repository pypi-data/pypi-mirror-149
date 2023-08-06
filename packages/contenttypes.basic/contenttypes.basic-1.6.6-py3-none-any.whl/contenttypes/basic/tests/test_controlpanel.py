# -*- coding: utf-8 -*-
from contenttypes.basic.testing import CONTENTTYPES_BASIC_CONTROLPANEL_TESTING
from contenttypes.basic.tests import TestUtils
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class ControlPanelFunctionalTest(TestUtils):

    layer = CONTENTTYPES_BASIC_CONTROLPANEL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()
        self.portal_setup = api.portal.get_tool('portal_setup')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_coordinates_controlpanel(self):
        self._set_browser()
        self.browser.open(self.portal_url + '/@@coordinates-controlpanel')
        contents = self.browser.contents
        field = 'form-widgets-map_center'
        self.assertTrue(field in contents)
