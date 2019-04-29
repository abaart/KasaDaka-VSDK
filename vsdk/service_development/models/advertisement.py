from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import Farmer


class Advertisement(models.Model):
    farmer = models.ForeignKey(Farmer,on_delete = models.SET_NULL, null = True)
    product = models.CharField(_('Product'), max_length = 100, blank = True)
    quantity = models.IntegerField(_('Quantity'), default = 0, blank = True)
    price = models.IntegerField(_('Price'), default = 0, blank = True)

    class Meta:
        verbose_name = _('Advertisement')

    def __str__(self):
        return self.seed

def lookup_advertisement_by_farmer(farmer, service):
    """
    If farmer for current voice_service exists, returns Advertisement objects.
    If farmer does not exist, returns None.
    """
    if farmer:
        try:
            return Advertisement.objects.get(farmer = farmer, service = service)
        except Advertisement.DoesNotExist:
            return None
    return None
