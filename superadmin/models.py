from django.db import models
class SuperadminLog(models.Model):
	uid=models.IntegerField(blank=False)
	user_name=models.CharField(max_length=50,blank=False)
	userip=models.CharField(max_length=50)
	loginTime= models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=False)
	logoutTime= models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=True,null=True)
	success=models.BooleanField()

# Create your models here.
class Superadmin(models.Model):
	firstname=models.CharField(max_length=50, blank=False)
	lastname=models.CharField(max_length=50, blank=False)
	created_at = models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=False)
	updated_at = models.DateTimeField('%m/%d/%Y %H:%M:%S')
	user_name=models.CharField(max_length=50,blank=False)
	email = models.EmailField(max_length = 70,blank=False)
	password = models.CharField(max_length = 50,blank=False)
	user_photo = models.ImageField(upload_to = 'pictures/superadmin/superadmin_img')
	User_progress=models.CharField(max_length=10,null=True)
	User_otp=models.CharField(max_length=10,null=True)
	dateofBirth=models.DateField('%d/%m/%Y')
	User_otp_created=models.DateTimeField('%m/%d/%Y %H:%M:%S',null=True)
	class Meta:
		db_table = "superadmin_check"