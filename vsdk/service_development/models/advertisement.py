import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from enum import Enum

from . import KasaDakaUser

class Advertisement(models.Model):
    """
    Advertisement that belongs to a farmer
    """
    farmer = models.ForeignKey(KasaDakaUser, on_delete=models.CASCADE)
    seed = models.CharField(max_length=200)
    description = models.TextField(default="", blank=True)
    quantity = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    price = models.PositiveIntegerField(validators=[MaxValueValidator(999999999)])
    pub_date = models.DateTimeField('date published')

    class Meta:
        unique_together = (('farmer', 'pub_date'),)
        unique_together = (('farmer', 'seed'),)

    def __str__(self):
        return self.seed

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
