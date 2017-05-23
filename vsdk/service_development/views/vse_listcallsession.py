from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *


def list_call_session_element_get_redirect_url(list_call_session_element, session):
    return list_call_session_element.redirect.get_absolute_url(session)

def list_call_session_element_generate_context(list_call_session_element, session_to_list, session):
    language = session.language
    redirect_url = list_call_session_element_get_redirect_url(list_call_session_element, session)

    name_voice_label = list_call_session_element.name_voice_label.get_voice_fragment_url(language)
    category_voice_label = list_call_session_element.category_voice_label.get_voice_fragment_url(language)
    message_voice_label = list_call_session_element.message_voice_label.get_voice_fragment_url(language)


    name = ''
    message = ''
    category = ''

    #TODO : The name of each value is a hardcoded value, should be changed to a more dynamic solution
    if Result.objects.filter(session = session_to_list, name = 'Record name').exists():
        name = Result.objects.filter(session = session_to_list, name = 'Record name').first().file.url
    if Result.objects.filter(session=session_to_list, name='Record name').exists():
        message = Result.objects.filter(session=session_to_list, name='Record Village DB').first().file.url
    if Result.objects.filter(session=session_to_list, name='Record name').exists():
        category = Result.objects.filter(session=session_to_list, name='Record message').first().file.url

    context = {'list_call_session_element': list_call_session_element,
               'redirect_url': redirect_url,
               'name_voice_label' : name_voice_label,
               'category_voice_label' : category_voice_label,
               'message_voice_label' : message_voice_label ,
               'name' : name,
               'message' : message,
               'category' : category,
               }

    return context


def list_call_session(request, element_id, session_id):

    list_call_session_element = get_object_or_404(ListCallSessions, pk=element_id)

    empty_redirect = VoiceServiceElement.objects.get_subclass(id=list_call_session_element.empty_redirect.id)

    session = get_object_or_404(JournalistCallSession, pk=session_id)

    service_to_list_sessions_from = list_call_session_element.list_sessions_from_service

    if not EndUserCallSession.objects.filter(listened=False, service = service_to_list_sessions_from).exists():
        return redirect(empty_redirect.get_absolute_url(session))

    session_to_list = EndUserCallSession.objects.filter(listened=False, service = service_to_list_sessions_from).order_by('start').first()
    session_to_list.listened = True
    session_to_list.save()

    session.record_step(list_call_session_element)
    context = list_call_session_element_generate_context(list_call_session_element, session_to_list, session)

    context['url'] = request.get_full_path(False)

    return render(request, 'list_call_session.xml', context, content_type='text/xml')

