from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect

from ..models import CallSession, VoiceService, Language

class LanguageSelection(TemplateView):

    def render_language_selection_form(self, request, session, redirect_url):
        languages = session.service.supported_languages.all()

        # This is the redirect URL to POST the language selected
        redirect_url_POST = reverse('service-development:language-selection', args = [session.id])

        # This is the redirect URL for *AFTER* the language selection process
        pass_on_variables = {'redirect_url' : redirect_url}

        context = {'languages' : languages,
                   'redirect_url' : redirect_url_POST,
                   'pass_on_variables' : pass_on_variables
                   }
        return render(request, 'language_selection.xml', context, content_type='text/xml')

    def get(self, request, session_id):
        """
        Asks the user to select one of the supported languages.
        """
        session = get_object_or_404(CallSession, pk = session_id)
        voice_service = session.service
        if 'redirect_url' in request.GET:
            redirect_url = request.GET['redirect_url']
        return self.render_language_selection_form(request, session, redirect_url)

    def post(self, request, session_id):
        """
        Saves the chosen language to the session
        """

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
