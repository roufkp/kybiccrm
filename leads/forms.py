from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,UsernameField
from .models import Lead,Agent,Category,FollowUp

User = get_user_model() 

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'whatsapp_number',
            'email',
            'age',
            'description',
            'q1',
            'a1',
            'job_title',
            'city',

        )

class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )


class AssignAgentForm(forms.Form):
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)   

    def __init__(self, *args, **kwargs):
        request= kwargs.pop("request")
        agents = Agent.objects.filter(organisation= request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        print(request.user.userprofile)
        self.fields["agent"].queryset = agents
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())
    

class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields=(
            "category",
        
        )
class FollowUpModelForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = (
            'notes',
            'file',
            'next_date'
        )