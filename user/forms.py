from django import forms
from .models import User,User_fb,User_contacts,User_medical,User_surgery
from captcha.fields import CaptchaField
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _
class Login(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = User
		fields=['email','password']
		widgets = {
		'password': forms.PasswordInput(),
	}

class Register(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	captcha = CaptchaField()
	class Meta:
		model = User
		exclude=['created_at','updated_at','password','User_progress','User_otp','User_otp_created']
class Update_user(forms.ModelForm):
	class Meta:
		model = User
		exclude=['created_at','updated_at','password','email','User_progress','User_otp','User_otp_created']
class Change_Password(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields=['password']
class forgot_pass_form(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = User
		fields=['email','dateofBirth']
class forgot_pass_form_chg(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	captcha = CaptchaField()
	class Meta:
		model = User
		fields=['User_otp']
class email_verify(forms.ModelForm):
	class Meta:
		model = User
		fields=['User_otp']
class user_feedback_form(forms.ModelForm):
	class Meta:
		model= User_fb
		fields=['content','subject']
class user_emergency_contacts(forms.ModelForm):
	class Meta:
		model = User_contacts
		exclude=['user']
class user_surgery_f(forms.ModelForm):
	class Meta:
		model = User_surgery
		exclude=['user']
class basic_med_form(forms.ModelForm):
	class Meta:
		model = User_medical
		exclude=['user','updated_at']
		