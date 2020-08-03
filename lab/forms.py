from django import forms
from .models import Lab,Lab_fb
from user.models import User
from captcha.fields import CaptchaField
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _
class Login(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = Lab
		fields=['email','password']
		widgets = {
		'password': forms.PasswordInput(),
	}
class Register(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	captcha = CaptchaField()
	class Meta:
		model = Lab
		exclude=['created_at','updated_at','password','User_progress','User_otp','User_otp_created']
class Update_user(forms.ModelForm):
	class Meta:
		model = Lab
		exclude=['created_at','updated_at','password','email','User_progress','User_otp','User_otp_created']
class Change_Password(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = Lab
		fields=['password']
class forgot_pass_form(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = Lab
		fields=['email']
class forgot_pass_form_chg(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	captcha = CaptchaField()
	class Meta:
		model = Lab
		fields=['User_otp']
class email_verify(forms.ModelForm):
	class Meta:
		model = Lab
		fields=['User_otp']
class lab_feedback_form(forms.ModelForm):
	class Meta:
		model= Lab_fb
		fields=['content','subject']
class lab_consult_user_login(forms.ModelForm):
	class Meta:
		model=User
		fields=['id','User_otp']