import json

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.utils.dateparse import parse_date

from vsdk.service_development.models import ChoiceSaved, CallSession, SpokenUserInput


def results(request, date):

  yesNoResults = ChoiceSaved.yes_no_objects.all().filter(call_date__date=date)

  sessionIds = set(baz.session.id for baz in ChoiceSaved.objects.all().filter(call_date__date=date))
  sui = SpokenUserInput.objects.filter(session_id__in = sessionIds)

  yes_count = 0
  no_count = 0
  for result in yesNoResults:
    if result['choice'] == 'Yes':
      yes_count = result['count']
    elif result['choice'] == 'No':
      no_count = result['count']
  total_count = yes_count + no_count

  context = {
    'poll_date': parse_date(date),
    'yes_count': yes_count,
    'no_count': no_count,
    'total_count': total_count,
    'recordings': sui,
  }

  if total_count > 0:
    context['yes_percentage'] = yes_count * 100 / total_count
    context['no_percentage'] = no_count * 100 / total_count

  return render(request, 'results.html', context=context)



def resultsIndex(request):

  context = {
    'yes_no_results': ChoiceSaved.yes_no_objects.all().order_by('-call_date'),
  }

  return render(request, 'results-index.html', context=context)

