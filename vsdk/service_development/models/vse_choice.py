from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from .vs_element import VoiceServiceElement, VoiceServiceSubElement

class Choice(VoiceServiceElement):
    _urls_name = 'service-development:choice'

    class Meta:
        verbose_name = _('Choice Element')

    def __str__(self):
        return self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def validator(self):
        errors = []
        errors.extend(super(Choice, self).validator())
        choice_options = self.choice_options.all()
        for choice_option in choice_options:
            errors.extend(choice_option.validator())

        #deduplicate errors
        errors = list(set(errors))
        return errors


class ChoiceOption(VoiceServiceSubElement):
    ACTION_CHOICES = (
        ('remove', 'Remove'),
    )

    parent = models.ForeignKey(
            Choice,
            on_delete = models.CASCADE,
            related_name='choice_options')
    _redirect = models.ForeignKey(
            VoiceServiceElement, 
            on_delete = models.SET_NULL,
            verbose_name = _('Redirect element'),
            help_text = _("The element to redirect to when this choice is made by the farmer."),
            related_name='%(app_label)s_%(class)s_redirect_related',
            blank = True,
            null = True)
    action = models.CharField(verbose_name=_("Action"), max_length=30, choices=ACTION_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = _('Voice Service')

    @property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        return VoiceServiceSubElement.objects.get_subclass(id = self._redirect.id)

    def __str__(self):
        return "(%s): %s" % (self.parent.name,self.name)
    
    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def validator(self):
        errors = []
        errors.extend(super(ChoiceOption, self).validator())
        #check if redirect is present
        if not self._redirect:
            errors.append(ugettext('No redirect in choice option: "%s"')%str(self))
        else:
            if self.service.id != self.parent.service.id:
                errors.append(ugettext('Choice option "%(name_of_element)s" not in correct (same) Voice Service as Choice element! ("%(name_service_of_element)s", should be "%(name_service_of_parent_of_element)s")')%{'name_of_element' : str(self),'name_service_of_element' : str(self.service),'name_service_of_parent_of_element' : str(self.parent.service)})
            if self.redirect.service.id != self.parent.service.id:
                errors.append(ugettext('Redirect element of choice option "%(name_of_element)s" not in correct (same) Voice Service! ("%(name_service_of_element)s", should be "%(name_service_of_parent_of_element)s")')%{'name_of_element' : str(self),'name_service_of_element' : str(self.redirect.service),'name_service_of_parent_of_element' : str(self.service)})

        return errors

