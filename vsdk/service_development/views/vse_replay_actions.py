from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http.response import HttpResponseRedirect

from ..models import *


def replay_actions_get_redirect_url(replay_actions_element, session):
    return replay_actions_element.redirect.get_absolute_url(session)


def replay_actions_generate_context(replay_actions_element,session):
    language = session.language
    redirect_url = replay_actions_get_redirect_url(replay_actions_element,session)

    you_have = replay_actions_element.you_have.get_voice_fragment_url(language)
    created = replay_actions_element.created.get_voice_fragment_url(language)
    updated = replay_actions_element.updated.get_voice_fragment_url(language)
    deleted = replay_actions_element.deleted.get_voice_fragment_url(language)
    advertisements = replay_actions_element.advertisements.get_voice_fragment_url(language)
    an_advertisement = replay_actions_element.an_advertisement.get_voice_fragment_url(language)
    namely = replay_actions_element.namely.get_voice_fragment_url(language)
    made_no_new_changes_to_your_advertisements = replay_actions_element.made_no_new_changes_to_your_advertisements.get_voice_fragment_url(language)
    replay_for = replay_actions_element.replay_for.get_voice_fragment_url(language)
    number = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    replay_action_create = session.replay_action_create
    replay_action_update = session.replay_action_update
    replay_action_delete = session.replay_action_delete
    amount_create = getattr(language, number[int(len(replay_action_create))]).get_voice_fragment_url(language)
    amount_update = getattr(language, number[int(len(replay_action_update))]).get_voice_fragment_url(language)
    amount_delete = getattr(language, number[int(len(replay_action_delete))]).get_voice_fragment_url(language)

    context = {
                'you_have':you_have,
                'created': created,
                'updated': updated,
                'deleted': deleted,
                'advertisements': advertisements,
                'an_advertisement': an_advertisement,
                'replay_for': replay_for,
                'namely': namely,
                'made_no_new_changes_to_your_advertisements': made_no_new_changes_to_your_advertisements,
                'replay_actions': replay_actions,
                'replay_action_create': replay_action_create,
                'replay_action_update': replay_action_update,
                'replay_action_delete': replay_action_delete,
                'amount_create': amount_create,
                'amount_update': amount_update,
                'amount_delete': amount_delete,
                'redirect_url':redirect_url
    }
    return context


def replay_actions(request, element_id, session_id):
    replay_actions_element = get_object_or_404(ReplayActions, pk=element_id)
    voice_service = replay_actions_element.service
    session = lookup_or_create_session(voice_service, session_id)
    session.record_step(replay_actions_element)
    context = replay_actions_generate_context(replay_actions_element, session)
    return render(request, 'replay_actions.xml', context, content_type='text/xml')
