from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect
from django.utils import timezone

from ..models import ChoiceSaved

class ChoiceSave(TemplateView):

    def post(self, request, session_id):
        """
        Saves selected choice to DB
        """
        if 'selected_choice_url' not in request.POST:
            raise ValueError('Incorrect request, selected_choice_url not set')
        choice_url = request.POST['selected_choice_url']

        if 'selected_choice_name' not in request.POST:
            raise ValueError('Incorrect request, selected_choice_name not set')
        choice_name = request.POST['selected_choice_name']

        choice = ChoiceSaved(call_date = timezone.now(), choice = choice_name)
        choice.save()

        print(choice_url)
        print(choice_name)


        

        return HttpResponseRedirect(choice_url)
