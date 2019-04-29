from xml.etree import ElementTree as ET

import mock

from django.test.utils import setup_test_environment
from django.test import Client, TestCase
from django.urls import reverse
from django.core.files import File
from django.core.files.storage import Storage

from ..views import farmer
from ..models import KasaDakaUser, CallSession, CallSessionStep
from ..models import VoiceService
from ..models import Language, VoiceLabel, VoiceFragment

from .helpers import create_sample_voice_service

class TestUserRegistration(TestCase):
#    setup_test_environment()
    client = Client()
    user_registration_form_url = reverse('service-development:user-registration') 
    caller_id = "123"
    
    def setUp(self):
        create_sample_voice_service(self) 

    def test_user_registration_invalid_request(self):
        #empty request should raise error
        self.assertRaises(ValueError, self.client.get, self.user_registration_form_url)

    def test_user_registration_get_request(self):
        response = self.client.get(self.user_registration_form_url,
                {'caller_id' : self.caller_id,
                    'session_id' : self.session.id})
        assert response.status_code == 200
        #TODO
        #assert response.context == ""
        assert ET.fromstring(response.content), 'Should produce valid XML'



    def test_user_registration_post_request(self):
        number_of_users_pre = len(KasaDakaUser.objects.all())

        response = self.client.post(
                self.user_registration_form_url,
                {
                    'caller_id': self.caller_id,
                    'session_id': self.session.id,
                    'language_id': self.language.id}
                )

        #user should be created and redirected
        assert response.status_code == 302

        assert len(KasaDakaUser.objects.all()) == number_of_users_pre + 1 , 'Number of users should be one greater than before registration.'

        assert KasaDakaUser.objects.all().filter(caller_id = self.caller_id, service = self.voice_service).order_by('-creation_date')[0].service == self.voice_service


