from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *


def choice_options_resolve_redirect_urls(choice_options, session):
    choice_options_redirection_urls = []
    for choice_option in choice_options:
        redirect_url = choice_option.redirect.get_absolute_url(session)
        choice_options_redirection_urls.append(redirect_url)
    return choice_options_redirection_urls

def choice_options_resolve_voice_labels(choice_options, language):
    """
    Returns a list of voice labels belonging to the provided list of choice_options.
    """
    choice_options_voice_labels = []
    for choice_option in choice_options:
        choice_options_voice_labels.append(choice_option.get_voice_fragment_url(language))
    return choice_options_voice_labels

def choice_generate_context(choice_element, element_id, session):
    """
    Returns a dict that can be used to generate the choice VXML template
    choice = this Choice element object
    choice_voice_label = the resolved Voice Label URL for this Choice element
    choice_options = iterable of ChoiceOption object belonging to this Choice element
    choice_options_voice_labels = list of resolved Voice Label URL's referencing to the choice_options in the same position
    choice_options_redirect_urls = list of resolved redirection URL's referencing to the choice_options in the same position
        """
    choice_options = choice_element.choice_options.all()
    language = session.language
    context = {
        'choice':choice_element,
        'choice_voice_label':choice_element.get_voice_fragment_url(language),
        'choice_options': choice_options,
        'choice_options_voice_labels':choice_options_resolve_voice_labels(choice_options, language),
        'choice_options_redirect_urls': choice_options_resolve_redirect_urls(choice_options,session),
        'language': language,
        'removable': choice_element.action == "remove",
        'redirect_url': reverse('service-development:choice', args=[element_id, session.id])
    }
    return context


def post(request, session):
    Advertisement.objects.filter(farmer=session.farmer, seed=session.advertisement.seed).delete()
    CallSession.objects.filter(id=session.id).update(advertisement=None)


def choice(request, element_id, session_id):
    if request.method == "POST":
        session = get_object_or_404(CallSession, pk=session_id)
        
        if 'redirect_url' in request.POST:
            redirect_url = request.POST['redirect_url']
        else: raise ValueError('Incorrect request, redirect_url not set')
        if 'option_id' not in request.POST:
            raise ValueError('Incorrect request, no option selected')
        if 'action' not in request.POST:
            raise ValueError('No action defined')

        post(request, session)

        return HttpResponseRedirect(redirect_url)

    elif request.method == "GET":
        choice_element = get_object_or_404(Choice, pk=element_id)
        session = get_object_or_404(CallSession, pk=session_id)
        session.record_step(choice_element)
        context = choice_generate_context(choice_element, element_id, session)

        return render(request, 'choice.xml', context, content_type='text/xml')

