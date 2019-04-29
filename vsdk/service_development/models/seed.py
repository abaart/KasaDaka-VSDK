from django.db import models
from django.utils.translation import ugettext_lazy as _


class Seed(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Seed Name'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('Seed')

    def __str__(self):
        return "%s" % self.name
