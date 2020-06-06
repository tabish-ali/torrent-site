from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class UserRegisterForm(forms.Form, UserCreationForm):
	class Meta :
		model = User
		fields ={
		'username',
		'password1',
		'password2',
		}

	username = forms.CharField(label='User Name',required=True,widget=forms.TextInput(
							attrs={'placeholder':'Username','class':'form-control my-input'}))

	password1 = forms.CharField(label='User Name',required=True,widget=forms.PasswordInput(
							attrs={'placeholder':'Password','class':'form-control my-input'}))
							
	password2 = forms.CharField(label='User Name',required=True,widget=forms.PasswordInput(
							attrs={'placeholder':'Confirm password','class':'form-control my-input'}))

class UserProfileForm(forms.ModelForm):
	class Meta :
		model = UserProfile
		fields ={
		'email',
		'first_name',	
		'image_field',
		}

	email = forms.CharField(label='User Name',required=True,widget=forms.TextInput(
							attrs={'placeholder':'email','class':'form-control my-input'}))

	first_name = forms.CharField(label='User Name',required=True,widget=forms.TextInput(
							attrs={'placeholder':'First Name','class':'form-control my-input'}))

class UserloginForm(forms.Form):

	class Meta :
		model = User
		fields ={
		'Usr_Name',
		'Usr_Pwd',
		}

	Usr_Name = forms.CharField(label='User Name:',required=True,widget=forms.TextInput(
								attrs={'placeholder':'User Name','class':'form-control my-input'}))

	Usr_Pwd = forms.CharField(label='Password',required=True,widget=forms.PasswordInput(
							attrs={'placeholder':'Password','class':'form-control my-input'}))


class UserPasswordEditForm(UserChangeForm):

	class Meta:
		model = User 
		fields = {
			'username',
			'password',
		}

class UserEditForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = {
			'first_name',
			'email',
			'image_field',
			'profile_status',
		}
		
