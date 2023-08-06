# -*- coding: utf-8 -*-
from contenttypes.basic.testing import CONTENTTYPES_BASIC_FUNCTIONAL_TESTING
from contenttypes.basic.tests import TestUtils
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class ViewFunctionalTest(TestUtils):

    layer = CONTENTTYPES_BASIC_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_redirect_custom_view(self):
        self._create_dummy_fti(behavior='contenttypes.basic.link')
        self._create_obj()
        self._set_browser()

        self.browser.open(self.portal_url + '/test/@@link_redirect_custom_view')
        contents = self.browser.contents
        template_class = 'template-link_redirect_custom_view'
        self.assertTrue(template_class in contents)

        self.browser.open(self.portal_url + '/test/edit')
        link = self.browser.getControl(
            name='form.widgets.ILinkBehaviorSchema.remoteUrl.external',
        )
        link.value = 'https://www.google.es'
        save = self.browser.getControl(name='form.buttons.save')
        save.click()

        self.browser.open(self.portal_url + '/test/@@link_redirect_custom_view')
        contents = self.browser.contents
        message_info = 'portalMessage info'
        self.assertTrue(message_info in contents)
