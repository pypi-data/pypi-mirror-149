# -*- coding: utf-8 -*-
from contenttypes.basic import _
from contenttypes.basic.interfaces import IColourField
from contenttypes.basic.interfaces import IColourWidget
from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer


@implementer(IColourWidget)
class ColourWidget(TextWidget):

    name = 'colour-widget'
    label = _('Colour Widget')


@implementer(IFieldWidget)
@adapter(IColourField, IFormLayer)
def ColourFieldWidget(field, request):
    return FieldWidget(field, ColourWidget(request))
