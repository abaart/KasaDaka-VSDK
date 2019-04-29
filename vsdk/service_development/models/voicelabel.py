from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.safestring import mark_safe


from .validators import validate_audio_file_extension, validate_audio_file_format


class VoiceLabel(models.Model):
    name = models.CharField(_('Name'),max_length=50)
    description = models.CharField(_('Description'),max_length=1000, blank = True, null = True)

    class Meta:
        verbose_name = _('Voice Label')

    def __str__(self):
        return _("Voice Label") + ": %s" % (self.name)

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def validator(self, language):
        errors = []        
        if len(self.voicefragment_set.filter(language = language)) > 0:
            errors.extend(self.voicefragment_set.filter(language=language)[0].validator())
        else:
            errors.append(ugettext('"%(description_of_this_element)s" does not have a Voice Fragment for "%(language)s"') %{'description_of_this_element' : str(self),'language' : str(language)})
        return errors

    def get_voice_fragment_url(self, language):
        return self.voicefragment_set.filter(language=language)[0].get_url()

class Language(models.Model):
    name = models.CharField(_('Name'),max_length=100, unique = True)
    code = models.CharField(_('Code'),max_length=10, unique = True)
    voice_label = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = _('Language voice label'),
            related_name = 'language_description_voice_label',
            help_text = _("A Voice Label of the name of the language"))
    error_message = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = _('Error message voice label'),
            related_name = 'language_error_message',
            help_text = _("A general error message"))
    select_language = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = _('Select language voice label'),
            related_name = 'language_select_language',
            help_text = _("A message requesting the farmer to select a language"))
    pre_choice_option = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = _('Pre-Choice Option voice label'),
            related_name = 'language_pre_choice_option',
            help_text = _("The fragment that is to be played before a choice option (e.g. '[to select] option X, please press 1')"))
    post_choice_option = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = _('Post-Choice Option voice label'),
            related_name = 'language_post_choice_option',
            help_text = _("The fragment that is to be played before a choice option (e.g. 'to select option X, [please press] 1')"))
    one = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'1'},
            related_name = 'language_one',
            help_text = ugettext('The number %(number)s')% {'number':'1'})
    two = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'2'},
            related_name = 'language_two',
            help_text = ugettext("The number %(number)s")% {'number':'2'})
    three = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'3'},
            related_name = 'language_three',
            help_text = ugettext("The number %(number)s")% {'number':'3'})
    four = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'4'},
            related_name = 'language_four',
            help_text = ugettext("The number %(number)s")% {'number':'4'})
    five = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'5'},
            related_name = 'language_five',
            help_text = ugettext("The number %(number)s")% {'number':'5'})
    six = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'6'},
            related_name = 'language_six',
            help_text = ugettext("The number %(number)s")% {'number':'6'})
    seven = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'7'},
            related_name = 'language_seven',
            help_text = ugettext("The number %(number)s")% {'number':'7'})
    eight = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'8'},
            related_name = 'language_eight',
            help_text = ugettext("The number %(number)s")% {'number':'8'})
    nine = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'9'},
            related_name = 'language_nine',
            help_text = ugettext("The number %(number)s")% {'number':'9'})
    zero = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            verbose_name = ugettext("The number %(number)s")% {'number':'0'},
            related_name = 'language_zero',
            help_text = ugettext("The number %(number)s")% {'number':'0'})

    class Meta:
        verbose_name = _('Language')

    def __str__(self):
        return '%s (%s)' % (self.name, self.code)

    @property
    def get_description_voice_label_url(self):
        """
        Returns the URL of the Voice Fragment describing
        the language, in the language itself.
        """
        return self.voice_label.get_voice_fragment_url(self)

    @property
    def get_interface_numbers_voice_label_url_list(self):
        numbers = [
                    self.zero,
                    self.one,
                    self.two,
                    self.three,
                    self.four,
                    self.five,
                    self.six,
                    self.seven,
                    self.eight,
                    self.nine
                    ]
        result = []
        for number in numbers:
            result.append(number.get_voice_fragment_url(self))
        return result

    @property
    def get_interface_voice_label_url_dict(self):
        """
        Returns a dictionary containing all URLs of Voice
        Fragments of the hardcoded interface audio fragments.
        """
        interface_voice_labels = {
                'voice_label':self.voice_label,
                'error_message':self.error_message,
                'select_language':self.select_language,
                'pre_choice_option':self.pre_choice_option,
                'post_choice_option':self.post_choice_option,
                }
        for k, v in interface_voice_labels.items():
            interface_voice_labels[k] = v.get_voice_fragment_url(self)
        return interface_voice_labels



class VoiceFragment(models.Model):
    parent = models.ForeignKey('VoiceLabel',
            on_delete = models.CASCADE)
    language = models.ForeignKey(
            'Language',
            on_delete = models.CASCADE)
    audio = models.FileField(_('Audio'),
            validators=[validate_audio_file_extension],
            help_text = _("Ensure your file is in the correct format! Wave (.wav) : Sample rate 8KHz, 16 bit, mono, Codec: PCM 16 LE (s16l)"))


    class Meta:
        verbose_name = _('Voice Fragment')

    def convert_wav_to_correct_format(self):
        from vsdk import settings
        if not settings.KASADAKA:
            pass

        import subprocess
        from os.path import basename
        new_file_name = self.audio.path[:-4] + "_conv.wav"
        subprocess.getoutput("sox -S %s -r 8k -b 16 -c 1 -e signed-integer %s"% (self.audio.path, new_file_name))
        self.audio = basename(new_file_name)
        
        


    def save(self, *args, **kwargs):
        super(VoiceFragment, self).save(*args, **kwargs)
        from vsdk import settings
        if  settings.KASADAKA:
            format_correct = validate_audio_file_format(self.audio)
            if not format_correct: 
                self.convert_wav_to_correct_format()
        super(VoiceFragment, self).save(*args, **kwargs)




    def __str__(self):
        return _("Voice Fragment: (%(name)s) %(name_parent)s") % {'name' : self.language.name, 'name_parent' : self.parent.name}

    def get_url(self):
        return self.audio.url

    def validator(self):
        errors = []
        #Temporary for ICT4D 2018, Heroku performance optimalization
        return errors
        try:
            accessible = self.audio.storage.exists(self.audio.name)
        except NotImplementedError:
            import urllib.request
            try:
                response = urllib.request.urlopen(self.audio.url)
                accessible = True
            except urllib.error.HTTPError:
                accessible = False


        if not self.audio:
            errors.append(ugettext('%s does not have an audio file')%str(self))
        elif not accessible:
            errors.append(ugettext('%s audio file not accessible')%str(self))
        #TODO verift whether this really is not needed anymore
        #elif not validate_audio_file_format(self.audio):
        #    errors.append(ugettext('%s audio file is not in the correct format! Should be: Wave: Sample rate 8KHz, 16 bit, mono, Codec: PCM 16 LE (s16l)'%str(self)))
        return errors

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio:
            file_url = settings.MEDIA_URL + str(self.audio)
            player_string = str('<audio src="%s" controls>'  % (file_url) + ugettext('Your browser does not support the audio element.') + '</audio>')
            return mark_safe(player_string)

    audio_file_player.short_description = _('Audio file player')


