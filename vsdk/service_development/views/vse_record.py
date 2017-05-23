from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *


def record_get_redirect_url(record_element, session):
    return record_element.redirect.get_absolute_url(session)

def record_generate_context(record_element, session):
    language = session.language
    redirect_url = record_get_redirect_url(record_element, session)


    voice_label = record_element.voice_label.get_voice_fragment_url(language)
    ask_confirmation_voice_label = record_element.ask_confirmation_voice_label.get_voice_fragment_url(language)
    repeat_voice_label = record_element.repeat_voice_label.get_voice_fragment_url(language)
    final_voice_label = record_element.final_voice_label.get_voice_fragment_url(language)
    did_not_hear_voice_label = record_element.not_heard_voice_label.get_voice_fragment_url(language)


    context = {'record': record_element,
               'redirect_url': redirect_url,
               'voice_label' : voice_label,
               'ask_confirmation_voice_label' : ask_confirmation_voice_label,
               'repeat_voice_label' : repeat_voice_label ,
               'final_voice_label' : final_voice_label,
               'did_not_hear_voice_label' : did_not_hear_voice_label

               }

    return context


def record(request, element_id, session_id):
    record_element = get_object_or_404(Record, pk=element_id)
    voice_service = record_element.service
    session = lookup_or_create_session(voice_service, session_id)


    if request.method == "POST":
        session = get_object_or_404(CallSession, pk=session_id)

        value = 'audio file'

        result = Result()

        result.session = session
        result.name = record_element.description
        result.value = value

        result.file = request.FILES['recording']
        result.file.name = 'recording_%s_%s.wav' % (session_id, element_id)

        result.save()

        if record_element.map_to_call_session_property in vars(session).keys():
            setattr(session, record_element.map_to_call_session_property, value)

        # redirect to next element
        return redirect(request.POST['redirect'])


    session.record_step(record_element)
    context = record_generate_context(record_element, session)

    context['url'] = request.get_full_path(False)

    return render(request, 'record.xml', context, content_type='text/xml')

