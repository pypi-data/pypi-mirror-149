# -*- coding: utf-8 -*-
from plone.app.contenttypes.interfaces import ILink
from plone.supermodel import model
from z3c.form.interfaces import ITextWidget
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.interfaces import ITextLine


class IContenttypesBasicLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IAnnouncement(model.Schema):
    """ Marker interface and Schema for Announcement
    """


class IBanner(model.Schema):
    """ Marker interface and Schema for Banner
    """


class IIcon(model.Schema):
    """ Marker interface and Schema for Icon
    """


class ISlide(model.Schema):
    """ Marker interface and Schema for Slide
    """


class IHideTextBehavior(Interface):
    """ Marker interface for Text Info Behavior
    """


class IButtonTextBehavior(Interface):
    """ Marker interface for Button Text Behavior
    """


class ITextPositionBehavior(Interface):
    """ Marker interface for Text Position Behavior
    """


class IColourBehavior(Interface):
    """ Marker interface for Colour Behavior
    """


class IIconBehavior(Interface):
    """ Marker interface for Icon Behavior
    """


class ILinkBehavior(ILink):
    """ Marker interface for Link Behavior
    """


class IOSMapBehavior(Interface):
    """ Marker interface for OSMap Behavior
    """


class IIconWidget(ITextWidget):
    """ Marker interface for Icon Widget
    """


class IColourWidget(ITextWidget):
    """ Marker interface for Colour Widget
    """


class IOSMapWidget(ITextWidget):
    """ Marker interface for OSMap Widget
    """


class IIconField(ITextLine):
    """ Marker interface for Icon Field
    """


class IColourField(ITextLine):
    """ Marker interface for Colour Field
    """


class IOSMapField(ITextLine):
    """ Marker interface for OSMap Field
    """
