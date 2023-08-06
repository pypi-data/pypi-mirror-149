# -*- coding: utf-8 -*-
from Products.Five import BrowserView


class SpriteView(BrowserView):
    """ SpriteView
    """

    def __call__(self):
        response = self.request.response
        response.setHeader('Content-type', 'image/svg+xml')
        return super(SpriteView, self).__call__()
