from django.http import HttpResponse
from django.shortcuts import render

from vsdk.service_development.models import ChoiceSaved

def results(request):

  yesNoResults = ChoiceSaved.yes_no_objects.all()

  print(ChoiceSaved.objects.all())
  print(ChoiceSaved.yes_no_objects.all())

  context = {
        'yes_no_results': yesNoResults,
  }


  #return HttpResponse(choices)
  return render(request, 'results.html', context=context)