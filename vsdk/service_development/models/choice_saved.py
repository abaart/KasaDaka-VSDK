from django.db import models

class ChoiceSaved(models.Model):
  call_date = models.DateTimeField('call_date')
  choice = models.CharField(max_length=200)

  def __str__(self):
    out = "%s;%s;%s" % (str(self.id), str(self.call_date), str(self.choice))
    return out