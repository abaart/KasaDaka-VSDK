from django.db import models
from django.utils.translation import ugettext_lazy as _


class Commune(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Commune Name'), max_length=100, blank=True)

    class Meta:
        verbose_name = _('Commune')

    def __str__(self):
        return "%s" % self.name
