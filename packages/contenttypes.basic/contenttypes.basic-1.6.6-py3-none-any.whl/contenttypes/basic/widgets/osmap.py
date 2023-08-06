# -*- coding: utf-8 -*-
from contenttypes.basic import _
from contenttypes.basic.interfaces import IOSMapField
from contenttypes.basic.interfaces import IOSMapWidget
from datetime import datetime
from plone import api
from plone.api.exc import InvalidParameterError
from z3c.form.browser.text import TextWidget
from z3c.form.converter import BaseDataConverter
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer


@implementer(IOSMapWidget)
class OSMapWidget(TextWidget):

    name = 'osmap-widget'
    label = _('OSMap Widget')
    timestamp = datetime.now().strftime('%s')

    @property
    def portal_url(self):
        return api.portal.get().absolute_url()

    @property
    def default_value(self):
        return self.field.default or '0|0'

    def default_value_map(self):
        try:
            return api.portal.get_registry_record(name='coordinates.map_center')
        except InvalidParameterError:
            return '0|0'


@implementer(IFieldWidget)
@adapter(IOSMapField, IFormLayer)
def OSMapFieldWidget(field, request):
    return FieldWidget(field, OSMapWidget(request))


@adapter(IOSMapField, IOSMapWidget)
class OSMapConverter(BaseDataConverter):
    """ Convert between the context and the widget
    """

    def toWidgetValue(self, value):
        return self.parse_coordinates(value)

    def toFieldValue(self, value):
        return self.parse_coordinates(value)

    def parse_coordinates(self, value):
        if not value:
            return '0|0'

        coordinates = value.split('|')
        if len(coordinates) != 2:
            return '0|0'

        coordinates = map(lambda coord: self.parse_float(coord), coordinates)
        return '|'.join(coordinates)

    def parse_float(self, value):
        try:
            value = float(value)
            value = str(value)
            if value == '0.0':
                value = '0'
            return value
        except ValueError:
            return '0'
