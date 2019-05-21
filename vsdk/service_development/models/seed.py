from django.db import models
from django.utils.translation import ugettext_lazy as _


class Seed(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Seed Name'), max_length=100, blank=True)
    voice_label = models.ForeignKey(
            'VoiceLabel',
            on_delete=models.PROTECT,
            verbose_name=_('Seed voice label'),
            related_name='seed_voice_label',
            help_text=_("A Voice Label of the name of the seed"),
            blank=True,
            null=True)

    class Meta:
        verbose_name = _('Seed')

    def __str__(self):
        return "%s" % self.name

    def get_voice_fragment_url(self, language):
        """
        Returns the url of the audio file of this element, in the given language.
        """
        return self.voice_label.get_voice_fragment_url(language)
