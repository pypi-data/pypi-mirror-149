# -*- coding: utf-8 -*-
from plone.app.contenttypes.browser.link_redirect_view import LinkRedirectView as LinkRedirect
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class LinkRedirectView(LinkRedirect):

    index = ViewPageTemplateFile('link.pt')

    def __call__(self):
        if not self.context.remoteUrl:
            return self.index()
        return super().__call__()
