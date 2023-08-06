# -*- coding: utf-8 -*-
from contenttypes.basic import _
from contenttypes.basic.fields.colour import ColourField
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IColourBehaviorSchema(model.Schema):
    """ Colour Behavior Schema
    """

    colour = ColourField(
        title=_('Colour'),
        required=False,
        default='#000000',
    )


@implementer(IColourBehaviorSchema)
@adapter(IDexterityContent)
class ColourBehaviorFactory(object):

    def __init__(self, context):
        self.context = context

    @property
    def colour(self):
        return self.context.colour

    @colour.setter
    def colour(self, value):
        self.context.colour = value
