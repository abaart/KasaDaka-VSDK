from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import Language
from . import VoiceService


class Farmer(models.Model):
    caller_id = models.CharField(_('Phone number'),max_length=100, unique = True)
    name = models.CharField(_('Name'), max_length = 100, blank = True)
    creation_date = models.DateTimeField(_('Date created'),auto_now_add = True)
    modification_date = models.DateTimeField(_('Date last modified'),auto_now = True)
    language = models.ForeignKey(Language,on_delete = models.SET_NULL, null = True)
    region = models.CharField(_('Region'), max_length = 100, blank = True)
    place = models.CharField(_('Place'), max_length = 100, blank = True)
    service = models.ForeignKey(VoiceService, on_delete = models.CASCADE)

    class Meta:
        verbose_name = _('Farmer')

    def __str__(self):
        if not (self.name):
            return "%s" % self.caller_id
        else:
            return "%s (%s)" % (self.name, self.caller_id)

def lookup_famer_by_caller_id(caller_id, service):
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
