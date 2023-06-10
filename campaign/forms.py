from django import forms
from django.contrib.auth import get_user_model
from leads.models import Campaign,Agent
from django.forms import DateInput

# class CampaignModelForm(forms.ModelForm):
#     agent = forms.ModelMultipleChoiceField(queryset=Agent.objects.none())

#     class Meta:
#         model = Campaign
#         fields = (
#             'name',
#             'end_date',
#             'description',
#         )

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user')

#         super().__init__(*args, **kwargs)

#         self.fields['agent'].queryset = Agent.objects.filter(organisation=user.userprofile)

#     def save(self, commit=True):
#         campaign = super().save(commit=False)
#         if commit:
#             campaign.save()
#         self.save_m2m()
#         return campaign
class CampaignModelForm(forms.ModelForm):
    agents = forms.ModelMultipleChoiceField(queryset=Agent.objects.none())

    class Meta:
        model = Campaign
        fields = (
            'name',
            'end_date',
            'ad_id',
            # 'agent',
            'description',
        )
        widgets = {
            'end_date': DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

        self.fields['agents'].queryset = Agent.objects.filter(organisation=user.userprofile)

    def save(self, commit=True):
        campaign = super().save(commit=False)
        if commit:
            campaign.save()
            self.save_m2m()

        return campaign


class CampaignAddAgentModelForm(forms.ModelForm):
    agent = forms.ModelMultipleChoiceField(queryset=Agent.objects.none())

    class Meta:
        model = Campaign
        fields = ('agent',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        campaign_id = kwargs.pop('campaign_id')
        super().__init__(*args, **kwargs)
        self.fields['agent'].queryset = Agent.objects.filter(organisation=user.userprofile).exclude(campaign=campaign_id)


class AgentSelectionForm(forms.Form):
    agents = forms.ModelMultipleChoiceField(queryset=Agent.objects.all())



class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField()
    subject = forms.CharField(max_length=500)
    message = forms.CharField(widget=forms.Textarea)


    