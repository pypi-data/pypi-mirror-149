# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from ideabox.policy.utils import can_view_rating
from plone import api
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class ProjectsView(BrowserView):
    @property
    def default_image(self):
        return "{0}/project_default.jpg".format(api.portal.get().absolute_url())

    def rating(self, context):
        return can_view_rating(context)

    def get_theme(self, key):
        if not hasattr(self, "_themes"):
            factory = getUtility(IVocabularyFactory, "collective.taxonomy.theme")
            self._themes = factory(self.context)
        try:
            return self._themes.getTerm(key).title
        except KeyError:
            return ""

    def get_path(self):
        context = self.context
        return "/".join(context.getPhysicalPath())

    def can_submit_project(self):
        if self.context.portal_type != "campaign":
            return False
        return getattr(self.context, "project_submission", False)
