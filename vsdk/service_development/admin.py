from django.contrib import admin

from vsdk.service_development.models.session import EndUserCallSession
from .models import VoiceService, MessagePresentation, Choice, ChoiceOption, VoiceFragment, CallSession, CallSessionStep, KasaDakaUser, Language, VoiceLabel, Record, \
    Result, ListCallSessions


def format_validation_result(obj):
        """
        Creates a HTML list from all errors found in validation
        """
        return '<br/>'.join(obj.validator())


class VoiceServiceAdmin(admin.ModelAdmin):
    fieldsets = [('General',    {'fields' : ['name', 'description', 'vxml_url', 'active', 'is_valid', 'validation_details', 'supported_languages']}),
                    ('Requirements', {'fields': ['requires_registration', 'end_user_service', 'radio_journalist_service']}),
                    ('Call flow', {'fields': ['_start_element']})]
    list_display = ('name','active','is_valid')
    readonly_fields = ('vxml_url', 'is_valid', 'validation_details')

    def get_readonly_fields(self, request, obj=None):
        """
        Only allow activation of voice service if it is valid
        """
        if obj is not None:
            if not obj.is_valid():
                return self.readonly_fields + ('active',)
        return self.readonly_fields


    def validation_details(self, obj=None):
        return format_validation_result(obj)
    validation_details.allow_tags = True
    

class VoiceServiceElementAdmin(admin.ModelAdmin):
    fieldsets = [('General',    {'fields' : [ 'name', 'description','service','map_to_call_session_property', 'is_valid', 'validation_details', 'voice_label']})]
    list_display = ('name', 'service', 'is_valid')
    readonly_fields = ('is_valid', 'validation_details')
     
    def validation_details(self, obj=None):
        return format_validation_result(obj)
    validation_details.allow_tags = True

class ChoiceOptionsInline(admin.TabularInline):
    model = ChoiceOption
    exclude = ['map_to_call_session_property ']
    extra = 2
    fk_name = 'parent'
    view_on_site = False

class ChoiceAdmin(VoiceServiceElementAdmin):
    inlines = [ChoiceOptionsInline]

class VoiceLabelInline(admin.TabularInline):
    model = VoiceFragment
    extra = 2
    fk_name = 'parent'

class VoiceLabelAdmin(admin.ModelAdmin):
    inlines = [VoiceLabelInline]

class CallSessionInline(admin.TabularInline):
    model = CallSessionStep
    extra = 0 
    fk_name = 'session'
    can_delete = False
    fieldsets = [('General', {'fields' : ['visited_element', 'time']})]
    readonly_fields = ('time','session','visited_element')
    max_num = 0

class ResultInline(admin.TabularInline):
    model = Result
    extra = 0
    fk_name = 'session'
    fields = ['name', 'file', 'value']
    readonly_fields = ['name', 'file']
    can_delete = False
    max_num = 0

class CallSessionAdmin(admin.ModelAdmin):
    list_display = ('start','user','service','caller_id','language')
    fieldsets = [('General', {'fields' : ['service', 'user','caller_id','start','end','language']})]
    readonly_fields = ('service','user','caller_id','start','end','language') 
    inlines = [ResultInline,CallSessionInline]
    can_delete = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, reques, obj=None):
        return True

    def get_actions(self, request):
        actions = super(CallSessionAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class EndUserCallSessionAdmin(admin.ModelAdmin):
    list_display = ('start','user','category', 'service','caller_id','language')
    fieldsets = [('General', {'fields' : ['service', 'user', 'category', 'caller_id','start','end','language']})]
    readonly_fields = ('service','user','caller_id','start','end','language')
    search_fields = ['category']
    list_filter = ['service', 'start', 'category', '_language', 'user']
    inlines = [ResultInline]
    can_delete = True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    def get_actions(self, request):
        actions = super(EndUserCallSessionAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

class ListCallSessionsAdmin(admin.ModelAdmin):
    exclude = ['map_to_call_session_property', 'voice_label']

class MessagePresentationAdmin(VoiceServiceElementAdmin):
    fieldsets = VoiceServiceElementAdmin.fieldsets + [('Message Presentation', {'fields': ['_redirect','final_element']})]

# Register your models here.

admin.site.register(VoiceService, VoiceServiceAdmin)
admin.site.register(MessagePresentation, MessagePresentationAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(CallSession, CallSessionAdmin)
admin.site.register(EndUserCallSession, EndUserCallSessionAdmin)
admin.site.register(KasaDakaUser)
admin.site.register(Language)
admin.site.register(VoiceLabel, VoiceLabelAdmin)
admin.site.register(Record)
admin.site.register(ListCallSessions, ListCallSessionsAdmin)