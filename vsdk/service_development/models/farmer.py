from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from . import Language
from . import VoiceService

class Farmer(models.Model):
    """
    Farmer that belongs to a Voice Service on this system
    """
    caller_id = models.CharField(_('Phone number'),max_length=100, unique = True)
    #phone_number = PhoneNumberField()
    first_name = models.CharField(_('First name'), max_length = 100, blank = True)
    last_name = models.CharField(_('Last name'), max_length=100, blank = True)
    creation_date = models.DateTimeField(_('Date created'),auto_now_add = True)
    modification_date = models.DateTimeField(_('Date last modified'),auto_now = True)
    language = models.ForeignKey(Language,on_delete = models.SET_NULL, null = True)
    commune = models.CharField(_('Commune'), max_length=100, blank = True)
    village = models.CharField(_('Village'), max_length=100, blank = True)
    service = models.ForeignKey(VoiceService, on_delete = models.CASCADE)

    class Meta:
        verbose_name = _('Farmer')

    def __str__(self):
        if not (self.first_name or self.last_name):
            return "%s" % self.caller_id
        else:
            return "%s %s (%s)" % (self.first_name, self.last_name, self.caller_id)


def lookup_farmer_by_caller_id(caller_id, service):
    """
    If farmer with caller_id for current voice_service exists, returns Farmer object.
    If farmer does not exist or caller_id is None, returns None.
    """
    if caller_id:
        try:
            return Farmer.objects.get(caller_id = caller_id,
                                      service = service)
        except Farmer.DoesNotExist:
            return None
    return None
