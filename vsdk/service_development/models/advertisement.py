from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import KasaDakaUser, Seed


class Advertisement(models.Model):
    farmer = models.ForeignKey(KasaDakaUser,on_delete = models.SET_NULL, null = True)
    seed = models.ForeignKey(Seed,on_delete = models.SET_NULL, null = True)
    quantity = models.IntegerField(_('Quantity'), default = 0, blank = True)
    price = models.IntegerField(_('Price'), default = 0, blank = True)

    class Meta:
        verbose_name = _('Advertisement')

    def __str__(self):
        return self.seed
