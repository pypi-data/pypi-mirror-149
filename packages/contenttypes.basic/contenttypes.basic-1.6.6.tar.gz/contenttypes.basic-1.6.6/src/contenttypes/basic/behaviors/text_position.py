# -*- coding: utf-8 -*-
from contenttypes.basic import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


PositionVocabulary = SimpleVocabulary([
    SimpleTerm(value=1, title=_('Upper - Left')),
    SimpleTerm(value=2, title=_('Upper - Centre')),
    SimpleTerm(value=3, title=_('Upper - Right')),
    SimpleTerm(value=4, title=_('Centre - Left')),
    SimpleTerm(value=5, title=_('Centre - Centre')),
    SimpleTerm(value=6, title=_('Centre - Right')),
    SimpleTerm(value=7, title=_('Bottom - Left')),
    SimpleTerm(value=8, title=_('Bottom - Centre')),
    SimpleTerm(value=9, title=_('Bottom - Right')),
])


@provider(IFormFieldProvider)
class ITextPositionSchema(model.Schema):
    """ Text Position Schema
    """

    text_position = schema.Choice(
        title=_('Position'),
        description=_(
            'Position where the title and the button will be displayed over '
            'the image. Only useful for medium and up screens.',
        ),
        vocabulary=PositionVocabulary,
        required=False,
        default=5,
    )


@implementer(ITextPositionSchema)
@adapter(IDexterityContent)
class TextPositionFactory(object):

    def __init__(self, context):
        self.context = context

    @property
    def text_position(self):
        return self.context.text_position

    @text_position.setter
    def text_position(self, value):
        self.context.text_position = value
