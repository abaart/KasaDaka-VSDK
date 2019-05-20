import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from enum import Enum

from . import Farmer, Seed

class Advertisement(models.Model):
    """
    Advertisement that belongs to a farmer
    """
    farmer = models.ForeignKey(Farmer, on_delete=models.SET_NULL, null=True)
    seed = models.ForeignKey(Seed,on_delete = models.SET_NULL, blank=True, null=True, default=1)
    quantity = models.PositiveIntegerField(validators=[MaxValueValidator(99999)], null = True)
    pub_date = models.DateTimeField(_('Date published'), auto_now_add=True)

    class Meta:
        verbose_name = _('Advertisement')
        unique_together = (('farmer', 'seed'),)

    def __str__(self):
        if self.farmer is not None and self.seed is not None:
            return "%s %s (%s)" % (self.farmer.name, self.seed.name)
        else:
            return ""

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
