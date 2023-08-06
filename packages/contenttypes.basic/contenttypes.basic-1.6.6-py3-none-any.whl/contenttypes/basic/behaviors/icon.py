# -*- coding: utf-8 -*-
from contenttypes.basic import _
from contenttypes.basic.fields.icon import IconField
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IIconBehaviorSchema(model.Schema):
    """ Icon Behavior Schema
    """

    icon = IconField(
        title=_('Icon'),
        description=_('Select an icon'),
        required=True,
    )


@implementer(IIconBehaviorSchema)
@adapter(IDexterityContent)
class IconBehaviorFactory(object):

    def __init__(self, context):
        self.context = context

    @property
    def icon(self):
        return self.context.icon

    @icon.setter
    def icon(self, value):
        self.context.icon = value
