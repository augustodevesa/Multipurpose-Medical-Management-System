from django import forms
from .models import Pharm,Pharm_fb
from captcha.fields import CaptchaField
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _
class Login(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = Pharm
		fields=['email','password']
		widgets = {
		'password': forms.PasswordInput(),
	}
class Register(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	captcha = CaptchaField()
	class Meta:
		model = Pharm
		exclude=['created_at','updated_at','password','User_progress','User_otp','User_otp_created']
class Update_user(forms.ModelForm):
	class Meta:
		model = Pharm
		exclude=['created_at','updated_at','password','email','User_progress','User_otp','User_otp_created']
class Change_Password(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = Pharm
		fields=['password']
class forgot_pass_form(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = Pharm
		fields=['email']
class forgot_pass_form_chg(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	captcha = CaptchaField()
	class Meta:
		model = Pharm
		fields=['User_otp']
class email_verify(forms.ModelForm):
	class Meta:
		model = Pharm
		fields=['User_otp']
class lab_feedback_form(forms.ModelForm):
	class Meta:
		model= Pharm_fb
		fields=['content','subject']
class pharm_consult_user_login(forms.ModelForm):
	class Meta:
		model=Pharm
		fields=['id','User_otp']