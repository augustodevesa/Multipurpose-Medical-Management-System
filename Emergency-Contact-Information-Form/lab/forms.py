from django import forms
from .models import Lab
from captcha.fields import CaptchaField
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _

class Login(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = Lab
		fields=['lab_email','lab_password']
		widgets = {
		'lab_password': forms.PasswordInput(),
	}

class Register(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	captcha = CaptchaField()
	class Meta:
		model = Lab
		exclude=['created_at','updated_at','lab_password','lab_progress','lab_otp','lab_otp_created']

class Update_lab(forms.ModelForm):
	class Meta:
		model = Lab
		exclude=['created_at','updated_at','lab_password','lab_email','lab_progress','lab_otp','lab_otp_created']

class Change_Password(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = Lab
		fields=['lab_password']

class forgot_pass_form(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = Lab
		fields=['lab_email']

class forgot_pass_form_chg(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	captcha = CaptchaField()
	class Meta:
		model = Lab
		fields=['lab_otp']

class lab_email_verify(forms.ModelForm):
	class Meta:
		model = Lab
		fields=['lab_otp']
