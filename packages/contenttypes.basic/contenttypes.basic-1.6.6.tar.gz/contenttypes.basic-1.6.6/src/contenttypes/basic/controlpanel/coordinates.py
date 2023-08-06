# -*- coding: utf-8 -*-
from contenttypes.basic import _
from contenttypes.basic.widgets.osmap import OSMapWidget
from plone.app.registry.browser import controlpanel
from plone.autoform import directives
from zope import schema
from zope.interface import Interface


class ICoordinatesControlPanel(Interface):

    directives.widget('map_center', OSMapWidget)
    map_center = schema.TextLine(
        title=_('Map center'),
        description=_('Set the default coordinates for the map widget.'),
        default='0|0',
    )


class CoordinatesControlPanelForm(controlpanel.RegistryEditForm):
    """ CoordinatesControlPanelForm
    """
    schema = ICoordinatesControlPanel
    schema_prefix = 'coordinates'
    label = _('Coordinates')


class CoordinatesControlPanel(controlpanel.ControlPanelFormWrapper):
    """ CoordinatesControlPanel
    """
    form = CoordinatesControlPanelForm
