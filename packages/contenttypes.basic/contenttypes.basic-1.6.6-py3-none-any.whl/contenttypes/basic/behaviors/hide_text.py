# -*- coding: utf-8 -*-
from contenttypes.basic import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IHideTextSchema(model.Schema):
    """ Text Info Schema
    """

    hide_text = schema.Bool(
        title=_('Hide Text'),
        required=False,
    )


@implementer(IHideTextSchema)
@adapter(IDexterityContent)
class HideTextFactory(object):

    def __init__(self, context):
        self.context = context

    @property
    def hide_text(self):
        return self.context.hide_text

    @hide_text.setter
    def hide_text(self, value):
        self.context.hide_text = value
