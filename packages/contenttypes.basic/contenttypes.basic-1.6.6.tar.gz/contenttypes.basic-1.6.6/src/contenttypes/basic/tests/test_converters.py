# -*- coding: utf-8 -*-
from contenttypes.basic.testing import CONTENTTYPES_BASIC_FUNCTIONAL_TESTING
from contenttypes.basic.tests import TestUtils
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class ConvertersFunctionalTest(TestUtils):

    layer = CONTENTTYPES_BASIC_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_osmap_converter(self):
        self._create_dummy_fti(behavior='contenttypes.basic.osmap')
        self._create_obj()
        self._set_browser()

        self.browser.open(self.portal_url + '/test/edit')
        geolocation = self.browser.getControl(
            name='form.widgets.IOSMapBehaviorSchema.geolocation',
        )
        geolocation_value = 'wrong_number|0.6267842'
        geolocation.value = geolocation_value
        save = self.browser.getControl(name='form.buttons.save')
        save.click()
        self.assertTrue(self.obj.geolocation, '0|0.6267842')

        self.browser.open(self.portal_url + '/test/edit')
        geolocation = self.browser.getControl(
            name='form.widgets.IOSMapBehaviorSchema.geolocation',
        )
        geolocation_value = 'wrong_number|wrong_number'
        geolocation.value = geolocation_value
        save = self.browser.getControl(name='form.buttons.save')
        save.click()
        self.assertTrue(self.obj.geolocation, '0|0')

        self.browser.open(self.portal_url + '/test/edit')
        geolocation = self.browser.getControl(
            name='form.widgets.IOSMapBehaviorSchema.geolocation',
        )
        geolocation_value = 'wrong_length'
        geolocation.value = geolocation_value
        save = self.browser.getControl(name='form.buttons.save')
        save.click()
        self.assertTrue(self.obj.geolocation, '0|0')

        self.browser.open(self.portal_url + '/test/edit')
        geolocation = self.browser.getControl(
            name='form.widgets.IOSMapBehaviorSchema.geolocation',
        )
        geolocation_value = '0.1|0.1'
        geolocation.value = geolocation_value
        save = self.browser.getControl(name='form.buttons.save')
        save.click()
        self.assertTrue(self.obj.geolocation, '0.1|0.1')
