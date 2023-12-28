from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
from django import forms
from .models import Interest, UserProfile

class UserProfileForm(forms.ModelForm):
    birth_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
    profile_image = forms.ImageField(required=True)
    company_code = forms.CharField(max_length=255,required=True)

    class Meta:
        model = UserProfile
        fields = ['birth_date', 'interests', 'profile_image', 'company_code']

from django import forms
from .models import Project

class ProjectUploadForm(forms.ModelForm):
    project_name = forms.CharField(max_length=300 )
    class Meta:
        model = Project
        fields = ['project_file','project_name']
  
