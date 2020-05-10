from datetime import date, timedelta

from django.db import models
from model_utils.managers import InheritanceManager
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

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
            help_text=_("The service to which this element belongs"))
    creation_date = models.DateTimeField(_('Date created'), auto_now_add = True)
    modification_date = models.DateTimeField(_('Date last modified'), auto_now = True)
    name = models.CharField(_('Name'),max_length=100)

    is_forecast = models.BooleanField(_('Is forecast message'), default = False)

    day_index = models.IntegerField(choices = [(i,i) for i in range(7)],
            null = True,
            blank = True
            )

    description = models.CharField(
            max_length = 1000,
            blank = True)

    voice_label = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Voice label'),
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            )

    class Meta:
        verbose_name = _('Voice Service Sub-Element')

    def __str__(self):
        return "Sub-element: %s" % self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

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
            errors.append(ugettext('No VoiceLabel in: "%s"')%str(self))
        return errors


    def get_voice_fragment_url(self, language):
        """
        Returns the url of the audio file of this element, in the given language.
        """
        return self.voice_label.get_voice_fragment_url(language)

    def get_subclass_object(self):
        return VoiceServiceSubElement.objects.get_subclass(id = self.id)


class VoiceServiceElement(VoiceServiceSubElement):
    """
    An element in a voice service (could be Choice, Message, etc.)
    Is accessible through HTTP in a generated VoiceXML
    """
    objects = InheritanceManager()
    _urls_name = "" #This should be the same as in urls.py
    
    class Meta:
        verbose_name = _('Voice Service Element')
    
    def __str__(self):
        return _("Element: %s") % self.name

    def get_absolute_url(self, session):
        """
        Returns the url at which this element is accessible through VoiceXML.
        """
        return reverse(self._urls_name, kwargs= {'element_id':str(self.id), 'session_id':session.id})