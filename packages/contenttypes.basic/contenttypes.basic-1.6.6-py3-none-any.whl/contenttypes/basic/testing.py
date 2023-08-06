# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import contenttypes.basic


class ContenttypesBasicLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=contenttypes.basic)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'contenttypes.basic:default')


class ContenttypesBasicControlPanelLayer(ContenttypesBasicLayer):

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)
        applyProfile(
            portal,
            'contenttypes.basic:z-coordinates-controlpanel',
        )


CONTENTTYPES_BASIC_FIXTURE = ContenttypesBasicLayer()
CONTENTTYPES_BASIC_CONTROLPANEL_FIXTURE = ContenttypesBasicControlPanelLayer()


CONTENTTYPES_BASIC_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CONTENTTYPES_BASIC_FIXTURE,),
    name='ContenttypesBasicLayer:IntegrationTesting',
)


CONTENTTYPES_BASIC_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CONTENTTYPES_BASIC_FIXTURE,),
    name='ContenttypesBasicLayer:FunctionalTesting',
)


CONTENTTYPES_BASIC_CONTROLPANEL_TESTING = FunctionalTesting(
    bases=(CONTENTTYPES_BASIC_CONTROLPANEL_FIXTURE,),
    name='ContenttypesBasicControlPanelLayer:FunctionalTesting',
)


CONTENTTYPES_BASIC_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CONTENTTYPES_BASIC_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='ContenttypesBasicLayer:AcceptanceTesting',
)
