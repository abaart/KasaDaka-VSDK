from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from ..models import Seed, CallSession

class Seed(TemplateView):
    def registration_process(self, request, session):
        redirect_url = reverse('service-development:user-registration', args =[session.id])
        return

    def get(self, request, session_id):
        session = get_object_or_404(CallSession, pk=session_id)
        return request, session
