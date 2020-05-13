import datetime

from django.utils import timezone
from django.db import models
from django.db.models import Count

class ChoiceSavedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
          .values('call_date__date', 'choice')\
          .annotate(count=Count('choice'))

class ChoiceSaved(models.Model):
  call_date = models.DateTimeField('call_date')
  choice = models.CharField(max_length=200)

  objects = models.Manager() # The default manager.
  day_objects = ChoiceSavedManager() # The day-specific manager.

  def __str__(self):
    out = "%s;%s;%s" % (str(self.id), str(self.call_date), str(self.choice))
    return out
  
