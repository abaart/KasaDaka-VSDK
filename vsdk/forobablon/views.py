from django.http import HttpResponse
from django.shortcuts import render

from vsdk.service_development.models import ChoiceSaved

def results(request):

  choices = ChoiceSaved.day_objects.all()

  print(ChoiceSaved.objects.all())
  print(ChoiceSaved.day_objects.all())

  context = {
        'results': choices,
  }

  #return HttpResponse(choices)
  return render(request, 'results.html', context=context)