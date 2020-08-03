from django.db import models
from django.core.validators import RegexValidator
from user.models import User_reports
class LabLog(models.Model):
	uid=models.IntegerField(blank=False)
	user_name=models.CharField(max_length=50,blank=False)
	userip=models.CharField(max_length=50)
	loginTime= models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=False)
	logoutTime= models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=True,null=True)
	success=models.BooleanField()

# Create your models here.
class Lab(models.Model):
	lab_name=models.CharField(max_length=50, blank=False)
	created_at = models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=False)
	updated_at = models.DateTimeField('%m/%d/%Y %H:%M:%S')
	user_name=models.CharField(max_length=50,blank=False)
	email = models.EmailField(max_length = 70,blank=False)
	password = models.CharField(max_length = 50,blank=False)
	user_photo = models.ImageField(upload_to = 'pictures/lab/lab_img')
	cert_image = models.ImageField(upload_to = 'pictures/lab/cert_image')
	User_progress=models.CharField(max_length=10,null=True)
	User_otp=models.CharField(max_length=10,null=True)
	User_otp_created=models.DateTimeField('%m/%d/%Y %H:%M:%S',null=True)
	lab_address=models.TextField()
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	lab_contact_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	lab_verified=models.BooleanField()
class Lab_fb(models.Model):
	uid=models.IntegerField(blank=False)
	user_name=models.CharField(max_length=50,blank=False)
	created_at= models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=False)
	content = models.TextField()
	subject=models.CharField(max_length=50,blank=False)
class Lab_rec(models.Model):
	user_report=models.ForeignKey(User_reports, on_delete=models.CASCADE)
	pathologist=models.ForeignKey(Lab, on_delete=models.CASCADE)
	status=models.BooleanField()
