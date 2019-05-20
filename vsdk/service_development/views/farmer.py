from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect

from ..models import Farmer, Commune, Village, CallSession, Language

from . import base


class FarmerRegistration(TemplateView):

    def resolve_voice_labels(self, items, language):
        """
        Returns a list of voice labels belonging to the provided list of choice_options.
        """
        voice_labels = []
        for item in items:
            voice_labels.append(item.get_voice_fragment_url(language))
        return voice_labels

    def render_farmer_registration_form(self, request, session):
        # This is the redirect URL to POST the language selected
        redirect_url = reverse('service-development:farmer-registration', args=[session.id])

        if session.language is None:
            return base.redirect_add_get_parameters('service-development:language-selection', session.id,
                    redirect_url=redirect_url)

        language = session.language
        communes = Commune.objects.all()
        villages = Village.objects.all()

        context = {
            "redirect_url": redirect_url,
            "language": language,
            'communes': communes,
            'villages': villages,
            'commune_voice_labels':self.resolve_voice_labels(communes, language),
            'village_voice_labels':self.resolve_voice_labels(villages, language),
        }

        return render(request, 'farmer_registration.xml', context, content_type='text/xml')

    def get(self, request, session_id):
        session = get_object_or_404(CallSession, pk=session_id)
        return self.render_farmer_registration_form(request, session)

    def post(self, request, session_id):
        """
        After all required elements of the registration process
        have been filled, this function creates the farmer.
        After registration the farmer is redirected back to the start
        of the voice service.
        """
        if 'commune_id' not in request.POST:
            raise ValueError('Incorrect request, commune not set')
        if 'village_id' not in request.POST:
            raise ValueError('Incorrect request, village not set')

        session = get_object_or_404(CallSession, pk=session_id)
        caller_id = session.caller_id
        commune = request.POST["commune_id"]
        village = request.POST["village_id"]

        farmer = Farmer(caller_id=caller_id, commune=commune, village=village, service=session.service)

        if session.service.registration_language:
            farmer.language = session.language

        farmer.save()

        advertisement = session.advertisement
        advertisement.farmer = farmer
        advertisement.save()

        session.link_to_farmer(farmer)

        session.record_step(None, "Registered as farmer: %s" %str(farmer))

        # Return to start of voice service
        return redirect('service-development:voice-service', voice_service_id = session.service.id, session_id = session.id)
