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

def choice_generate_context(choice_element, session):
    """
    Returns a dict that can be used to generate the choice VXML template
    choice = this Choice element object
    choice_voice_label = the resolved Voice Label URL for this Choice element
    choice_options = iterable of ChoiceOption object belonging to this Choice element
    choice_options_voice_labels = list of resolved Voice Label URL's referencing to the choice_options in the same position
    choice_options_redirect_urls = list of resolved redirection URL's referencing to the choice_options in the same position
        """
    choice_options =  choice_element.choice_options.all()
    language = session.language
    context = {'choice':choice_element,
                'choice_voice_label':choice_element.get_voice_fragment_url(language),
                'choice_options': choice_options,
                'choice_options_voice_labels':choice_options_resolve_voice_labels(choice_options, language),
                    'choice_options_redirect_urls': choice_options_resolve_redirect_urls(choice_options,session),
                    'language': language,
                    }
    return context

def choice(request, element_id, session_id):
    choice_element = get_object_or_404(Choice, pk=element_id)
    voice_service = choice_element.service
    session = lookup_or_create_session(voice_service, session_id)

    if request.method == "POST":
        value = request.POST['field1']

        value = list(choice_element.choice_options.all())[int(value) -1].name


        result = Result()

        result.session = session
        result.name = choice_element.description
        result.value = value

        result.save()

        if choice_element.map_to_call_session_property in vars(session).keys():
            setattr(session, choice_element.map_to_call_session_property, value)
            session.save()

        # redirect to next element
        return redirect(request.POST['redirect'])

    session.record_step(choice_element)
    context = choice_generate_context(choice_element, session)

    context['url'] = request.get_full_path(False)
    
    return render(request, 'choice.xml', context, content_type='text/xml')

