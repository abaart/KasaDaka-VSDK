from django.db import models
from model_utils.managers import InheritanceManager
from django.urls import reverse

from .voicelabel import VoiceLabel

class VoiceServiceSubElement(models.Model):
    """
    A sub-element in a voice service (could be ChoiceOption, etc).
    Is NOT accessible through HTTP in a VoiceXML
    """

    #use django_model_utils to be able to find out what is the subclass of this element
    #see: https://django-model-utils.readthedocs.io/en/latest/managers.html#inheritancemanager
    objects = InheritanceManager()

    service = models.ForeignKey('VoiceService', on_delete = models.CASCADE,
            help_text="The service to which this element belongs")
    creation_date = models.DateTimeField('date created', auto_now_add = True)
    modification_date = models.DateTimeField('date last modified', auto_now = True)

    name = models.CharField(max_length=100)

    description = models.CharField(
            max_length = 1000,
            blank = True)

    map_to_call_session_property = models.CharField(max_length=100, default='', null=True, blank=True)

    voice_label = models.ForeignKey(
            VoiceLabel,
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            )

    def __str__(self):
        return "Sub-element: %s" % self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        """
        Returns a list of problems with this element that would surface when accessing
        through voice.
        """
        errors = []
        #check if voice label is present, and validate it
        if self.voice_label:
            for language in self.service.supported_languages.all():
                errors.extend(self.voice_label.validator(language))
        else:
            errors.append('No VoiceLabel in: "%s"'%str(self))
        return errors


    def get_voice_fragment_url(self, language):
        """
        Returns the url of the audio file of this element, in the given language.
        """
        return self.voice_label.get_voice_fragment_url(language)


class VoiceServiceElement(VoiceServiceSubElement):
    """
    An element in a voice service (could be Choice, Message, etc.)
    Is accessible through HTTP in a generated VoiceXML
    """
    objects = InheritanceManager()
    _urls_name = "" #This should be the same as in urls.py
    
    
    def __str__(self):
        return "Element: %s" % self.name

    def get_absolute_url(self, session):
        """
        Returns the url at which this element is accessible through VoiceXML.
        """
        url_name = self._urls_name
        return reverse(url_name, kwargs= {'element_id':str(self.id), 'session_id':session.id})
