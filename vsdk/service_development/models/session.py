from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from . import KasaDakaUser
from . import VoiceService, VoiceServiceElement
from . import Language

class CallSession(models.Model):
    start = models.DateTimeField(auto_now_add = True)
    #TODO: make some kind of handler when the Asterisk connection is closed, to officially end the session.
    end = models.DateTimeField(null = True, blank = True)
    user = models.ForeignKey(KasaDakaUser, on_delete = models.SET_NULL, null = True, blank = True)
    caller_id = models.CharField(max_length = 100, blank = True, null = True)
    service = models.ForeignKey(VoiceService, on_delete = models.SET_NULL, null = True)
    _language = models.ForeignKey(Language,on_delete = models.SET_NULL, null = True)


    def __str__(self):
        from django.template import defaultfilters
        start_date = defaultfilters.date(self.start, "SHORT_DATE_FORMAT")
        start_time = defaultfilters.time(self.start, "TIME_FORMAT")
        return "%s (%s %s)" % (str(self.user), str(start_date), str(start_time))

    @property
    def language(self):
        """
        Tries to determine the language of the session, taking into account
        the voice service, user preferences and possibly an already set language
        for the session. 
        Returns a determined to be valid Language for the Session.
        Returns None if the language cannot be determined.
        """
        if self.service:
            if self.service.supports_single_language:
                self._language = self.service.supported_languages.all()[0]
            elif self.user and self.user.language in self.service.supported_languages.all(): 
                    self._language = self.user.language
            elif self._language and not self._language in self.service.supported_languages.all():
                    self._language = None
        else:
            self._language = None
        
        self.save()
        return self._language
    
    def record_step(self, element):
        step = CallSessionStep(session = self, _visited_element = element)
        self.end = timezone.now() 
        self.save()
        step.save()
        return

    def link_to_user(self, user):
        self.user = user
        self.save()
        return self

class CallSessionStep(models.Model):
    time = models.DateTimeField(auto_now_add = True)
    session = models.ForeignKey(CallSession, on_delete = models.CASCADE, related_name = "steps")
    _visited_element = models.ForeignKey(VoiceServiceElement, on_delete = models.SET_NULL, null = True)

    def __str__(self):
        from django.template import defaultfilters
        date = defaultfilters.date(self.time, "SHORT_DATE_FORMAT")
        time = defaultfilters.time(self.time, "TIME_FORMAT")
        datetime = date + " " + time
        return "%s: @ %s -> %s" % (str(self.session), str(datetime), str(self.visited_element))

    @property
    def visited_element(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        return VoiceServiceElement.objects.get_subclass(id = self._visited_element.id)


class EndUserCallSession(CallSession):

    category = models.CharField(max_length=100, blank=True, null=True)
    listened = models.BooleanField(blank=True, default=False)


class JournalistCallSession(CallSession):

    last_session = models.ForeignKey(EndUserCallSession, on_delete=models.SET_NULL, null=True)

def lookup_or_create_session(voice_service, session_id=None, caller_id = None):

    if voice_service.radio_journalist_service:
        if session_id:
            if session_id:
                session = get_object_or_404(JournalistCallSession, pk=session_id)
                return session
        else:
            session = JournalistCallSession.objects.create(
                service=voice_service,
                caller_id=caller_id)
            session.save()
            return session

    if voice_service.end_user_service:
        if session_id:
            if session_id:
                session = get_object_or_404(EndUserCallSession, pk=session_id)
                return session
        else:
            session = EndUserCallSession.objects.create(
                service=voice_service,
                caller_id=caller_id)
            session.save()
            return session
    else:
        if session_id:
            session = get_object_or_404(CallSession, pk = session_id)
            return session
        else:
            session = CallSession.objects.create(
                    service = voice_service,
                    caller_id = caller_id)
            session.save()
            return session