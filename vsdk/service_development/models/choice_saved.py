import datetime

from django.utils import timezone
from django.db import models
from django.db.models import Count, Q
from . import CallSession

class ChoiceSavedYesNoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
          .filter(Q(choice='Yes') | Q(choice='No'))\
          .values('call_date__date', 'choice')\
          .annotate(count=Count('choice'))

class ChoiceSaved(models.Model):
  call_date = models.DateTimeField('call_date')
  choice = models.CharField(max_length=200)
  session = models.ForeignKey(CallSession, on_delete=models.CASCADE, related_name="choice_saved")

  objects = models.Manager() # The default manager.
  yes_no_objects = ChoiceSavedYesNoManager() # The day-specific yes-no manager.
  

  def __str__(self):
    out = "%s;%s;%s;%s" % (str(self.id), str(self.call_date), str(self.choice), str(self.session.id))
    return out
  
