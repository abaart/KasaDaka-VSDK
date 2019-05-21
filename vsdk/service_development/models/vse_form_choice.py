from django.db import models
from django.utils.translation import ugettext_lazy as _

from .vs_element import VoiceServiceElement, VoiceServiceSubElement


class FormChoice(VoiceServiceElement):
    MODEL_CHOICES = (
        ('seed', 'Seed'),
    )
    ACTION_CHOICES = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('remove', 'Remove'),
    )

    _urls_name = 'service-development:form-choice'
    _redirect = models.ForeignKey(
            VoiceServiceElement,
            on_delete=models.SET_NULL,
            verbose_name=_('Redirect element'),
            help_text=_("The element to redirect to after a choice has been made."),
            related_name='%(app_label)s_%(class)s_redirect_related',
            blank=True,
            null=True)
    model_type = models.CharField(verbose_name=_("Model for choices"), max_length=30, choices=MODEL_CHOICES)
    action_type = models.CharField(verbose_name=_("Action"), max_length=30, choices=ACTION_CHOICES)

    class Meta:
        verbose_name = _('Form Choice Element')

    @property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        if self._redirect:
            return VoiceServiceSubElement.objects.get_subclass(id = self._redirect.id)
        else:
            return None

    def __str__(self):
        return self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def validator(self):
        errors = []
        errors.extend(super(FormChoice, self).validator())
        if not self._redirect:
            errors.append(_('Form_Choice %s does not have a redirect element')%self.name)

        return errors

