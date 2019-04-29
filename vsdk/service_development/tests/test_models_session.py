import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

from django.test import TestCase
from ..models.session import lookup_or_create_session, CallSession

class TestCallSession(TestCase):
    def setUp(self):
        self.lang = mixer.blend('service_development.Language')
        self.lang2 = mixer.blend('service_development.Language')
        self.lang3 = mixer.blend('service_development.Language')
    
    def test_init(self):
        obj = mixer.blend('service_development.CallSession')
        assert obj.pk == 1

    def test_str(self):
        obj = mixer.blend('service_development.CallSession')
        assert isinstance(str(obj),str)

    def test_get_session_language_user_language(self):
        user = mixer.blend('service_development.KasaDakaUser',
                language = self.lang)
        service = mixer.blend('service_development.VoiceService',
                supported_languages = ())
        obj = mixer.blend('service_development.CallSession',
                user = user,
                service = service)
        assert obj.language == None , 'If user preferred language is not supported by service, language cannot be determined'
        
        service = mixer.blend('service_development.VoiceService',
                supported_languages = (self.lang,self.lang2))
        obj = mixer.blend('service_development.CallSession',
                user = user,
                service = service)
        assert obj.language == obj.user.language , 'Language should be language of user'

    def test_get_session_language_no_voice_service(self):
        obj = mixer.blend('service_development.CallSession', 
                service = None)
        assert obj.language == None , 'Without Service, language cannot be determined'

    def test_get_session_language_service_single_language(self):
        user = mixer.blend('service_development.KasaDakaUser',
                language = self.lang)
        service = mixer.blend('service_development.VoiceService',
                supported_languages = (self.lang2))
        obj = mixer.blend('service_development.CallSession',
                service = service)
        assert obj.language == self.lang2 , 'If service only supports single language, this will be session language.'
        
        obj = mixer.blend('service_development.CallSession',
                user = user,
                service = service)
        assert obj.language == self.lang2 , 'If service only supports single language, this will be session language.'

    def test_get_session_language_service_defined_in_session(self):
        service = mixer.blend('service_development.VoiceService',
                supported_languages = (self.lang2, self.lang3))
        obj = mixer.blend('service_development.CallSession',
                service = service,
                _language = self.lang)
        assert obj.language == None , 'If language in session is not supported by service, language cannot be determined.'

        obj = mixer.blend('service_development.CallSession',
                service = service,
                _language = self.lang2)
        assert obj.language == self.lang2 , 'If language set in session is supported by service, this language will be used.'

    def test_record_step(self):
        session = mixer.blend('service_development.CallSession')
        choice_element = mixer.blend('service_development.Choice')
        session.record_step(choice_element)
        assert session.steps.all()[0].visited_element == choice_element

        
        session = mixer.blend('service_development.CallSession')
        choice_elements = mixer.cycle(11).blend('service_development.Choice')
        message_elements = mixer.cycle(10).blend('service_development.MessagePresentation')
        general_element = mixer.blend('service_development.VoiceServiceElement')
        session.record_step(message_elements[0])

        for element in choice_elements:
            session.record_step(element)
            session.record_step(general_element)
        
        step_visted_elements = []
        for step in session.steps.all():
            step_visted_elements.append(step.visited_element)
        for element in choice_elements:
            assert element in step_visted_elements

        assert message_elements[0] in step_visted_elements
        assert general_element in step_visted_elements
        
        count = 0
        for element in step_visted_elements:
            if element == general_element:
                count += 1
        assert count == 11
        assert session.steps.all()[5].session == session

    def test_link_to_user(self):
        session = mixer.blend('service_development.CallSession',
                user=None)
        assert session.user == None
        user = mixer.blend('service_development.KasaDakaUser')
        session.link_to_farmer(user)
        assert session.user == user

class TestCallSessionStep:

    def test_init(self):
        obj = mixer.blend('service_development.CallSessionStep')
        assert obj.pk == 1

    def test_str(self):
        obj = mixer.blend('service_development.CallSessionStep')
        assert isinstance(str(obj),str)

def test_lookup_or_create_session():
        session = mixer.blend('service_development.CallSession')
        assert lookup_or_create_session(None, session.id)== session
        assert isinstance(lookup_or_create_session(None,None), CallSession)
        vs = mixer.blend('service_development.VoiceService')
        assert lookup_or_create_session(vs, None).service == vs

    


