from datetime import date, timedelta

from django.db import models
from model_utils.managers import InheritanceManager
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from .voicelabel import VoiceLabel


class VoiceServiceSubElement(models.Model):
    """
    A sub-element in a voice service (could be ChoiceOption, etc).
    Is NOT accessible through HTTP in a VoiceXML
    """

    #use django_model_utils to be able to find out what is the subclass of this element
    #see: https://django-model-utils.readthedocs.io/en/latest/managers.html#inheritancemanager
    objects = InheritanceManager()

    service = models.ForeignKey('VoiceService', on_delete = models.CASCADE,
            help_text=_("The service to which this element belongs"))
    creation_date = models.DateTimeField(_('Date created'), auto_now_add = True)
    modification_date = models.DateTimeField(_('Date last modified'), auto_now = True)
    name = models.CharField(_('Name'),max_length=100)
    description = models.CharField(
            max_length = 1000,
            blank = True)
    voice_label = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Voice label'),
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            )

    # Weather Parameters

    is_weather_element = models.BooleanField(_('This element contains weather forecasts'), default = False)
    wind_threshold = models.IntegerField(_('Wind Threshold (km/h)'), blank=True, null=True)

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

    voice_label_today = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Voice label today'),
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='voice_label_today'
    )

    voice_label_tomorrow = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Voice label tomorrow'),
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='voice_label_tomorrow'
    )

    voice_label_monday = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Voice label monday'),
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='voice_label_monday'
    )

    voice_label_tuesday = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Voice label tuesday'),
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='voice_label_tuesday'
    )

    voice_label_wednesday = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Voice label wednesday'),
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='voice_label_wednesday'
    )

    voice_label_thursday = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Voice label thursday'),
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='voice_label_thursday'
    )

    voice_label_friday = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Voice label friday'),
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='voice_label_friday'
    )

    voice_label_saturday = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Voice label saturday'),
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='voice_label_saturday'
    )

    voice_label_sunday = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Voice label sunday'),
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='voice_label_sunday'
    )

    voice_label_rain_0 = models.ForeignKey(
        VoiceLabel,
        verbose_name=_('Voice label rain 0'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voice_label_rain_0'
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

    class Meta:
        verbose_name = _('Voice Service Sub-Element')

    def __str__(self):
        return "Sub-element: %s" % self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def validator(self):
        """
        Returns a list of problems with this element that would surface when accessing
        through voice.
        """
        errors = []
        #check if voice label is present, and validate it
        if self.voice_label:
            for language in self.service.supported_languages.all():
                errors.extend(self.voice_label.validator(language))
        else:
            errors.append(ugettext('No VoiceLabel in: "%s"')%str(self))
        return errors


    def get_voice_fragment_url(self, language):
        """
        Returns the url of the audio file of this element, in the given language.
        """
        return self.voice_label.get_voice_fragment_url(language)

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
        rounded_rain = int(round(rain, -1)) # round to nearest 10
        if rounded_rain == 0:
            return self.voice_label_rain_0.get_voice_fragment_url(language)
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


    def get_voice_fragment_url_day(self, language, forecast, count):
        """Returns the url of the audio file for the corresponding day.
        It will use today, tomorrow, [weekday of day after tomorrow], ...
        """

        day_in_forecast = forecast.days[count].forecast_date
        today = date.today()

        # today
        if day_in_forecast == today:
            return self.voice_label_today.get_voice_fragment_url(language)

        # tomorrow
        elif day_in_forecast == today + timedelta(days=1):
            return self.voice_label_tomorrow.get_voice_fragment_url(language)

        # Mondays
        elif day_in_forecast.weekday() == 0:
            return self.voice_label_monday.get_voice_fragment_url(language)

        # Tuesday
        elif day_in_forecast.weekday() == 1:
            return self.voice_label_tuesday.get_voice_fragment_url(language)

        # Wednesday
        elif day_in_forecast.weekday() == 2:
            return self.voice_label_wednesday.get_voice_fragment_url(language)

        # Thursday
        elif day_in_forecast.weekday() == 3:
            return self.voice_label_thursday.get_voice_fragment_url(language)

        # Friday
        elif day_in_forecast.weekday() == 4:
            return self.voice_label_friday.get_voice_fragment_url(language)

        # Saturday
        elif day_in_forecast.weekday() == 5:
            return self.voice_label_saturday.get_voice_fragment_url(language)

        # Sunday
        elif day_in_forecast.weekday() == 6:
            return self.voice_label_sunday.get_voice_fragment_url(language)

        else:
            raise ValueError("weekday not calculated correctly")


    def get_subclass_object(self):
        return VoiceServiceSubElement.objects.get_subclass(id = self.id)


class VoiceServiceElement(VoiceServiceSubElement):
    """
    An element in a voice service (could be Choice, Message, etc.)
    Is accessible through HTTP in a generated VoiceXML
    """
    objects = InheritanceManager()
    _urls_name = "" #This should be the same as in urls.py
    
    class Meta:
        verbose_name = _('Voice Service Element')
    
    def __str__(self):
        return _("Element: %s") % self.name

    def get_absolute_url(self, session):
        """
        Returns the url at which this element is accessible through VoiceXML.
        """
        return reverse(self._urls_name, kwargs= {'element_id':str(self.id), 'session_id':session.id})