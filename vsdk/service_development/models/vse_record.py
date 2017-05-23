from django.db import models

from vsdk.service_development.models import VoiceLabel
from .vs_element import VoiceServiceElement

class Record(VoiceServiceElement):
    """
        An element that records user input to a sound file.
    """

    _urls_name = 'service-development:record'

    not_heard_voice_label = models.ForeignKey(
        VoiceLabel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='not_heard_voice_label'
    )


    barge_in = models.BooleanField('Allow the caller to start recording immediately', default=True)

    repeat_recording_to_caller = models.BooleanField('Repeat the recording to the caller before asking for confirmation', default=True)
    repeat_voice_label = models.ForeignKey(
        VoiceLabel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repeat_voice_label'
    )

    ask_confirmation = models.BooleanField(
        'Ask the caller to confirm their recording', default=True)
    ask_confirmation_voice_label = models.ForeignKey(
        VoiceLabel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='confirmation_voice_label',
    )

    final_voice_label = models.ForeignKey(
        VoiceLabel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='final_voice_label',
    )


    _redirect = models.ForeignKey(
        VoiceServiceElement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_related',
        help_text="The element to redirect to after the message has been played.")

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

    def validator(self):
        errors = []
        errors.extend(super(Record, self).validator())
        if not self._redirect:
            errors.append('Record %s does not have a redirect element' % self.name)
        return errors
