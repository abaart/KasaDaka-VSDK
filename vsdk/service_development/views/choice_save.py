from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect

from ..models import CallSession, VoiceService, Language

class ChoiceSave(TemplateView):

    def post(self, request, session_id):
        """
        Saves the chosen choice to DB
        """
        
        print("##### hey ho ####")

        if 'redirect_url' in request.POST:
            redirect_url = request.POST['redirect_url']
        else: raise ValueError('Incorrect request, redirect_url not set')
        if 'language_id' not in request.POST:
            raise ValueError('Incorrect request, language ID not set')

        session = get_object_or_404(CallSession, pk = session_id)
        voice_service = session.service
        language = get_object_or_404(Language, pk = request.POST['language_id'])

        session._language = language
        session.save()

        session.record_step(None, "Language selected, %s" % language.name)

        return HttpResponseRedirect(redirect_url)
