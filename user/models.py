from django.db import models
from django.core.validators import RegexValidator
from doctor.models import Doctor
class UserLog(models.Model):
	uid=models.IntegerField(blank=False)
	user_name=models.CharField(max_length=50,blank=False)
	userip=models.CharField(max_length=50)
	loginTime= models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=False)
	logoutTime= models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=True,null=True)
	success=models.BooleanField()
class User(models.Model):
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
	user_photo = models.ImageField(upload_to = 'pictures/user/user_img')
	# secret_que=models.CharField(max_length=100)
	# secret_ans=models.CharField(max_length=100)
	User_progress=models.CharField(max_length=10,null=True)
	User_otp=models.CharField(max_length=10,null=True)
	User_otp_created=models.DateTimeField('%m/%d/%Y %H:%M:%S',null=True)
	class Meta:
		db_table = "User_check"
class User_fb(models.Model):
	uid=models.IntegerField(blank=False)
	user_name=models.CharField(max_length=50,blank=False)
	created_at= models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=False)
	content = models.TextField()
	subject=models.CharField(max_length=50,blank=False)
class User_contacts(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    email=models.EmailField(max_length=50,null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    address=models.TextField()
    PARENTS='PR'
    RELATIONSHIP = [
        ('SB', 'Sibling/Cousin'),
        ('PR', 'Parents'),
        ('RL', 'Relative'),
        ('FR', 'Friend'),
        ('NG', 'Neighbour'),
        ('OT', 'Other'),
    ]
    # family_doctor=models.CharField(max_length=50)
    phone_number_2 = models.CharField(validators=[phone_regex], max_length=17, null=True) # validators should be a list
    relationship=models.CharField(max_length=2,choices=RELATIONSHIP,default=PARENTS)

class User_medical(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	height=models.IntegerField(null=True)#in CM
	weight=models.IntegerField(null=True)#in Kgs
	MARTIAL_STATUS = (
		('S', 'Single'),
		('M', 'Married'),
		('D','Divorced'),
		('W','Widowed'),
		)
	martial_s=models.CharField(max_length=1,choices=MARTIAL_STATUS)
	disability_status=models.BooleanField()
	DISABILITY_TYPE = (
		('VI', 'Vision Impairment'),
		('DF', 'Deaf or Hard of hearing'),
		('MH','Mental health Conditions'),
		('ID','Intellectual Disability'),
		('AB','Acquired Brain Injury'),
		('AS','Autism Spectrum Disorder'),
		('PD','Physical Disability'),
		('OT','Other'),
		)
	disability_type=models.CharField(max_length=2,choices=DISABILITY_TYPE,null=True)
	disability_other=models.CharField(max_length=50,null=True)
	pregnency=models.BooleanField()
	RATING = (
		('0','Severe'),
		('1','Bad'),
		('2','OK'),
		('3','Good'),
		('4','Very good'),
		)
	vision=models.CharField(max_length=1,choices=RATING)
	alcohol=models.CharField(max_length=1,choices=RATING)
	smoking=models.CharField(max_length=1,choices=RATING)
	drugs=models.CharField(max_length=1,choices=RATING)
	color_vison=models.CharField(max_length=1,choices=RATING)
	masturbating=models.CharField(max_length=1,choices=RATING)
	other_imp_details=models.TextField(null=True)
	other_details=models.TextField(null=True)
	updated_at = models.DateTimeField('%m/%d/%Y %H:%M:%S')
	# DISEASE_CHOICE=(
	# 	('Y','YES'),
	# 	('N','NO not having'),
	# 	('O','Not knowing'),
	# 	)
	
class User_surgery(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	surgery_type=models.CharField(max_length=50)
	surgery_description=models.TextField(null=True)
	dateofSurgery=models.DateField('%d/%m/%Y')
	surgery_file=models.FileField(upload_to = 'documents/user/surgery')
	hospital_name=models.CharField(max_length=50)
	hospital_location=models.CharField(max_length=50)
class User_doctor_case(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	symptoms=models.TextField(null=True)#with Rating from 1-5
	general_notes=models.TextField(null=True)
	diseases=models.TextField(null=True)
	is_accidental=models.BooleanField()
	injury_type=models.TextField(null=True)
	is_closed=models.BooleanField(null=True)
class User_doctor_consultancy(models.Model):
	user_case=models.ForeignKey(User_doctor_case, on_delete=models.CASCADE)
	doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
	loginTime= models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=False)
	logoutTime= models.DateTimeField('%m/%d/%Y %H:%M:%S',blank=True,null=True)
	success=models.BooleanField()
	symptoms=models.TextField(null=True)#with Rating from 1-5
	personal_notes=models.TextField(null=True)
	general_notes=models.TextField(null=True)
	diseases=models.TextField(null=True)
	is_accidental=models.BooleanField()
	injury_type=models.TextField(null=True)
class User_medicine(models.Model):
	use_consult=models.ForeignKey(User_doctor_consultancy, on_delete=models.CASCADE)
	medicine_name=models.CharField(max_length=50)
	dosage=models.CharField(max_length=50)
	quantity=models.CharField(max_length=50)
	is_delivered=models.BooleanField(default=False)
class User_medicine_own(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	medicine_name=models.CharField(max_length=50)
	dosage=models.CharField(max_length=50)
	quantity=models.CharField(max_length=50)
class User_allergy(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	allergy_name=models.CharField(max_length=50)
class User_reports(models.Model):
	user_case=models.ForeignKey(User_doctor_case, on_delete=models.CASCADE)
	name=models.CharField(max_length=50)
	doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
	ref_date= models.DateTimeField('%m/%d/%Y %H:%M:%S',null=True)
	deliv_date= models.DateTimeField('%m/%d/%Y %H:%M:%S',null=True)
	is_delivered=models.BooleanField(default=False)
	lab_desc=models.TextField(null=True)
class Lab_report_files(models.Model):
	user_report=models.ForeignKey(User_reports, on_delete=models.CASCADE)
	lab_files=models.FileField(upload_to = 'documents/user/lab_reports')
class User_parameters(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	param_name=models.CharField(max_length=50)
	param_value=models.CharField(max_length=50)









