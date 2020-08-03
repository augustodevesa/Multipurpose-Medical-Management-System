from django import forms
from .models import Doctor,Doctor_fb
from user.models import User
from captcha.fields import CaptchaField
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _
class Login(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = Doctor
		fields=['email','password']
		widgets = {
		'password': forms.PasswordInput(),
	}

class Register(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	captcha = CaptchaField()
	class Meta:
		model = Doctor
		exclude=['created_at','updated_at','password','doctor_verified','User_progress','User_otp','User_otp_created']
class Update_user(forms.ModelForm):
	class Meta:
		model = Doctor
		exclude=['created_at','updated_at','password','email','User_progress','User_otp','User_otp_created','doctor_degree_name','doctor_license_no','doctor_degree_cert','doctor_licencse_cert','doctor_verified','doctor_specialization_level']
class Change_Password(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = Doctor
		fields=['password']
class forgot_pass_form(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = Doctor
		fields=['email','dateofBirth']
class forgot_pass_form_chg(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	captcha = CaptchaField()
	class Meta:
		model = Doctor
		fields=['User_otp']
class email_verify(forms.ModelForm):
	class Meta:
		model = Doctor
		fields=['User_otp']
class doctor_feedback_form(forms.ModelForm):
	class Meta:
		model= Doctor_fb
		fields=['content','subject']
class doctor_consult_user_login(forms.ModelForm):
	class Meta:
		model=User
		fields=['id','User_otp']