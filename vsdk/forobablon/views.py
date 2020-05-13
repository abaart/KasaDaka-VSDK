from django.http import HttpResponse

from vsdk.service_development.models import ChoiceSaved

def results(request):

  choices = ChoiceSaved.day_objects.all()

  print(ChoiceSaved.objects.all())
  print(ChoiceSaved.day_objects.all())

  return HttpResponse(choices)