import glob
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from vsdk.service_development.models import ChoiceSaved, CallSession, SpokenUserInput, SpokenUserInput

class Statistics:
  def __init__(self):
    self._options = {}

  def register_option(self, name: str):
    if name not in self._options:
      self._options[name] = 0

    self._options[name] += 1

  @property
  def __dict__(self):
    return {
      "options": list(self._options.keys()),
      "results": list(self._options.values()),
    }


class Result:
  def __init__(self, session_id, phone_number: str, start_time: str, end_time: str):
    self.session_id = session_id
    self.phone_number = phone_number
    self.start_time = start_time
    self.end_time = end_time
    self.language = None
    self.answer = None
    self.audio_file_player = ""
  
  def add_answer(self, answer: ChoiceSaved):
    if self.language is None:
      self.language = str(answer)
      return

    self.answer = str(answer)
  
  @property
  def finished(self) -> bool:
    return self.language is not None and self.answer is not None


def _get_results():
  result_object = {}
  all_sessions = CallSession.objects.all().order_by("pk")

  for session in all_sessions:
    start = "-"
    end = "-"
    if session.start is not None: start = session.start.isoformat()
    if session.end is not None: end = session.end.isoformat()
    result_object[session.id] = Result(session.pk, session.caller_id, start, end)

  choices = ChoiceSaved.objects.filter(session_id__in = list(result_object.keys())).order_by("pk")
  for choice in choices:
    result_object[choice.session_id].add_answer(choice.choice)


  sui = SpokenUserInput.objects.filter(session_id__in = list(result_object.keys()))
  for input_element in sui:
    input_element = input_element # type: SpokenUserInput
    result_object[input_element.session_id].audio_file_player = input_element.audio_file_player()

  obj = []
  for k in result_object:
    obj.append(result_object[k])
  return obj


def results(request):
  obj = _get_results()
  languages = Statistics()
  options = Statistics()

  for item in obj:
    languages.register_option(item.language)
    options.register_option(item.answer)

  yesNoResults = ChoiceSaved.yes_no_objects.all()
  test_path = settings.MEDIA_URL + "uploads/*"
  test_path2 = settings.MEDIA_URL + "*"
  test_path3 = settings.MEDIA_URL

  context = {
    'yes_no_results': yesNoResults,
    'test_path': glob.glob(test_path),
    'test_path2': glob.glob(test_path2),
    'test_path3': test_path3,
    'dump': reversed(obj),
    "stats_language": json.dumps(languages.__dict__),
    "stats_options": json.dumps(options.__dict__),
  }

  return render(request, 'results.html', context=context)