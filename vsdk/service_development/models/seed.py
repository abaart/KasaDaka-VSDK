from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext_lazy as _

class Seed(models.Model):
    """
    Seed that belongs to an advertisement
    """
    seed_name = models.CharField(primary_key=True, max_length=70)

    class Meta:
        verbose_name = _('Seed')

    def __str__(self):
        return self.seed_name
