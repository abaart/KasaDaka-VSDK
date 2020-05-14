import glob
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from vsdk.service_development.models import ChoiceSaved

def results(request):

  yesNoResults = ChoiceSaved.yes_no_objects.all()
  test_path = settings.MEDIA_URL + "uploads/*"
  test_path2 = settings.MEDIA_URL + "*"
  test_path3 = settings.MEDIA_URL

  all_raw = ChoiceSaved.objects.all().values()
  print(ChoiceSaved.yes_no_objects.all().values())

  all = []
  for item_raw in all_raw:
    item = item_raw
    item["call_date"] = item["call_date"].timestamp()
    all.append(item)
    print(item)

  obj = {
    "all":all,
    # "ChoiceSaved.yes_no_objects.all().values()": ChoiceSaved.yes_no_objects.all().values()
  }

  context = {
    'yes_no_results': yesNoResults,
    'test_path': glob.glob(test_path),
    'test_path2': glob.glob(test_path2),
    'test_path3': test_path3,
    'dump': json.dumps(obj, indent=2)
  }

  return render(request, 'results.html', context=context)