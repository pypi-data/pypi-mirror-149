# -*- coding: utf-8 -*-
from contenttypes.basic import _
from contenttypes.basic.interfaces import IIconField
from contenttypes.basic.interfaces import IIconWidget
from lxml import etree
from plone import api
from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer


@implementer(IIconWidget)
class IconWidget(TextWidget):

    name = 'icon-widget'
    label = _('Icon Widget')
    _xml = None

    @property
    def portal_url(self):
        return api.portal.get().absolute_url()

    @property
    def xml(self):
        if not self._xml:
            self._xml = self.get_xml()
        return self._xml

    def get_xml(self):
        sprite_view = api.portal.get().restrictedTraverse('@@sprite-icons')
        result = sprite_view()
        symbols = []

        root = etree.fromstring(result)
        for element in root.iter('{http://www.w3.org/2000/svg}symbol'):
            symbols.append(element.get('id'))

        return symbols


@implementer(IFieldWidget)
@adapter(IIconField, IFormLayer)
def IconFieldWidget(field, request):
    return FieldWidget(field, IconWidget(request))
