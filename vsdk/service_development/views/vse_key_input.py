from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http.response import HttpResponseRedirect

from ..models import *


def key_input_get_redirect_url(key_input_element, session):
    return key_input_element.redirect.get_absolute_url(session)


def key_input_generate_context(key_input_element, session, element_id):
    language = session.language
    key_input_voice_fragment_url = key_input_element.get_voice_fragment_url(language)
    redirect_url = key_input_get_redirect_url(key_input_element, session)
    save_option = getattr(key_input_element, 'save_option')

    # This is the redirect URL to POST the language selected
    redirect_url_POST = reverse('service-development:key-input', args=[element_id, session.id])

    # This is the redirect URL for *AFTER* the language selection process
    pass_on_variables = {
        'redirect_url': redirect_url,
        'save_option': save_option
    }

    context = {
        'voice_label': key_input_voice_fragment_url,
        'redirect_url': redirect_url_POST,
        'pass_on_variables': pass_on_variables
    }

    print("Context: ", context)

    return context


def post(request, session_id):
    """
    Saves the key input to the session
    """
    session = get_object_or_404(CallSession, pk=session_id)
    key_input = request.POST['key_input_value']
    save_option = request.POST['save_option']
    advertisement = Advertisement()
    setattr(advertisement, save_option, key_input)
    advertisement.save()

    session.link_to_advertisement(advertisement)
    session.record_step(None, "Value input, %s" % key_input)


def key_input(request, element_id, session_id):
    print("Request method: ", request.method)

    if request.method == "POST":
        if 'redirect_url' in request.POST:
            redirect_url = request.POST['redirect_url']
        else: raise ValueError('Incorrect request, redirect_url not set')
        if 'key_input_value' not in request.POST:
            raise ValueError('Incorrect request, input value not set')
        if 'save_option' not in request.POST:
            raise ValueError('No save_option was given')

        post(request, session_id)

        return HttpResponseRedirect(redirect_url)

    elif request.method == "GET":
        key_input_element = get_object_or_404(KeyInput, pk=element_id)
        session = get_object_or_404(CallSession, pk=session_id)
        session.record_step(key_input_element)
        context = key_input_generate_context(key_input_element, session, element_id)

        return render(request, 'key_input.xml', context, content_type='text/xml')



