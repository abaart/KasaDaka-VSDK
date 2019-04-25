from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from . import Farmer


class Advertisement(models.Model):
    farmer = models.ForeignKey(Farmer,on_delete = models.SET_NULL, null = True)
    seed = models.CharField(_('Seed'), max_length = 100, blank = True)
    amount = models.IntegerField(_('Amount'), default = 0, blank = True)
    price = models.IntegerField(_('Price'), default = 0, blank = True)
