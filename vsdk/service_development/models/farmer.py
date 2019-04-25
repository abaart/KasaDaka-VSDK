from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from . import Language


class Farmer(models.Model):
    caller_id = models.CharField(_('Phone number'),max_length=100, unique = True)
    name = models.CharField(_('Name'), max_length = 100, blank = True)
    creation_date = models.DateTimeField(_('Date created'),auto_now_add = True)
    modification_date = models.DateTimeField(_('Date last modified'),auto_now = True)
    language = models.ForeignKey(Language,on_delete = models.SET_NULL, null = True)
    region = models.CharField(_('Region'), max_length = 100, blank = True)
    place = models.CharField(_('Place'), max_length = 100, blank = True)
