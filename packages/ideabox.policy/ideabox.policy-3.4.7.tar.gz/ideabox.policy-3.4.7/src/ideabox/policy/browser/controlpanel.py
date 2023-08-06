# -*- coding: utf-8 -*-

from ideabox.policy import _
from plone.app.registry.browser import controlpanel
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.autoform import directives as form
from z3c.form.interfaces import INPUT_MODE
from zope import schema
from zope.interface import Interface


class InvalidEmailError(schema.ValidationError):
    __doc__ = u"Please enter a valid e-mail address."


class IIdeaBoxSettingsSchema(Interface):

    project_manager_email = schema.TextLine(
        title=_(u"Email address of the project manager"),
        description=_(
            u"If there are multiple email addresses, separate them with semicolons"
        ),
    )

    form.widget("legal_information_text", klass="pat-tinymce")
    legal_information_text = schema.Text(
        title=_(u"Legal information text"),
        required=False,
        description=_(u"Legal information text"),
    )

    project_directly_submitted = schema.Bool(
        title=u"Projects directly submitted",
        description=u"If checked, projects are public as soon as they are submitted.",
        default=True,
    )


class IdeaBoxSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IIdeaBoxSettingsSchema
    label = _(u"Configuration for ideabox product")
    description = _(u"")

    def updateFields(self):
        super(IdeaBoxSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(IdeaBoxSettingsEditForm, self).updateWidgets()
        self.fields["legal_information_text"].widgetFactory[
            INPUT_MODE
        ] = WysiwygFieldWidget


class IdeaBoxSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = IdeaBoxSettingsEditForm
