from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import VoiceService, KasaDakaUser, lookup_or_create_session, lookup_kasadaka_user_by_caller_id

from .base import *

def get_caller_id_from_GET_request(request):
    if 'caller_id' in request.GET:
        return request.GET['caller_id']
    elif 'callerid' in request.GET:
        return request.GET['callerid']
    return None



def voice_service_start(request, voice_service_id, session_id = None):
    """
    Starting point for a voice service. Looks up user (redirects to registation
    otherwise), creates session, (redirects to language selection).
    If all requirements are fulfilled, redirects to the starting element of the
    voice service.
    """
    voice_service = get_object_or_404(VoiceService, pk=voice_service_id)

    if not voice_service.active:
        # TODO give a nicer error message
        raise Http404()

    caller_id = get_caller_id_from_GET_request(request)
    session = lookup_or_create_session(voice_service, session_id, caller_id)
    
    #If the session is not yet linked to an user, try to look up the user by Caller ID, and link it to the session
    if not session.user:
        found_user = lookup_kasadaka_user_by_caller_id(caller_id, session.service)
        if found_user:
            session.link_to_user(found_user)

        # If there is no user with this caller_id, redirect to registration
        elif caller_id:
            return redirect_add_get_parameters('service-development:user-registration',
                    caller_id = caller_id,
                    session_id = session.id)
        else:
            if voice_service.requires_registration:
                # TODO make this into a nice audio error
                raise ValueError('This service requires registration, but registration is not possible, because there is no callerID!')
        
    # If the language for this session can not be determined,
    # redirect the user to language selection for this session only.
    if not session.language:
        return redirect('service-development:language-selection',
                        voice_service_id = voice_service.id,
                        session_id = session.id)

    return redirect_to_voice_service_element(voice_service.start_element, session)

