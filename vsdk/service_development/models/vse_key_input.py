from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from .vs_element import VoiceServiceElement

class KeyInput(VoiceServiceElement):
    _urls_name = 'service-development:key-input'
    input = models.IntegerField(_('Input'), default = 0, blank = True)
    _redirect = models.ForeignKey(
            VoiceServiceElement,
            on_delete = models.SET_NULL,
            verbose_name = _('Redirect element'),
            help_text = _("The element to redirect to when the user has entered the input."),
            related_name='%(app_label)s_%(class)s_redirect_related',
            blank = True,
            null = True)

    class Meta:
        verbose_name = _('Key Input Element')

    @property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        if self._redirect :
            return VoiceServiceElement.objects.get_subclass(id = self._redirect.id)
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
        errors.extend(super(KeyInput, self).validator())
        if not self._redirect:
            errors.append(ugettext('No redirect in key input element: "%s"')%str(self))
        elif not self.input:
            if self._redirect.id == self.id:
                errors.append(ugettext('There is a loop in %s')%str(self))

        return errors
