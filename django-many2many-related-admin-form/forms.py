### An example of functionality


from accounts.models import User
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _
from pools.models import PoolDirector


class UserForm(forms.ModelForm):
    """Competition form"""

    member_pools = forms.ModelMultipleChoiceField(
        PoolDirector.objects.all(), required=False, label=_('Pool director'),
        widget=FilteredSelectMultiple(_('pools'), False))

    class Meta:
        """Meta class"""

        model = User
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.initial['member_pools'] = self.instance.members.values_list('pk', flat=True)

    def save(self, commit=True):
        instance = super(UserForm, self).save(commit)

        member_pools = self.cleaned_data['member_pools']
        if member_pools is not None:
            self._save_members_pool_director(instance=instance, member_pools=member_pools)

        return instance

    @staticmethod
    def _save_members_pool_director(instance, member_pools):
        for pool_director in instance.members.all():
            if pool_director not in member_pools:
                instance.members.remove(pool_director)

        for pool_director in member_pools:
            if pool_director not in instance.members.all():
                instance.members.add(pool_director)
