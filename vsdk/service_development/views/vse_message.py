from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from vsdk.settings import OWM_API_KEY
from ..models import *
from ..weather_apis import get_apis
from ..location import get_location


def message_presentation_get_redirect_url(message_presentation_element, session):
    if not message_presentation_element.final_element:
        return message_presentation_element.redirect.get_absolute_url(session)
    else:
        return None


def message_presentation_generate_context(message_presentation_element, session):
    language = session.language
    message_voice_fragment_url = message_presentation_element.get_voice_fragment_url(language)
    redirect_url = message_presentation_get_redirect_url(message_presentation_element, session)
    context = {
        'message_voice_fragment_url': message_voice_fragment_url,
        'redirect_url': redirect_url
    }
    return context


def message_presentation_generate_weather_context(message_presentation_element, session):
    
    forecast = get_apis(OWM_API_KEY).get_forecast(get_location())

    language = session.language
    message_voice_fragment_url = message_presentation_element.get_voice_fragment_url(language)
    redirect_url = message_presentation_get_redirect_url(message_presentation_element, session)
    context = {
        'message_voice_fragment_url': message_voice_fragment_url,

        'message_voice_fragment_today_url':
            message_presentation_element.get_voice_fragment_url_day(language, forecast, 0),
        'message_voice_fragment_wind0_url':
            message_presentation_element.get_voice_fragment_url_wind(language, forecast, 0),
        'message_voice_fragment_rain0_url':
            message_presentation_element.get_voice_fragment_url_rain(language, forecast, 0),

        'message_voice_fragment_tomorrow_url':
            message_presentation_element.get_voice_fragment_url_day(language, forecast, 1),
        'message_voice_fragment_wind1_url':
            message_presentation_element.get_voice_fragment_url_wind(language, forecast, 1),
        'message_voice_fragment_rain1_url':
            message_presentation_element.get_voice_fragment_url_rain(language, forecast, 1),

        'message_voice_fragment_day2_url':
            message_presentation_element.get_voice_fragment_url_day(language, forecast, 2),
        'message_voice_fragment_wind2_url':
            message_presentation_element.get_voice_fragment_url_wind(language, forecast, 2),
        'message_voice_fragment_rain2_url':
            message_presentation_element.get_voice_fragment_url_rain(language, forecast, 2),

        'message_voice_fragment_day3_url':
            message_presentation_element.get_voice_fragment_url_day(language, forecast, 3),
        'message_voice_fragment_wind3_url':
            message_presentation_element.get_voice_fragment_url_wind(language, forecast, 3),
        'message_voice_fragment_rain3_url':
            message_presentation_element.get_voice_fragment_url_rain(language, forecast, 3),

        'message_voice_fragment_day4_url':
            message_presentation_element.get_voice_fragment_url_day(language, forecast, 4),
        'message_voice_fragment_wind4_url':
            message_presentation_element.get_voice_fragment_url_wind(language, forecast, 4),
        'message_voice_fragment_rain4_url':
            message_presentation_element.get_voice_fragment_url_rain(language, forecast, 4),

        'message_voice_fragment_day5_url':
            message_presentation_element.get_voice_fragment_url_day(language, forecast, 5),
        'message_voice_fragment_wind5_url':
            message_presentation_element.get_voice_fragment_url_wind(language, forecast, 5),
        'message_voice_fragment_rain5_url':
            message_presentation_element.get_voice_fragment_url_rain(language, forecast, 5),

        'redirect_url': redirect_url
    }
    return context


def message_presentation(request, element_id, session_id):
    message_presentation_element = get_object_or_404(MessagePresentation, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(message_presentation_element)

    if message_presentation_element.is_weather_element:
        context = message_presentation_generate_weather_context(message_presentation_element, session)
        return render(request, 'message_presentation_weather.xml', context, content_type='text/xml')
    else:
        context = message_presentation_generate_context(message_presentation_element, session)
        return render(request, 'message_presentation.xml', context, content_type='text/xml')
