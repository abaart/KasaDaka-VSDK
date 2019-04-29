from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from ..models import Advertisement, CallSession, Language

from . import base


class Advertisement(TemplateView):

    def create_new(self, request, session):
        # TODO: expand function that can add a new advertisment
        advertisement = Advertisement()

        advertisement.save()
        session.link_to_advertisement(advertisement)

        session.record_step(None, "Created new advertisement: %s" %str(advertisement))
        return

    def change_existing(self, request, session, advertisement):
        # TODO: create function that can change a selected advertisment
        return

    def registration_process(self, request, session):
        # TODO: start registration process (if necessary)
        return

    def get(self, request, session_id):
        session = get_object_or_404(CallSession, pk = session_id)
        return self.create_new(request, session)
