from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *


def resolve_choice_options(choice_options, session):
    options = []
    for choice_option in choice_options:
        items = {}
        items['voice_label'] = choice_option.get_voice_fragment_url(session.language)
        items['redirect_url'] = choice_option.redirect.get_absolute_url(session)
        items['removable'] = choice_option.action == "remove"
        options.append(items)
    return options


def choice_generate_context(choice_element, element_id, session):
    """
    Returns a dict that can be used to generate the choice VXML template
    choice = this Choice element object
    choice_voice_label = the resolved Voice Label URL for this Choice element
    choice_options = iterable of ChoiceOption object belonging to this Choice element
    choice_options_voice_labels = list of resolved Voice Label URL's referencing to the choice_options in the same position
    choice_options_redirect_urls = list of resolved redirection URL's referencing to the choice_options in the same position
        """

    choice_options = resolve_choice_options(choice_element.choice_options.all(), session)
    language = session.language
    context = {
        'choice':choice_element,
        'choice_voice_label':choice_element.get_voice_fragment_url(language),
        'choice_options': choice_options,
        'language': language,
        'redirect_url': reverse('service-development:choice', args=[element_id, session.id])
    }
    return context


def post(request, session):
    advertisement = Advertisement.objects.filter(farmer=session.farmer, seed=session.advertisement.seed)
    session.replay_action_remove.add(advertisement)
    advertisement.delete()
    CallSession.objects.filter(id=session.id).update(advertisement=None)


def choice(request, element_id, session_id):
    if request.method == "POST":
        session = get_object_or_404(CallSession, pk=session_id)

        if 'redirect_url' in request.POST:
            redirect_url = request.POST['redirect_url']
        else: raise ValueError('Incorrect request, redirect_url not set')

        post(request, session)

        return HttpResponseRedirect(redirect_url)

    elif request.method == "GET":
        choice_element = get_object_or_404(Choice, pk=element_id)
        session = get_object_or_404(CallSession, pk=session_id)
        session.record_step(choice_element)
        context = choice_generate_context(choice_element, element_id, session)

        return render(request, 'choice.xml', context, content_type='text/xml')

