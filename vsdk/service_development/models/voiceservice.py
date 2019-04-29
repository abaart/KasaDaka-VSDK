from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from .voicelabel import VoiceLabel, Language, VoiceFragment
from .vs_element import VoiceServiceElement

class VoiceService(models.Model):
    _urls_name = 'service-development:voice-service'

    name = models.CharField(_('Name'),max_length=100)
    description = models.CharField(_('Description'),max_length=1000)
    creation_date = models.DateTimeField(_('Date created'), auto_now_add = True)
    modification_date = models.DateTimeField(_('Date last modified'), auto_now = True)
    active = models.BooleanField(_('Voice service active'),
            help_text = _("A voice service that is active is accessible to farmers. Marking this service as active (which is only possible when it is valid) will activate this service and disactivate all other services."))
    _start_element = models.ForeignKey(            
            VoiceServiceElement,
            related_name='%(app_label)s_%(class)s_related',
            verbose_name=_('Starting element'),
            null = True,
            on_delete = models.SET_NULL,
            blank = True)
    registration_choices = [('required', _('required (service does not function without Caller ID!)')),
                            ('preferred', _('preferred')),
                            ('disabled', _('disabled'))]
    registration = models.CharField(_('Farmer registration'),max_length = 15, blank = False, choices = registration_choices)
    registration_language = models.BooleanField(_('Register Language preference'), help_text= _("The preferred language will be asked and stored during the farmer registration process"), default = True)
    registration_name = models.BooleanField(_('Register spoken name'), help_text = _("The farmer will be asked to speak their name as part of the farmer registration process"), default = False)

    supported_languages = models.ManyToManyField(Language, blank = True,verbose_name=_('Supported languages'))

    class Meta:
        verbose_name = _('Voice Service')
    
    def get_vxml_url(self):
        try:
            return reverse(self._urls_name, kwargs ={'voice_service_id': self.id})
        except NoReverseMatch:
            return _("unknown")
    get_vxml_url.short_description = _("VoiceXML endpoint URL")
    vxml_url = property(get_vxml_url)

    def _get_start_element(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        return VoiceServiceElement.objects.get_subclass(id = self._start_element.id)
    _get_start_element.short_description = _('Starting element')
    start_element = property(_get_start_element)

    def _supports_single_language(self):
        """
        Returns True if this service supports only a single language
        """
        return len(self.supported_languages.all()) == 1
    _supports_single_language.short_description = _('Supports only a single language')
    supports_single_language = property(_supports_single_language)

    @property
    def registration_required(self):
        "Returns True if farmer registration is required"
        return self.registration == 'required'

    @property
    def registration_preferred_or_required(self):
        "Returns True if farmer registration is preferred or required"
        return (self.registration == 'preferred' or self.registration == 'required')

    @property
    def registration_disabled(self):
        "Returns True if farmer registration is disabled"
        return self.registration == 'disabled'
    
    
    def __str__(self):
        return _('Voice Service: %s') % self.name

    def is_valid(self):
        if not len(self.validator()) == 0:
            return False
        else: return True
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def validator(self):
        errors = []
        if not self._start_element:
            errors.append(ugettext('No starting element'))
        else:
            associated_elements = self.voiceservicesubelement_set.all()
            for sub_element in associated_elements:
                errors.extend(sub_element.get_subclass_object().validator())
        if len(self.supported_languages.all()) == 0:
            errors.append(ugettext('No supported languages'))

        #deduplicate errors
        errors = list(set(errors))
        return errors

