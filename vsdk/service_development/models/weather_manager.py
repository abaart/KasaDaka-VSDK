from django.db import models
from .voicelabel import VoiceLabel
from django.utils.translation import ugettext_lazy as _

class WeatherManager(models.Model):

    service = models.ForeignKey('VoiceService', on_delete = models.CASCADE,
            help_text=_("The service to which this element belongs"))

    creation_date = models.DateTimeField(_('Date created'), auto_now_add = True)

    modification_date = models.DateTimeField(_('Date last modified'), auto_now = True)

    name = models.CharField(_('Name'),max_length=100)

    wind_threshold = models.IntegerField(_('Wind Threshold (km/h)'), blank=True, null=True)

    class Meta:
        verbose_name = _('Voice Service Weather Manager')

    def __str__(self):
        return "Weather-manager: %s" % self.name

    voice_label_wind_normal = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Voice label normal wind'),
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='voice_label_normal_wind',
            )

    voice_label_wind_strong = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Voice label strong wind'),
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='voice_label_strong_wind'
            )

    voice_label_rain_0 = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('Voice label rain 0'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voice_label_rain_0'
    )

    voice_label_rain_0_to_5 = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('Voice label rain 0 to 5'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voice_label_rain_0_to_5'
    )

    voice_label_rain_5 = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('Voice label rain 5'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voice_label_rain_5'
    )

    voice_label_rain_10 = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('Voice label rain 10'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voice_label_rain_10'
    )

    voice_label_rain_15 = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('Voice label rain 15'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voice_label_rain_15'
    )

    voice_label_rain_20 = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('Voice label rain 20'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voice_label_rain_20'
    )

    voice_label_rain_25 = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('Voice label rain 25'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voice_label_rain_25'
    )

    voice_label_rain_30 = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('Voice label rain 30'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voice_label_rain_30'
    )

    voice_label_rain_35 = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('Voice label rain 35'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voice_label_rain_35'
    )

    def get_voice_fragment_url_wind(self, language, forecast, count):
        """
        Returns the url of the audio file of the days' element, in the given language.
        """

        wind_speed_of_day = forecast.days[count].wind_speed
        if wind_speed_of_day < self.wind_threshold:
            return self.voice_label_wind_normal.get_voice_fragment_url(language)
        return self.voice_label_wind_strong.get_voice_fragment_url(language)

    def get_voice_fragment_url_rain(self, language, forecast, count):
        """
        Returns the url of the audio file of the rain file in the given language
        """
        rain = forecast.days[count].rainfall

        if rain == 0:
            return self.voice_label_rain_0.get_voice_fragment_url(language)

        # to prevent saying "no rain" when it's a little rain
        if 0 < rain <= 5:
            return self.voice_label_rain_0_to_5.get_voice_fragment_url(language)

        # round to nearest 10
        rounded_rain = int(round(rain, -1))
        if rounded_rain == 5:
            return self.voice_label_rain_5.get_voice_fragment_url(language)
        if rounded_rain == 10:
            return self.voice_label_rain_10.get_voice_fragment_url(language)
        if rounded_rain == 15:
            return self.voice_label_rain_15.get_voice_fragment_url(language)
        if rounded_rain == 20:
            return self.voice_label_rain_20.get_voice_fragment_url(language)
        if rounded_rain == 25:
            return self.voice_label_rain_25.get_voice_fragment_url(language)
        if rounded_rain == 30:
            return self.voice_label_rain_30.get_voice_fragment_url(language)
        if rounded_rain == 35:
            return self.voice_label_rain_35.get_voice_fragment_url(language)
        else:
            raise ValueError("Rain is more than 35mm/day")