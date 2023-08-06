# -*- coding: utf-8 -*-
from contenttypes.basic import _
from plone import api
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


MORE_INFORMATION = _('More information')


@provider(IContextAwareDefaultFactory)
def default_button_text(context):
    return api.portal.translate('More information', 'contenttypes.basic', lang=api.portal.get_current_language())


@provider(IFormFieldProvider)
class IButtonTextSchema(model.Schema):
    """ Button Text Schema
    """

    button_text = schema.TextLine(
        title=_(u'Button text'),
        required=False,
        defaultFactory=default_button_text,
    )


@implementer(IButtonTextSchema)
@adapter(IDexterityContent)
class ButtonTextFactory(object):

    def __init__(self, context):
        self.context = context

    @property
    def button_text(self):
        return self.context.button_text

    @button_text.setter
    def button_text(self, value):
        self.context.button_text = value
