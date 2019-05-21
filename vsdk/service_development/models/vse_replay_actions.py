from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from .vs_element import VoiceServiceElement


class ReplayActions(VoiceServiceElement):
    _urls_name = 'service-development:replay-actions'
    _redirect = models.ForeignKey(
            VoiceServiceElement,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name='%(app_label)s_%(class)s_related',
            verbose_name=_('Redirect element'),
            help_text=_("The element to redirect to after the replay_actions has been played."))
    created = models.ForeignKey('VoiceLabel',
            on_delete=models.PROTECT,
            verbose_name=_('Created'),
            related_name='replay_action_created',
            help_text=_("A Voice Label of 'created'"))
    updated = models.ForeignKey('VoiceLabel',
            on_delete=models.PROTECT,
            verbose_name=_('Updated'),
            related_name='replay_action_updated',
            help_text=_("A Voice Label of 'updated'"))
    removed = models.ForeignKey('VoiceLabel',
            on_delete=models.PROTECT,
            verbose_name=_('Removed'),
            related_name='replay_action_removed',
            help_text=_("A Voice Label of 'removed'"))
    you_have = models.ForeignKey('VoiceLabel',
            on_delete=models.PROTECT,
            verbose_name=_('You have'),
            related_name='replay_action_you_have',
            help_text=_("A Voice Label of 'you have'"))
    advertisements = models.ForeignKey('VoiceLabel',
             on_delete=models.PROTECT,
             verbose_name=_('Advertisements'),
             related_name='replay_action_advertisements',
             help_text=_("A Voice Label of 'advertisements'"))
    an_advertisement = models.ForeignKey('VoiceLabel',
             on_delete=models.PROTECT,
             verbose_name=_('An advertisement'),
             related_name='replay_action_an_advertisement',
             help_text=_("A Voice Label of 'an advertisement'"))
    replay_for = models.ForeignKey('VoiceLabel',
             on_delete=models.PROTECT,
             verbose_name=_('For'),
             related_name='replay_action_for',
             help_text=_("A Voice Label of 'for'"))
    namely = models.ForeignKey('VoiceLabel',
            on_delete=models.PROTECT,
            verbose_name=_('Namely'),
            related_name='replay_action_namely',
            help_text=_("A Voice Label of 'namely'"))
    made_no_new_changes_to_your_advertisements = models.ForeignKey('VoiceLabel',
            on_delete=models.PROTECT,
            verbose_name=_('Made no new changes to your advertisements'),
            related_name='replay_action_made_no_new_changes_to_your_advertisements',
            help_text=_("A Voice Label of 'made_no_new_changes_to_your_advertisements'"))

    class Meta:
        verbose_name = _('Replay Action Element')

    @property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        if self._redirect:
            return VoiceServiceElement.objects.get_subclass(id=self._redirect.id)
        else:
            return None

    def __str__(self):
        return 'Replay actions:' + self.name

    def is_valid(self):
        return len(self.validator()) == 0

    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def validator(self):
        errors = []
        errors.extend(super(ReplayActions, self).validator())
        if not self._redirect:
            errors.append(ugettext('Replay actions %s does not have a redirect element') % self.name)

        return errors

    @property
    def get_interface_voice_label_url_dict(self):
        """
        Returns a dictionary containing all URLs of Voice
        Fragments of the hardcoded interface audio fragments.
        """
        interface_voice_labels = {
                'created':self.created,
                'updated':self.updated,
                'removed':self.removed,
                'you_have':self.you_have,
                'advertisements':self.advertisements,
                'an_advertisement':self.an_advertisement,
                'for': self.replay_for,
                'namely': self.namely,
                'made_no_new_changes_to_your_advertisements': self.made_no_new_changes_to_your_advertisements
                }
        for k, v in interface_voice_labels.items():
            interface_voice_labels[k] = v.get_voice_fragment_url(self)
        return interface_voice_labels
