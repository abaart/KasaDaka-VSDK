from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from ..models import Farmer, CallSession

from . import base


class FarmerRegistration(TemplateView):

    def create_new(self, request, session):
        farmer = Farmer(caller_id = session.caller_id)

        if session.service.registration_language:
            farmer.language = session.language

        farmer.save()
        session.link_to_farmer(farmer)

        session.record_step(None, "Registered as farmer: %s" %str(farmer))
        return

    def registration_process(self, request, session):
        # Always redirect back to registration process
        redirect_url = reverse('service-development:farmer-registration', args =[session.id])

        if session.service.registration_language and session.language is None:
            return base.redirect_add_get_parameters(
                'service-development:language-selection',
                session.id,
                redirect_url=redirect_url
            )

        #TODO: dit verder uitwerken, user bestaat natuurlijk nog niet dus daar kun je niet checken.
        #if 'name' in session.service.registration_elements and session.user.name_voice == None:
            # go to user name voice prompt
        #    pass

        # If all required elements are present, finalize registration by creating a new user
        self.create_new(request, session)

        # Return to start of voice service
        return redirect('service-development:voice-service', voice_service_id = session.service.id, session_id = session.id)

    def get(self, request, session_id):
        session = get_object_or_404(CallSession, pk = session_id)
        return self.registration_process(request, session)
