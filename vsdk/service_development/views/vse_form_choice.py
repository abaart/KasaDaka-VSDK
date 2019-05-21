from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.apps import apps
from django.contrib.contenttypes.models import ContentType

from ..models import *


def resolve_redirect_url(choice_element, session):
    return choice_element.redirect.get_absolute_url(session)


def resolve_voice_labels(choice_options, language):
    """
    Returns a list of voice labels belonging to the provided list of choice_options.
    """
    voice_labels = []
    for choice_option in choice_options:
        voice_labels.append(choice_option.get_voice_fragment_url(language))
    return voice_labels


def get_model_from_any_app(model_name):

    for app_config in apps.get_app_configs():
        try:
            model = app_config.get_model(model_name)
            return model
        except LookupError:
            pass
    return None


def choice_generate_context(choice_element, session):
    """
    Returns a dict that can be used to generate the choice VXML template
    choice = this Choice element object
    choice_voice_label = the resolved Voice Label URL for this Choice element
    choice_options = iterable of ChoiceOption object belonging to this Choice element
    choice_options_voice_labels = list of resolved Voice Label URL's referencing to the choice_options in the same position
    choice_options_redirect_urls = list of resolved redirection URL's referencing to the choice_options in the same position
        """
    model_type = choice_element.model_type
    choice_elements = get_model_from_any_app(model_type).objects.all()
    language = session.language

    context = {
        'choice': choice_element,
        'choice_voice_label': choice_element.get_voice_fragment_url(language),
        'choice_options': choice_elements,
        'voice_labels': resolve_voice_labels(choice_elements, language),
        'redirect_url': resolve_redirect_url(choice_element, session),
        'language': language,
    }
    return context


def form_choice(request, element_id, session_id):
    choice_element = get_object_or_404(FormChoice, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(choice_element)
    context = choice_generate_context(choice_element, session)

    return render(request, 'form_choice.xml', context, content_type='text/xml')

