from django.conf import settings
from django.contrib import messages
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from vsdk import settings
from .models import *

def format_validation_result(obj):
        """
        Creates a HTML list from all errors found in validation
        """
        return '<br/>'.join(obj.validator())


class VoiceServiceAdmin(admin.ModelAdmin):
    fieldsets = [(_('General'),    {'fields' : ['name', 'description', 'vxml_url', 'active', 'is_valid', 'validation_details', 'supported_languages']}),
                    (_('Registration process'), {'fields': ['registration', 'registration_language']}),
                    (_('Call flow'), {'fields': ['_start_element']})]
    list_display = ('name','active')
    readonly_fields = ('vxml_url', 'is_valid', 'validation_details')

    def save_model(self, request, obj, form, change):
        if obj.active and 'active' in form.changed_data and settings.KASADAKA:
            #set all other voice services to inactive
            other_vs = VoiceService.objects.exclude(pk=obj.id)
            for vs in other_vs:
                vs.active = False
                vs.save()
            #change asterisk config here
            from pathlib import Path
            my_file = Path(settings.ASTERISK_EXTENSIONS_FILE)
            if my_file.is_file():
                extensions = ''
                with open(settings.ASTERISK_EXTENSIONS_FILE) as infile:
                    import re
                    extensions = infile.read()
                    regex = r"(Vxml\()(.+)(\?callerid\=\$\{CALLERID\(num\)\}\))"
                    subst = "\\1"+ settings.VXML_HOST_ADDRESS + str(obj.get_vxml_url()) + "\\3"
                    extensions = re.sub(regex, subst, extensions, 0)
                with open(settings.ASTERISK_EXTENSIONS_FILE, 'w') as outfile:
                    outfile.write(extensions)
                #Reload asterisk
                import subprocess
                subprocess.getoutput("sudo /etc/init.d/asterisk reload")
                messages.add_message(request, messages.WARNING, _('Voice service activated. Other voice services have been deactivated, the Asterisk configuration has been changed to point to this service, and this new configuration has been loaded.'))
            else:
                messages.add_message(request, messages.ERROR, _('Voice service activated. Other voice services have been deactivated. THE ASTERISK CONFIGURATION COULD NOT BE FOUND!'))
        super(VoiceServiceAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """
        Only allow activation of voice service if it is valid
        """
        if obj is not None:
            if not obj.is_valid():
                return self.readonly_fields + ('active',)
        return self.readonly_fields


    def validation_details(self, obj=None):
        return mark_safe(format_validation_result(obj))
    validation_details.short_description = _('Validation errors')
    

class VoiceServiceElementAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('General'), {'fields' : [ 'name', 'description','service','is_valid', 'validation_details', 'voice_label']}),
        (_('Weather'), {'fields' : [ 'is_weather_element',
                                     'wind_threshold',
                                     'voice_label_wind_normal',
                                     'voice_label_wind_strong',
                                     'voice_label_today',
                                     'voice_label_tomorrow',
                                     'voice_label_monday',
                                     'voice_label_tuesday',
                                     'voice_label_wednesday',
                                     'voice_label_thursday',
                                     'voice_label_friday',
                                     'voice_label_saturday',
                                     'voice_label_sunday',
                                     ]})
    ]
    list_filter = ['service']
    list_display = ('name', 'service', 'is_valid')
    readonly_fields = ('is_valid', 'validation_details')
     
    def validation_details(self, obj=None):
        return mark_safe(format_validation_result(obj))
    validation_details.short_description = _('Validation errors')

class ChoiceOptionsInline(admin.TabularInline):
    model = ChoiceOption
    extra = 2
    fk_name = 'parent'
    view_on_site = False
    verbose_name = _('Possible choice')
    verbose_name_plural = _('Possible choices')

class ChoiceAdmin(VoiceServiceElementAdmin):
    inlines = [ChoiceOptionsInline]

class VoiceLabelInline(admin.TabularInline):
    model = VoiceFragment
    extra = 2
    fk_name = 'parent'
    fieldsets = [(_('General'),    {'fields' : [ 'language', 'is_valid', 'audio', 'audio_file_player']})]
    readonly_fields = ('audio_file_player','is_valid')



class VoiceLabelByVoiceServicesFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Voice Service')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'voice-service'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        voice_services  = VoiceService.objects.all()
        result = []
        for service in voice_services:
            result.append((service.id,service.name))
        return result

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        return VoiceLabel.objects.filter(voiceservicesubelement__service__id=self.value()).distinct()

class VoiceLabelAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = [VoiceLabelByVoiceServicesFilter]
    inlines = [VoiceLabelInline]

    def save_model(self, request, obj, form, change):
        if not settings.KASADAKA:
            messages.add_message(request, messages.WARNING, _('Automatic .wav file conversion only works when running on real KasaDaka system. MANUALLY ensure your files are in the correct format! Wave (.wav) : Sample rate 8KHz, 16 bit, mono, Codec: PCM 16 LE (s16l)'))
        super(VoiceLabelAdmin,self).save_model(request, obj, form, change)



class CallSessionInline(admin.TabularInline):
    model = CallSessionStep
    extra = 0 
    fk_name = 'session'
    can_delete = False
    fieldsets = [(_('General'), {'fields' : ['visited_element', 'time', 'description']})]
    readonly_fields = ('time','session','visited_element', 'description')
    max_num = 0

class CallSessionAdmin(admin.ModelAdmin):
    list_display = ('start','user','service','caller_id','language')
    list_filter = ('service','user','caller_id')
    fieldsets = [(_('General'), {'fields' : ['service', 'user','caller_id','start','end','language']})]
    readonly_fields = ('service','user','caller_id','start','end','language') 
    inlines = [CallSessionInline]
    can_delete = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    #def get_actions(self, request):
    #    actions = super(CallSessionAdmin, self).get_actions(request)
    #    if 'delete_selected' in actions:
    #        del actions['delete_selected']
    #    return actions

class MessagePresentationAdmin(VoiceServiceElementAdmin):
    fieldsets = VoiceServiceElementAdmin.fieldsets + [(_('Message Presentation'), {'fields': ['_redirect','final_element']})]

class KasaDakaUserAdmin(admin.ModelAdmin):
    list_filter = ['service','language','caller_id']
    list_display = ('__str__','caller_id', 'service', 'language')

class SpokenUserInputAdmin(admin.ModelAdmin):
    list_display = ('__str__','category','description','audio_file_player')
    list_filter = ('category',)
    fieldsets = [(_('General'), {'fields' : ['audio', 'audio_file_player', 'session','category','description']})]
    readonly_fields = ('audio','session','category', 'audio_file_player') 
    can_delete = True

    def has_add_permission(self, request):
        return False



# Register your models here.

admin.site.register(VoiceService, VoiceServiceAdmin)
admin.site.register(MessagePresentation, MessagePresentationAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(CallSession, CallSessionAdmin)
admin.site.register(KasaDakaUser, KasaDakaUserAdmin)
admin.site.register(Language)
admin.site.register(VoiceLabel, VoiceLabelAdmin)
admin.site.register(SpokenUserInput, SpokenUserInputAdmin)
admin.site.register(UserInputCategory)
admin.site.register(Record)
