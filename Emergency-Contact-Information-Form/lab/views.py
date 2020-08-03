from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .forms import Login,Register,Update_lab,Change_Password,forgot_pass_form_chg,forgot_pass_form,lab_email_verify
from .models import Lab,LabLog
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib import messages
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create your views here.
def send_email(receiver_address,subject,mail_content):
	sender_address = 'healthp74@gmail.com'
	sender_pass = '123@mohit'
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = receiver_address
	message['Subject'] = str(subject)
	message.attach(MIMEText(mail_content, 'plain'))
	#Create SMTP session for sending the mail
	session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
	session.starttls() #enable security
	session.login(sender_address, sender_pass) #login with mail_id and password
	text = message.as_string()
	session.sendmail(sender_address, receiver_address, text)
	session.quit()

def generateOTP() :
	import math,random 
	digits = "0123456789"
	OTP = "" 
	for i in range(4) : 
	    OTP += digits[math.floor(random.random() * 10)]   
	return OTP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def register(request):
	if request.method == "POST":
		loginForm=Register(request.POST, request.FILES)
		if loginForm.is_valid():
			if request.POST['password1']!=request.POST['password2']:
				return render(request,'dashboard/lab/register.html',{'form':loginForm,'message':'passwords does not match'})
			objects = Lab.objects.all()
			for elt in objects:
				if elt.lab_email==request.POST['lab_email']:
					return render(request,'dashboard/lab/register.html',{'form':loginForm,'message':'Already Email Registered'}) 
				if elt.lab_name==request.POST['lab_name']:
					return render(request,'dashboard/lab/register.html',{'form':loginForm,'message':'Already Lab Registered'})
			otp_lab=str(generateOTP())
			otp_email=request.POST['lab_email']
			otp_name=request.POST['lab_name']
			login_entry=Lab(
	            lab_name=request.POST['lab_name'],	
	            lab_email=request.POST['email'],
	            lab_password=request.POST['password1'],
	            created_at=datetime.datetime.now(),
	            updated_at=datetime.datetime.now(),
	            lab_progress=0,
	            lab_otp=otp_user,
				lab_address=request.POST['lab_address'],
				lab_contact_number=request.POST['lab_contact_number'],
				lab_hospital_association=request.POST['lab_hospital_association'],
				associated_hospital_name=request.POST['associated_hospital_name'],
				associated_hospital_address=request.POST['associated_hospital_address'],
			  )
			login_entry.lab_image=loginForm.cleaned_data['lab_image']
			login_entry.lab_certificate_image=loginForm.cleaned_data['lab_certificate_image']
			login_entry.save()
			send_email_str=str(otp_name)+"The OTP for your Health Lab id is "+str(otp_lab)
			send_email(str(otp_email),"UIMPR Authetication OTP",send_email_str)
			return redirect('/lab/login')
		else:
			return render(request,'dashboard/lab/register.html',{'form':loginForm,'message':'Invalid Details'})
	loginForm=Register()
	return render(request,'dashboard/lab/register.html',{'form':loginForm,'message':'Please Login'})

def login(request):
	if request.method == 'GET':
		if 'lab_name' in request.session:
			username = request.session['lab_name']
			return redirect('dashboard/'+username)
		loginForm=Login()
		return render(request,'dashboard/lab/login.html',{'form':loginForm,'message':'Please Login'})
	if request.method == "POST":
		loginForm=Login(request.POST)
		if loginForm.is_valid():
			try:
				m=Lab.objects.get(lab_email=loginForm.cleaned_data["lab_email"],lab_password=loginForm.cleaned_data["lab_password"])			
				if m.lab_progress=='0':
					request.session['labverify']=m.lab_name
					return redirect('lab_verify_email/'+m.lab_name)
				request.session['lab_name']=m.lab_name
				lab_log_entry=LabLog(uid=m.id,lab_name=m.lab_name,labip=get_client_ip(request),loginTime=datetime.datetime.now(),success=False)
				lab_log_entry.save()
				return redirect('dashboard/'+m.lab_name)
			except ObjectDoesNotExist as e:
				return render(request,'dashboard/lab/login.html',{'form':loginForm,'message':'Incorrect Credentials'})
		else:
			return render(request,'dashboard/lab/login.html',{'form':loginForm,'message':'Invalid Captcha'})
	loginForm=Login()
	return render(request,'dashboard/lab/login.html',{'form':loginForm})

def lab_verify_email(request,lab):
	try:
		if 'labverify' in request.session:
			if lab==request.session['labverify']:
				m=Lab.objects.get(lab_name=lab)
				if request.method=='POST':
					Verify_form=email_verify(request.POST)
					if Verify_form.is_valid():
						try:
							otp_p=request.POST['lab_otp']
							if otp_p==m.lab_otp:
								m.lab_progress=1
								request.session['superadmin_name']=m.user_name
								m.save()
								return redirect('/superadmin/dashboard/'+m.user_name)
							else:
								return render(request,'dashboard/superadmin/email_verify.html',{'message':'Wrong OTP','user':m})
						except Exception as e:
							return HttpResponse(e)
					else:
						return render(request,'dashboard/superadmin/email_verify.html',{'message':'Invalid Form','user':m})
				loginForm=email_verify()
				return render(request,'dashboard/superadmin/email_verify.html',{'message':'Enter OTP Details','form':loginForm,'user':m})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
