from django.db import models

# Create your models here.
class LabLog(models.Model):
	uid=models.IntegerField(blank=False)
	lab_name=models.CharField(max_length=50,blank=False)
	labip=models.CharField(max_length=50)
	loginTime= models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=False)
	logoutTime= models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=True,null=True)
	success=models.BooleanField()

# Create your models here.
class Lab(models.Model):
	lab_name=models.CharField(max_length=75, blank=False)
	created_at = models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=False)
	updated_at = models.DateTimeField('%m/%d/%Y %H:%M:%S')
	lab_email = models.EmailField(max_length = 70,blank=False)
	lab_password = models.CharField(max_length = 50,blank=False)
	lab_image = models.ImageField(upload_to = 'pictures/lab/lab_img')
	lab_address=models.TextField()
    lab_certificate_image = models.ImageField(upload_to = 'pictures/lab/lab_certificate_image')
	lab_progress=models.CharField(max_length=10,null=True)
	lab_otp=models.CharField(max_length=10,null=True)
	lab_otp_created=models.DateTimeField('%m/%d/%Y %H:%M:%S',null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	lab_contact_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	lab_hospital_association=models.BooleanField()
    associated_hospital_name=models.CharField(max_length=75, blank=False)
    associated_hospital_address=models.TextField()
	class Meta:
		db_table = "lab_check"