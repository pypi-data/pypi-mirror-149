# -*- coding: utf-8 -*-
from contenttypes.basic import _
from contenttypes.basic.fields.osmap import OSMapField
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IOSMapBehaviorSchema(model.Schema):
    """ OSmap Behavior Schema
    """

    geolocation = OSMapField(
        title=_('Geolocation'),
        description=_('Enter an address or set the location mark on the map'),
        required=False,
    )


@implementer(IOSMapBehaviorSchema)
@adapter(IDexterityContent)
class OSMapBehaviorFactory(object):

    def __init__(self, context):
        self.context = context

    @property
    def geolocation(self):
        return self.context.geolocation

    @geolocation.setter
    def geolocation(self, value):
        self.context.geolocation = value
