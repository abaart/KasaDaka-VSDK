from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from django.utils import timezone
from . import CallSession, VoiceService


class FarmerInputCategory(models.Model):
    name = models.CharField(_('Name'),max_length = 100, blank = False, null = False)
    description = models.CharField(_('Description'),max_length = 1000, blank = True, null = True)
    service = models.ForeignKey(VoiceService, on_delete=models.CASCADE, related_name="service", verbose_name = _('Voice service'))

    class Meta:
        verbose_name = _('Farmer Input Category')

    def __str__(self):
        return '"%s" ("%s")'%(self.name, self.service.name)

class SpokenFarmerInput(models.Model):
    #value = models.CharField(max_length = 100, blank = True, null = True)
    audio = models.FileField(_('Audio file'),upload_to='uploads/', blank=False, null= False)
    time = models.DateTimeField(_('Time'),auto_now_add = True)
    session = models.ForeignKey(CallSession, on_delete=models.CASCADE, related_name="session")
    category = models.ForeignKey(FarmerInputCategory, on_delete=models.CASCADE, related_name="category", verbose_name = _('Category'))
    description = models.CharField(max_length = 1000, blank = True, null = True, verbose_name = _('Description'))


    class Meta:
        verbose_name = _('Spoken Farmer Input')

    def __str__(self):
        from django.template import defaultfilters
        date = defaultfilters.date(self.time, "SHORT_DATE_FORMAT")
        time = defaultfilters.time(self.time, "TIME_FORMAT")
        return _('Spoken Farmer Input: %(category_name)s @ %(date)s %(time)s by %(caller_id)s (%(service_name)s)') %{'category_name' : self.category.name, 'date' : str(date), 'time' : str(time), 'caller_id' : str(self.session.caller_id), 'service_name' : self.session.service.name}


    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio:
            file_url = settings.MEDIA_URL + str(self.audio)
            player_string = str('<audio src="%s" controls>'  % (file_url) + ugettext('Your browser does not support the audio element.') + '</audio>')
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = _('Audio file player')




