from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile_org

class OrganizationRegisterForm(UserCreationForm):
	email = forms.EmailField()
	# meta class tells which model it intercts with
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class OrganizationUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	
	class Meta:
		model = User
		fields = ['username', 'email']


class Profile_viewerUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile_org
		fields = ['roll_number','department']

class Profile_orgUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile_org
		fields = ['image']