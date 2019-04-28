from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import Farmer


class Advertisement(models.Model):
    farmer = models.ForeignKey(Farmer,on_delete = models.SET_NULL, null = True)
    seed = models.CharField(_('Seed'), max_length = 100, blank = True)
    quantity = models.IntegerField(_('Quantity'), default = 0, blank = True)
    price = models.IntegerField(_('Price'), default = 0, blank = True)

    def __str__(self):
        return self.seed
