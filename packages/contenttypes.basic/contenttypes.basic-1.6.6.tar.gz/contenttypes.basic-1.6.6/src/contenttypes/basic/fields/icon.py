# -*- coding: utf-8 -*-
from contenttypes.basic.interfaces import IIconField
from zope.interface import implementer
from zope.schema import TextLine


@implementer(IIconField)
class IconField(TextLine):
    """ Icon Field
    """
