# -*- coding: utf-8 -*-
from contenttypes.basic.interfaces import IColourField
from zope.interface import implementer
from zope.schema import TextLine


@implementer(IColourField)
class ColourField(TextLine):
    """ Colour Field
    """
