import glob
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from vsdk.service_development.models import ChoiceSaved, CallSession
class SessionAnswers:
  def __init__(self, session_id):
    self.session_id = session_id
    self._anwsers = []

  def add_answer(self, answer: ChoiceSaved):
    self._anwsers.append(answer)
  
  def get_language(self) -> ChoiceSaved:
    return self._anwsers[0]

  def get_selection(self) -> ChoiceSaved:
    return self._anwsers[1]

  def finished_session(self) -> bool:
    return len(self._anwsers) >= 2

  def __dict__(self):
    res = {
      "session_id": self.session_id,
      "finished": self.finished_session(),
      "language": None,
      "selection": None,
    }
    if len(self._anwsers) > 0:
      res["language"] = str(self._anwsers[0])

    if len(self._anwsers) > 1:
      res["selection"] = str(self._anwsers[1])

    return res

def results(request):

  yesNoResults = ChoiceSaved.yes_no_objects.all()
  test_path = settings.MEDIA_URL + "uploads/*"
  test_path2 = settings.MEDIA_URL + "*"
  test_path3 = settings.MEDIA_URL

  all_raw = ChoiceSaved.objects.all()
  # all_raw = CallSession.objects.all().values()
  
  print(ChoiceSaved.yes_no_objects.all().values())

  all = {}
  for item in all_raw:
    if item.session_id not in all:
      all[item.session_id] = SessionAnswers(item.session_id)
    
    all[item.session_id].add_answer(item)

  obj = {
    "all": all,
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