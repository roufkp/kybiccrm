from django import forms
from django.contrib.auth import get_user_model
from leads.models import Agent,UserProfile

User = get_user_model()

class AgentModelForm(forms.ModelForm):
    role = forms.ChoiceField(choices=Agent.ROLE_CHOICES)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name', 
            'role', 
        )

   