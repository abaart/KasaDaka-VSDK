from django.db import models

from vsdk.service_development.models import VoiceLabel
from .vs_element import VoiceServiceElement, VoiceServiceSubElement
from .voiceservice import VoiceService

class ListCallSessions(VoiceServiceElement):
    _urls_name = 'service-development:list-call-session'

    list_sessions_from_service = models.ForeignKey(VoiceService, on_delete=models.SET_NULL, null=True)

    name_voice_label = models.ForeignKey(
        VoiceLabel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='name_voice_label'
    )

    category_voice_label = models.ForeignKey(
        VoiceLabel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category_voice_label'
    )

    message_voice_label = models.ForeignKey(
        VoiceLabel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='message_voice_label'
    )

    _redirect = models.ForeignKey(
        VoiceServiceElement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_related',
        help_text="The element to redirect to after the session has been played.")

    empty_redirect = models.ForeignKey(
        VoiceServiceElement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%empty_(app_label)s_%(class)s_related',
        help_text="The element to redirect to if there is not session to be played.")


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
        return "List callsessions: " + self.name

    def is_valid(self):
        return len(self.validator()) == 0

    is_valid.boolean = True

    def validator(self):
        errors = []
        errors.extend(super(ListCallSessions, self).validator())
        if not self._redirect:
            errors.append('List call session %s does not have a redirect element' % self.name)
        return errors