from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from vsdk.service_development.models import VoiceLabel
from .vs_element import VoiceServiceElement
from .farmer_input import FarmerInputCategory

class Record(VoiceServiceElement):
    """
        An element that records farmer input to a sound file.
    """

    _urls_name = 'service-development:record'

    not_heard_voice_label = models.ForeignKey(
        VoiceLabel,
        verbose_name = _('No response voice label'),
        help_text = _('The voice label that is played when the system does not recognize the farmer saying anything. Example: "We did not hear anything, please speak your message."'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='not_heard_voice_label'
    )
    repeat_recording_to_caller = models.BooleanField(_('Repeat the recording to the caller before asking for confirmation'), default=True)
    repeat_voice_label = models.ForeignKey(
        VoiceLabel,
        verbose_name = _('Repeat input voice label'),
        help_text = _('The voice label that is played before the system repeats the farmer input. Example: "Your message is:"'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repeat_voice_label'
    )
    ask_confirmation = models.BooleanField(
        _('Ask the caller to confirm their recording'), default=True)
    ask_confirmation_voice_label = models.ForeignKey(
        VoiceLabel,
        verbose_name = _('Ask for confirmation voice label'),
        help_text = _('The voice label that asks the farmer to confirm their pinput. Example: "Are you satisfied with your recording? Press 1 to confirm, or press 2 to retry."'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='confirmation_voice_label',
    )
    final_voice_label = models.ForeignKey(
        VoiceLabel,
        verbose_name = _('Final voice label'),
        help_text = _('The voice label that is played when the farmer has completed the recording process. Example: "Thank you for your message! The message has been stored successfully."'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='final_voice_label',
    )
    input_category = models.ForeignKey(
        FarmerInputCategory,
        verbose_name = _('Input category'),
        help_text = _('The category under which the input will be stored in the system.'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='input_category',
    )
    max_time_input = models.IntegerField(_('Maximum time of message (seconds)'),default=180)


    _redirect = models.ForeignKey(
        VoiceServiceElement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name = _('Redirect element'),
        help_text=_("The element to redirect to after the message has been played."))

    class Meta:
        verbose_name = _('Spoken Input Element')

    @property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        if self._redirect:
            return VoiceServiceElement.objects.get_subclass(id=self._redirect.id)
        else:
            return None

    def __str__(self):
        return "Record: " + self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def validator(self):
        errors = []
        errors.extend(super(Record, self).validator())
        if not self._redirect:
            errors.append(ugettext('Record %s does not have a redirect element') % self.name)
        return errors

