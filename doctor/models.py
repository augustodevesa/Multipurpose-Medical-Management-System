from django.db import models
from django.core.validators import RegexValidator
class DoctorLog(models.Model):
	uid=models.IntegerField(blank=False)
	user_name=models.CharField(max_length=50,blank=False)
	userip=models.CharField(max_length=50)
	loginTime= models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=False)
	logoutTime= models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=True,null=True)
	success=models.BooleanField()
class Doctor(models.Model):
	firstname=models.CharField(max_length=50, blank=False)
	lastname=models.CharField(max_length=50, blank=False)
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
		('O','Other'),
		)
	gender=models.CharField(max_length=1,choices=GENDER_CHOICES,blank=False)
	created_at = models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=False)
	updated_at = models.DateTimeField('%m/%d/%Y %H:%M:%S')
	user_name=models.CharField(max_length=50,blank=False)
	country=models.CharField(max_length=50,blank=False)
	state=models.CharField(max_length=50,blank=False)
	district=models.CharField(max_length=50,blank=False)
	city=models.CharField(max_length=50,blank=False)
	area=models.CharField(max_length=50,blank=False)
	society=models.CharField(max_length=50)
	landmark=models.CharField(max_length=50)
	house_no=models.CharField(max_length=50)
	pincode=models.IntegerField(blank=False)
	blood_group=models.CharField(max_length=5)
	aadhar_card_no=models.CharField(max_length=12, validators=[RegexValidator(r'^\d{0,12}$')],blank=False)
	dateofBirth=models.DateField('%d/%m/%Y')
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	email = models.EmailField(max_length = 70,blank=False)
	password = models.CharField(max_length = 50,blank=False)
	user_photo = models.ImageField(upload_to = 'pictures/doctor/doctor_img')
	DOCTOR_LEVEL_DEGREE = (
		('B', 'Bachelor Degree'),
		('M', 'Masters Degree'),
		('P','Ph.D Degree'),
		('S','Super Specialist'),
		)
	doctor_specialization_level=models.CharField(max_length=1,choices=DOCTOR_LEVEL_DEGREE,blank=False)
	doctor_degree_name=models.CharField(max_length=50)
	doctor_license_no=models.CharField(max_length=50)
	doctor_hospital_name=models.CharField(max_length=50)
	doctor_specialization_field=models.CharField(max_length=50)
	doctor_degree_cert = models.ImageField(upload_to = 'pictures/doctor/doctor_degree_cert')
	doctor_licencse_cert= models.ImageField(upload_to = 'pictures/doctor/doctor_licencse_cert')
	doctor_verified=models.BooleanField()
	User_progress=models.CharField(max_length=10,null=True)
	User_otp=models.CharField(max_length=10,null=True)
	User_otp_created=models.DateTimeField('%m/%d/%Y %H:%M:%S',null=True)
	class Meta:
		db_table = "Doctor_check"
class Doctor_fb(models.Model):
	uid=models.IntegerField(blank=False)
	user_name=models.CharField(max_length=50,blank=False)
	created_at= models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=False)
	content = models.TextField()
	subject=models.CharField(max_length=50,blank=False)
class SymptomCat(models.Model):
	name=models.CharField(max_length=50)
	doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
	description=models.CharField(max_length=100)
class Symptoms(models.Model):
	doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
	name=models.CharField(max_length=50)
	alternate_names=models.CharField(max_length=100)
	Symptomcat=models.ForeignKey(SymptomCat, on_delete=models.CASCADE)
	description=models.CharField(max_length=100)
class DiseaseCat(models.Model):
	name=models.CharField(max_length=50)
	doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
	description=models.CharField(max_length=100)
class Diseases(models.Model):
	doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
	name=models.CharField(max_length=50)
	alternate_names=models.CharField(max_length=100)
	DiseaseCat=models.ForeignKey(DiseaseCat, on_delete=models.CASCADE)
	description=models.CharField(max_length=100)
	DISEASE_SEVERITY = (
		('Ordinary', 'Ordinary'),
		('Communicable', 'Communicable'),
		('Threat_to_region','Threat_to_region'),
		('Threat_to_country','Threat_to_country'),
		('Threat_to_humanity','Threat_to_humanity'),
		)
	disease_intensity=models.CharField(max_length=25,choices=DISEASE_SEVERITY)
class Injury(models.Model):
	doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
	description=models.CharField(max_length=100)
	name=models.CharField(max_length=50)
	alternate_names=models.CharField(max_length=100)
	Injury_SEVERITY = (
		('Ordinary', 'Ordinary'),
		('highly_severe', 'highly_severe'),
		('capable_of_handicapping','capable_of_handicapping'),
		('Life_threatning','Life_threatning'),
		)
	disease_intensity=models.CharField(max_length=25,choices=Injury_SEVERITY)



