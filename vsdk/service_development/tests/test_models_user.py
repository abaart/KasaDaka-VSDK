import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

from ..models.farmer import lookup_farmer_by_caller_id


class TestKasaDakaUser:
    caller_id = "+1234"
    first_name = "henk"
    last_name = "ernia"
    
    def test_init(self):
        obj = mixer.blend('service_development.KasaDakaUser')
        assert obj.pk == 1, 'Should save an instance'
    
    def test_str(self):
        obj = mixer.blend('service_development.KasaDakaUser',
                caller_id = self.caller_id,
                first_name = "",
                last_name = "")
        assert str(obj) == self.caller_id 
        obj = mixer.blend('service_development.KasaDakaUser',
                caller_id = self.caller_id,
                first_name = self.first_name,
                last_name = self.last_name
                )
        assert str(obj) == self.first_name + " " + self.last_name  + " (" + self.caller_id + ")"

    def test_lookup_by_caller_id(self):

        
        assert lookup_farmer_by_caller_id("1", "1") == None
        
        service = mixer.blend('service_development.VoiceService')
        user = mixer.blend('service_development.KasaDakaUser',
                caller_id = self.caller_id,
                first_name = "",
                last_name = "",
                service = service)
        assert lookup_farmer_by_caller_id(self.caller_id, service) == user
        assert lookup_farmer_by_caller_id(None, None) == None
        assert lookup_farmer_by_caller_id("1", None) == None
        assert lookup_farmer_by_caller_id(None, service) == None
        

