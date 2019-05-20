from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from .vs_element import VoiceServiceElement

class KeyInput(VoiceServiceElement):
    """
    An element that presents a Voice Label to the farmer.
    """
    _urls_name = 'service-development:key-input'
    _redirect = models.ForeignKey(
            VoiceServiceElement,
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='%(app_label)s_%(class)s_related',
            verbose_name=_('Redirect element'),
            help_text = _("The element to redirect to after the key_input has been played."))
    save_option = models.CharField(_('Save to'), max_length = 100, blank = True)

    class Meta:
        verbose_name = _('Key input Element')

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
        return _("Key Input: ") + self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def validator(self):
        errors = []
        errors.extend(super(KeyInput, self).validator())
        if not self._redirect:
            errors.append(ugettext('Key_input %s does not have a redirect element')%self.name)

        return errors
