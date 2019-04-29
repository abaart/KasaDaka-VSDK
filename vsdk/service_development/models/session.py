from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from . import Farmer
from . import VoiceService, VoiceServiceElement
from . import Language

class CallSession(models.Model):
    start = models.DateTimeField(_('Starting time'),auto_now_add = True)
    #TODO: make some kind of handler when the Asterisk connection is closed, to officially end the session.
    end = models.DateTimeField(_('Ending time'),null = True, blank = True)
    farmer = models.ForeignKey(Farmer, on_delete = models.SET_NULL, null = True, blank = True)
    caller_id = models.CharField(_('Caller ID'),max_length = 100, blank = True, null = True)
    service = models.ForeignKey(VoiceService, on_delete = models.SET_NULL, null = True)
    _language = models.ForeignKey(Language,on_delete = models.SET_NULL, null = True)

    class Meta:
        verbose_name = _('Call Session')

    def __str__(self):
        from django.template import defaultfilters
        start_date = defaultfilters.date(self.start, "SHORT_DATE_FORMAT")
        start_time = defaultfilters.time(self.start, "TIME_FORMAT")
        if self.farmer:
            return "%s (%s %s)" % (str(self.farmer), str(start_date), str(start_time))
        else:
            return "%s (%s %s)" % (str(self.caller_id), str(start_date), str(start_time))

    @property
    def language(self):
        """
        Tries to determine the language of the session, taking into account
        the voice service, farmer preferences and possibly an already set language
        for the session. 
        Returns a determined to be valid Language for the Session.
        Returns None if the language cannot be determined.
        """
        if self.service:
            if self.service.supports_single_language:
                self._language = self.service.supported_languages.all()[0]
            elif self.farmer and self.farmer.language in self.service.supported_languages.all():
                    self._language = self.farmer.language
            elif self._language and not self._language in self.service.supported_languages.all():
                    self._language = None
        else:
            self._language = None
        
        self.save()
        return self._language
    
    def record_step(self, element = None, description = None):
        step = CallSessionStep(session = self, _visited_element = element, description = description)
        self.end = timezone.now() 
        self.save()
        step.save()
        return

    def link_to_farmer(self, farmer):
        self.farmer = farmer
        self.save()
        return self

class CallSessionStep(models.Model):
    time = models.DateTimeField(_('Time'),auto_now_add = True)
    session = models.ForeignKey(CallSession, on_delete = models.CASCADE, related_name = "steps")
    _visited_element = models.ForeignKey(VoiceServiceElement, on_delete = models.SET_NULL, null = True)
    description = models.CharField(_('Description'),max_length = 1000,blank = True, null = True)
    class Meta:
        verbose_name = _('Call Session Step')

    def __str__(self):
        from django.template import defaultfilters
        date = defaultfilters.date(self.time, "SHORT_DATE_FORMAT")
        time = defaultfilters.time(self.time, "TIME_FORMAT")
        datetime = date + " " + time
        if self.visited_element:
            return "%s: @ %s -> %s" % (str(self.session), str(datetime), str(self.visited_element))
        elif self.description:
            return "%s: @ %s -> %s" % (str(self.session), str(datetime), str(self.description))
        else:
            return "%s: @ %s" % (str(self.session), str(datetime))

    @property
    def visited_element(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        if self._visited_element:
            return VoiceServiceElement.objects.get_subclass(id = self._visited_element.id)
        else: return None


def lookup_or_create_session(voice_service, session_id=None, caller_id = None):
    if session_id:
        session = get_object_or_404(CallSession, pk = session_id)
    else:
        session = CallSession.objects.create(
                service = voice_service,
                caller_id = caller_id) 
        session.save()
    return session
