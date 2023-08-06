# -*- coding: utf-8 -*-
from contenttypes.basic import _
from plone.autoform.directives import widget
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class ILinkBehaviorSchema(model.Schema):
    """ Link Behavior Schema
    """

    widget(remoteUrl='plone.app.z3cform.widget.LinkFieldWidget')
    remoteUrl = schema.TextLine(
        title=_('Link'),
        required=False,
    )


@implementer(ILinkBehaviorSchema)
@adapter(IDexterityContent)
class LinkBehaviorFactory(object):

    def __init__(self, context):
        self.context = context

    @property
    def remoteUrl(self):
        return self.context.remoteUrl

    @remoteUrl.setter
    def remoteUrl(self, value):
        self.context.remoteUrl = value
