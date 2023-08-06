# -*- coding: utf-8 -*-
from contenttypes.basic.interfaces import IOSMapField
from zope.interface import implementer
from zope.schema import TextLine


@implementer(IOSMapField)
class OSMapField(TextLine):
    """ OSMap Field
    """
