# -*- coding: utf-8 -*-
from contenttypes.basic.interfaces import IAnnouncement
from contenttypes.basic.interfaces import IBanner
from contenttypes.basic.interfaces import IIcon
from contenttypes.basic.interfaces import ISlide
from plone.dexterity.content import Container
from zope.interface import implementer


@implementer(IAnnouncement)
class Announcement(Container):
    """ Convenience subclass for ``Announcement`` portal type
    """


@implementer(IBanner)
class Banner(Container):
    """ Convenience subclass for ``Banner`` portal type
    """


@implementer(IIcon)
class Icon(Container):
    """ Convenience subclass for ``Icon`` portal type
    """


@implementer(ISlide)
class Slide(Container):
    """ Convenience subclass for ``Slide`` portal type
    """
