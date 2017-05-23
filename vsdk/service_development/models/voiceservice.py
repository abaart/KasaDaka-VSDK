from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


from .voicelabel import VoiceLabel, Language, VoiceFragment
from .vs_element import VoiceServiceElement

class VoiceService(models.Model):
    _urls_name = 'service-development:voice-service'

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    creation_date = models.DateTimeField('date created', auto_now_add = True)
    modification_date = models.DateTimeField('date last modified', auto_now = True)
    active = models.BooleanField('Voice service active',
            help_text = "This voice service is only accessible for users when marked active.")
    _start_element = models.ForeignKey(
            VoiceServiceElement,
            related_name='%(app_label)s_%(class)s_related',
            null = True,
            blank = True)
    requires_registration = models.BooleanField('Requires user registration')

    supported_languages = models.ManyToManyField(Language, blank = True)

    end_user_service = models.BooleanField(default= False)
    radio_journalist_service = models.BooleanField(default=False)

    @property
    def start_element(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        return VoiceServiceElement.objects.get_subclass(id = self._start_element.id)

    @property
    def supports_single_language(self):
        """
        Returns True if this service supports a single language
        """
        return len(self.supported_languages.all()) == 1

    def get_vxml_url(self):
        try:
            return reverse(self._urls_name, kwargs ={'voice_service_id': self.id})
        except NoReverseMatch:
            return "unknown"
    get_vxml_url.short_description = "VoiceXML endpoint URL"
    vxml_url = property(get_vxml_url)
    
    def __str__(self):
        return 'Voice Service: %s' % self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        errors = []
        if not self._start_element:
            errors.append('No starting element')
        else:
            errors.extend(self.start_element.validator())
        if len(self.supported_languages.all()) == 0:
            errors.append('No supported languages')
        return errors

    def get_elements(self):
        #TODO
        return []
