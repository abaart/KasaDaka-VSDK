from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *


def key_input_get_redirect_url(key_input_element, session):
    if not key_input_element.final_element:
        return key_input_element.redirect.get_absolute_url(session)
    else:
        return None


def key_input_generate_context(key_input_element, session):
    language = session.language
    key_input_voice_fragment_url = key_input_element.get_voice_fragment_url(language)
    redirect_url = key_input_get_redirect_url(key_input_element, session)
    context = {'voice_label': key_input_voice_fragment_url,
               'redirect_url': redirect_url}
    return context


def key_input(request, element_id, session_id):
    key_input_element = get_object_or_404(KeyInput, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(key_input_element)
    context = key_input_generate_context(key_input_element, session)

    return render(request, 'key_input.xml', context, content_type='text/xml')

