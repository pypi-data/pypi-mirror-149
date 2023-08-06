# -*- coding: utf-8 -*-
from contenttypes.basic.interfaces import IButtonTextBehavior
from contenttypes.basic.interfaces import IColourBehavior
from contenttypes.basic.interfaces import IHideTextBehavior
from contenttypes.basic.interfaces import IIconBehavior
from contenttypes.basic.interfaces import ILinkBehavior
from contenttypes.basic.interfaces import IOSMapBehavior
from contenttypes.basic.interfaces import ITextPositionBehavior
from contenttypes.basic.testing import CONTENTTYPES_BASIC_FUNCTIONAL_TESTING
from contenttypes.basic.tests import TestUtils
from plone.app.contenttypes.interfaces import ILink
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.uuid.utils import uuidToCatalogBrain


class BehaviorFunctionalTest(TestUtils):

    layer = CONTENTTYPES_BASIC_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_hide_text(self):
        self._create_dummy_fti(behavior='contenttypes.basic.hide_text')
        self._create_obj()
        self._set_browser()

        self.assertTrue(IHideTextBehavior.providedBy(self.obj))

        self.browser.open(self.portal_url + '/test/edit')
        checkbox = self.browser.getControl(
            name='form.widgets.IHideTextSchema.hide_text:list',
        )
        checkbox.value = ['selected']
        save = self.browser.getControl(name='form.buttons.save')
        save.click()

        self.assertTrue(self.obj.hide_text)

    def test_behavior_button_text(self):
        self._create_dummy_fti(behavior='contenttypes.basic.button_text')
        self._create_obj()
        self._set_browser()

        self.assertTrue(IButtonTextBehavior.providedBy(self.obj))
        self.assertEqual(self.obj.button_text, 'More information')

        self.browser.open(self.portal_url + '/test/edit')
        textline = self.browser.getControl(
            name='form.widgets.IButtonTextSchema.button_text',
        )
        textline_value = 'See more'
        textline.value = textline_value
        save = self.browser.getControl(name='form.buttons.save')
        save.click()

        self.assertEqual(self.obj.button_text, textline_value)

    def test_behavior_text_position(self):
        self._create_dummy_fti(behavior='contenttypes.basic.text_position')
        self._create_obj()
        self._set_browser()

        self.assertTrue(ITextPositionBehavior.providedBy(self.obj))

        self.browser.open(self.portal_url + '/test/edit')
        select = self.browser.getControl(
            name='form.widgets.ITextPositionSchema.text_position:list',
        )
        select.value = ['1']
        save = self.browser.getControl(name='form.buttons.save')
        save.click()

        self.assertTrue(self.obj.text_position, 1)

    def test_behavior_icon(self):
        self._create_dummy_fti(behavior='contenttypes.basic.icon')
        self._create_obj()
        self._set_browser()

        self.assertTrue(IIconBehavior.providedBy(self.obj))

        self.browser.open(self.portal_url + '/test/edit')
        icon = self.browser.getControl(
            name='form.widgets.IIconBehaviorSchema.icon',
        )
        icon_value = 'euro'
        icon.value = icon_value
        save = self.browser.getControl(name='form.buttons.save')
        save.click()

        self.assertTrue(self.obj.icon, icon_value)

    def test_behavior_colour(self):
        self._create_dummy_fti(behavior='contenttypes.basic.colour')
        self._create_obj()
        self._set_browser()

        self.assertTrue(IColourBehavior.providedBy(self.obj))
        self.assertEqual(self.obj.colour, '#000000')

        self.browser.open(self.portal_url + '/test/edit')
        colour = self.browser.getControl(
            name='form.widgets.IColourBehaviorSchema.colour',
        )
        colour_value = '#ffffff'
        colour.value = colour_value
        save = self.browser.getControl(name='form.buttons.save')
        save.click()

        self.assertTrue(self.obj.colour, colour_value)

    def test_behavior_link(self):
        self._create_dummy_fti(behavior='contenttypes.basic.link')
        self._create_obj()
        self._set_browser()

        self.assertTrue(ILinkBehavior.providedBy(self.obj))
        self.assertTrue(ILink.providedBy(self.obj))

        uuid_link = self.obj.UID()

        self.browser.open(self.portal_url + '/test/edit')
        link = self.browser.getControl(
            name='form.widgets.ILinkBehaviorSchema.remoteUrl.internal',
        )
        link.value = uuid_link
        save = self.browser.getControl(name='form.buttons.save')
        save.click()

        brain = uuidToCatalogBrain(uuid_link)

        self.assertTrue(
            self.obj.remoteUrl,
            '{{portal_url}}/resolveuid/{uuid}'.format(uuid=uuid_link),
        )
        self.assertTrue(
            brain.getRemoteUrl,
            '/{portal_id}/resolveuid/{uuid}'.format(
                portal_id=self.portal.id,
                uuid=uuid_link,
            ),
        )

    def test_behavior_osmap(self):
        self._create_dummy_fti(behavior='contenttypes.basic.osmap')
        self._create_obj()
        self._set_browser()

        self.assertTrue(IOSMapBehavior.providedBy(self.obj))
        self.assertEqual(self.obj.geolocation, None)

        self.browser.open(self.portal_url + '/test/edit')
        geolocation = self.browser.getControl(
            name='form.widgets.IOSMapBehaviorSchema.geolocation',
        )
        geolocation_value = '41.6147605|0.6267842'
        geolocation.value = geolocation_value
        save = self.browser.getControl(name='form.buttons.save')
        save.click()

        self.assertTrue(self.obj.geolocation, geolocation_value)
