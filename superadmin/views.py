from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .forms import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib import messages
from doctor.models import *
from user.models import *
from lab.models import *
from pharm.models import *
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
def get_sympt_by_id(id_list):
    list_ret=[]
    for iid in id_list:
        temp1=Symptoms.objects.get(id=iid)
        list_ret.append(temp1.name)
    return list_ret
def get_dis_by_id(id_list):
    list_ret=[]
    for iid in id_list:
        temp1=Diseases.objects.get(id=iid)
        list_ret.append(temp1.name)
    return list_ret
def get_inj_by_id(id_list):
    list_ret=[]
    for iid in id_list:
        temp1=Injury.objects.get(id=iid)
        list_ret.append(temp1.name)
    return list_ret

def register(request):
	if request.method == "POST":
		loginForm=Register(request.POST, request.FILES)
		if loginForm.is_valid():
			if request.POST['password1']!=request.POST['password2']:
				return render(request,'dashboard/superadmin/register.html',{'form':loginForm,'message':'passwords does not match'})
			objects = Superadmin.objects.all()
			for elt in objects:
				if elt.email==request.POST['email']:
					return render(request,'dashboard/superadmin/register.html',{'form':loginForm,'message':'Already Email Registered'}) 
				if elt.user_name==request.POST['user_name']:
					return render(request,'dashboard/superadmin/register.html',{'form':loginForm,'message':'Already user_name Registered'})
			otp_user=str(generateOTP())
			otp_email=request.POST['email']
			otp_name=request.POST['firstname']+request.POST['lastname']
			login_entry=Superadmin(
	            firstname=request.POST['firstname'],	
	            lastname=request.POST['lastname'],
	            user_name=request.POST['user_name'],
	            email=request.POST['email'],
	            password=request.POST['password1'],
	            dateofBirth=request.POST['dateofBirth'],
	            created_at=datetime.datetime.now(),
	            updated_at=datetime.datetime.now(),
	            User_progress=0,
	            User_otp=otp_user, )
			login_entry.user_photo=loginForm.cleaned_data['user_photo']
			login_entry.save()
			send_email_str=str(otp_name)+"The OTP for your Health id is "+str(otp_user)
			send_email(str(otp_email),"UIMPR Authetication OTP",send_email_str)
			return redirect('/superadmin/login')
		else:
			return render(request,'dashboard/superadmin/register.html',{'form':loginForm,'message':'Invalid Detail'})
	loginForm=Register()
	return render(request,'dashboard/superadmin/register.html',{'form':loginForm,'message':'Please Login'})
def login(request):
	if request.method == 'GET':
		if 'superadmin_name' in request.session:
			username = request.session['superadmin_name']
			redirect('dashboard/'+username)
		loginForm=Login()
		return render(request,'dashboard/superadmin/login.html',{'form':loginForm,'message':'Please Login'})
	if request.method == "POST":
		loginForm=Login(request.POST)
		if loginForm.is_valid():
			try:
				m=Superadmin.objects.get(email=loginForm.cleaned_data["email"],password=loginForm.cleaned_data["password"])
				
				if m.User_progress=='0':
					request.session['superadminverify']=m.user_name
					return redirect('user_verify_email/'+m.user_name)
				request.session['superadmin_name']=m.user_name
				user_log_entry=SuperadminLog(uid=m.id,user_name=m.user_name,userip=get_client_ip(request),loginTime=datetime.datetime.now(),success=False)
				user_log_entry.save()
				return redirect('dashboard/'+m.user_name)
			except ObjectDoesNotExist as e:
				return render(request,'dashboard/superadmin/login.html',{'form':loginForm,'message':'Incorrect Credentials'})
		else:
			return render(request,'dashboard/superadmin/login.html',{'form':loginForm,'message':'Invalid Captcha'})
	loginForm=Login()
	return render(request,'dashboard/superadmin/login.html',{'form':loginForm})
def user_verify_email(request,user):
	try:
		if 'superadminverify' in request.session:
			if user==request.session['superadminverify']:
				m=Superadmin.objects.get(user_name=user)
				if request.method=='POST':
					Verify_form=email_verify(request.POST)
					if Verify_form.is_valid():
						try:
							otp_p=request.POST['User_otp']
							if otp_p==m.User_otp:
								m.User_progress=1
								request.session['superadmin_name']=m.user_name
								user_log_entry=SuperadminLog(uid=m.id,user_name=m.user_name,userip=get_client_ip(request),loginTime=datetime.datetime.now(),success=False)
								user_log_entry.save()
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
def regenerate_otp(request,user):
	try:
		if 'superadminverify' in request.session:
			if user==request.session['superadminverify']:
				user_=str(request.GET.get('user_name', None))
				if user==user_:
					m=Superadmin.objects.get(user_name=user)
					otp_user=str(generateOTP())
					otp_email=m.email
					otp_name=m.firstname+" "+m.lastname
					send_email_str=str(otp_name)+"The OTP for your Health id is "+str(otp_user)
					send_email(str(otp_email),"UIMPR Authetication OTP",send_email_str)
					m.User_otp=otp_user
					m.save()
					response_data = {}
					response_data['result'] = " Otp sent successfully"
					return JsonResponse(response_data)
		response_data = {}
		response_data['result'] = "Authorization Breach"
		return JsonResponse(response_data)
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def otp_email_chg(request,user):
	try:
		if 'superadminverify' in request.session:
			if user==request.session['superadminverify']:
				user_=str(request.POST.get('email', None))
				objects = Superadmin.objects.only("email")
				for elt in objects:
					if elt.email==request.POST['email']:
						response_data = {}
						response_data['result'] = "Already Email Registered"
						return JsonResponse(response_data) 
				m=Superadmin.objects.get(user_name=user)
				m.email=user_
				m.save()
				response_data = {}
				response_data['result'] = "Successed Email Change"
				return JsonResponse(response_data)
		response_data = {}
		response_data['result'] = "Authorization Breach"
		return JsonResponse(response_data)
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def dashboard(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				return render(request,'dashboard/superadmin/index.html',{'user':m})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def logout(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				user_log_entry=SuperadminLog.objects.filter(user_name=user).order_by('-id')[0]
				user_log_entry.logoutTime=datetime.datetime.now()
				user_log_entry.success=True
				user_log_entry.save()
				# del request.session['username']
				request.session.flush()
				return redirect('/superadmin/login')
	except  Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to Logout 2")
def activity_log(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				user_log_entry=SuperadminLog.objects.filter(user_name=user).order_by('id')
				return render(request,'dashboard/superadmin/activity_log.html',{'user':m,'user_log':user_log_entry})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def profile(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				return render(request,'dashboard/superadmin/profile.html',{'user':m})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def settings(request,user):
	m=Superadmin.objects.get(user_name=user)
	# try:
	if 'superadmin_name' in request.session:
		if user==request.session['superadmin_name']:
			if request.method == "POST":
				loginForm=Update_user(request.POST, request.FILES)
				if loginForm.is_valid():
					objects = Superadmin.objects.all()
					for elt in objects:
						# print(type(elt),elt.email)
						if elt.user_name==request.POST['user_name']:
							if elt.user_name !=m.user_name:
								return render(request,'dashboard/superadmin/settings.html',{'form':loginForm,'message':'Already user_name Registered','user':m})
					login_entry=Superadmin.objects.get(user_name=user)
					login_entry.firstname=request.POST['firstname']	
					login_entry.lastname=request.POST['lastname']
					login_entry.user_name=request.POST['user_name']
					login_entry.dateofBirth=request.POST['dateofBirth']
					login_entry.updated_at=datetime.datetime.now()
					login_entry.user_photo=loginForm.cleaned_data['user_photo']
					login_entry.save()
					return render(request,'dashboard/superadmin/settings.html',{'form':loginForm,'message':'SuccessFul Updation','user':m})
				else:
					return render(request,'dashboard/superadmin/settings.html',{'form':loginForm,'message':'Invalid Detail','user':m})
			loginForm=Update_user()
			return render(request,'dashboard/superadmin/settings.html',{'form':loginForm,'message':'Please Update Details','user':m})
	# except Exception as e:
	# 	return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def chg_passwd(request,user):
	m=Superadmin.objects.get(user_name=user)
	# try:
	if 'superadmin_name' in request.session:
		if user==request.session['superadmin_name']:
			if request.method == "POST":
				loginForm=Change_Password(request.POST)
				if loginForm.is_valid():
					if m.password!=request.POST['password']:
						return render(request,'dashboard/superadmin/chg_passwd.html',{'form':loginForm,'message':'Your Original passworddoes not match'})
					if request.POST['password1']!=request.POST['password2']:
						return render(request,'dashboard/superadmin/chg_passwd.html',{'form':loginForm,'message':'passwords does not match'})
					m.password=request.POST['password1']
					m.updated_at=datetime.datetime.now()
					m.save()
					return render(request,'dashboard/superadmin/chg_passwd.html',{'form':loginForm,'message':'SuccessFul Updation','user':m})
				else:
					return render(request,'dashboard/superadmin/chg_passwd.html',{'form':loginForm,'message':'Invalid Detail','user':m})
			loginForm=Change_Password()
			return render(request,'dashboard/superadmin/chg_passwd.html',{'form':loginForm,'message':'Please Update Details','user':m})
	# except Exception as e:
	# 	return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def forgot_pass(request):
	if request.method == "POST":
		forgotForm=forgot_pass_form(request.POST)
		if forgotForm.is_valid():
			try:
				m=Superadmin.objects.get(email=forgotForm.cleaned_data["email"],dateofBirth=forgotForm.cleaned_data['dateofBirth'])
				request.session['forget-pass']=m.user_name
				otp_user=str(generateOTP())
				otp_email=m.email
				otp_name=m.firstname+" "+m.lastname
				send_email_str=str(otp_name)+"The OTP for your Health id is "+str(otp_user)
				send_email(str(otp_email),"UIMPR Authetication OTP",send_email_str)
				m.User_otp=otp_user
				m.save()
				return redirect('forgot_pass_chg/'+m.user_name)
			except ObjectDoesNotExist as e:
				return render(request,'dashboard/superadmin/forgot_pass.html',{'form':forgotForm,'message':'Incorrect Credentials'})
		else:
			return render(request,'dashboard/superadmin/forgot_pass.html',{'form':forgotForm,'message':'Invalid Captcha'})
	forgotForm=forgot_pass_form()
	return render(request,'dashboard/superadmin/forgot_pass.html',{'form':forgotForm,'message':'Please Enter Details'})
def forgot_pass_chg(request,user):
	if request.method == 'GET':
		try:
			if 'forget-pass' in request.session:
				if user==request.session['forget-pass']:
					m=Superadmin.objects.get(user_name=user)
					forgetForm=forgot_pass_form_chg()
					return render(request,'dashboard/superadmin/forgot_pass_chg.html',{'form':forgetForm,'message':'Enter password Details','user':m})
		except Exception as e:
			return HttpResponse(e)
	if request.method == "POST":
		try:
			if 'forget-pass' in request.session:
				if user==request.session['forget-pass']:
					m=Superadmin.objects.get(user_name=user)
					forgetForm=forgot_pass_form_chg(request.POST)
					if forgetForm.is_valid():
						if forgetForm.cleaned_data['password1']!=forgetForm.cleaned_data['password2']:
							return render(request,'dashboard/superadmin/forgot_pass_chg.html',{'form':forgetForm,'message':'passwords does not match'})
						if m.User_otp.strip()==forgetForm.cleaned_data['User_otp'].strip():
							m.password=forgetForm.cleaned_data['password1']
							m.updated_at=datetime.datetime.now()
							m.User_progress=1
							request.session.flush()
							m.save()
							return redirect('/superadmin/login')
					return render(request,'dashboard/superadmin/forgot_pass_chg.html',{'form':forgetForm,'message':'Invalid Captcha'})
		except Exception as e:
			return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def approveDoctor(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=Doctor.objects.filter(doctor_verified=False)
				return render(request,'dashboard/superadmin/approve_doctor.html',{'user':m,'doctor':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def approveDoctorAJAX(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				doctor_id=request.GET.get('DoctorId', None)
				approval_status=request.GET.get('Approve', None)
				if approval_status=='Y':
					t=Doctor.objects.get(doctor_verified=False,id=doctor_id)
					t.doctor_verified=True
					otp_email=t.email
					otp_name="Dr."+t.firstname+" "+t.lastname
					send_email_str=str(otp_name)+" we have activated your account.You can login again at any time"
					send_email(str(otp_email),"UIMPR Activation for doctor",send_email_str)
					t.save()
					response_txt={
						'data':str('Doctor having DoctorId'+doctor_id+' is Approved')
					}

					return JsonResponse(response_txt)
				else:
					t=Doctor.objects.get(doctor_verified=False,id=doctor_id)
					t.doctor_verified=False
					# t.delete()
					otp_email=t.email
					otp_name="Dr."+t.firstname+" "+t.lastname
					send_email_str=str(otp_name)+", due to failure in verification of your data, we have deleted your account.You can register again at any time"
					send_email(str(otp_email),"UIMPR Deactivation for doctor",send_email_str)
					# t.save()
					response_txt={
						'data':('Doctor having DoctorId'+doctor_id+' is Disapproved and deleted')
					}
					return JsonResponse(response_txt)
	except Exception as e:
		print(e)
		return HttpResponse(e)
	print(user,"Not Eligible to View 2")
	return HttpResponse("Not Eligible to View 2")
def manageDoctorAJAX(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				doctor_id=request.GET.get('DoctorId', None)
				approval_status=request.GET.get('Approve', None)
				if approval_status=='Y':
					t=Doctor.objects.get(id=doctor_id)
					print(t.doctor_verified)
					t.doctor_verified=False
					print(t.doctor_verified)
					otp_email=t.email
					otp_name="Dr."+t.firstname+" "+t.lastname
					send_email_str=str(otp_name)+", due to failure in verification of your data, we have unverified your account.It has been added to pending approval"
					send_email(str(otp_email),"UIMPR Deactivation for doctor",send_email_str)
					t.save()
					response_txt={
						'data':str('Doctor having DoctorId'+doctor_id+' is Approved')
					}
					print(t.doctor_verified)

					return JsonResponse(response_txt)
				else:
					t=Doctor.objects.get(doctor_verified=False,id=doctor_id)
					t.doctor_verified=False
					# t.delete()
					otp_email=t.email
					otp_name="Dr."+t.firstname+" "+t.lastname
					send_email_str=str(otp_name)+", due to failure in verification of your data, we have deleted your account.You can register again at any time"
					send_email(str(otp_email),"UIMPR Deactivation for doctor",send_email_str)
					t.save()
					response_txt={
						'data':('Doctor having DoctorId'+doctor_id+' is Disapproved and deleted')
					}
					return JsonResponse(response_txt)
	except Exception as e:
		print(e)
		return HttpResponse(e)
	print(user,"Not Eligible to View 2")
	return HttpResponse("Not Eligible to View 2")



def user_feedback(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=User_fb.objects.all()
				return render(request,'dashboard/superadmin/user_feedback.html',{'user':m,'user_feedback':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")

def user_session(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=UserLog.objects.all()
				return render(request,'dashboard/superadmin/user_session.html',{'user':m,'user_session':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def doctor_feedback(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=Doctor_fb.objects.all()
				return render(request,'dashboard/superadmin/doctor_feedback.html',{'user':m,'user_feedback':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")

def doctor_session(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=DoctorLog.objects.all()
				return render(request,'dashboard/superadmin/doctor_session.html',{'user':m,'user_session':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")

def lab_feedback(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=Lab_fb.objects.all()
				return render(request,'dashboard/superadmin/lab_feedback.html',{'user':m,'user_feedback':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")

def lab_sesssion(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=LabLog.objects.all()
				return render(request,'dashboard/superadmin/lab_sesssion.html',{'user':m,'user_session':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def pharm_feedback(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=Pharm_fb.objects.all()
				return render(request,'dashboard/superadmin/pharm_feedback.html',{'user':m,'user_feedback':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")

def pharm_session(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=PharmLog.objects.all()
				return render(request,'dashboard/superadmin/pharm_session.html',{'user':m,'user_session':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def manage_users(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=User.objects.all()
				return render(request,'dashboard/superadmin/manage_users.html',{'user':m,'user_user':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")

def manage_usersAJAX(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				UserId=request.GET.get('UserId', None)
				t=User.objects.get(id=UserId)
				otp_email=t.email
				otp_name="Mr./Mrs."+t.firstname+" "+t.lastname
				send_email_str=str(otp_name)+", due to failure in verification of your data, we have deleted your account.You can register again at any time"
				send_email(str(otp_email),"UIMPR Deactivation of account",send_email_str)
				################################################################################ t.delete()
				response_txt={
					'data':str('User '+t.firstname+' '+t.lastname+' having UserId '+UserId+' is Deleted')
				}
				return JsonResponse(response_txt)
	except Exception as e:
		print(e)
		return HttpResponse(e)
	print(user,"Not Eligible to View 2")
	return HttpResponse("Not Eligible to View 2")
def manage_doctors(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=Doctor.objects.all()
				return render(request,'dashboard/superadmin/manage_doctors.html',{'user':m,'doctor':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def user_emergency(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=User_contacts.objects.all()
				return render(request,'dashboard/superadmin/user_emergency.html',{'user':m,'user_emergency':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def user_health(request,user):
    try:
        if 'superadmin_name' in request.session:
            if user==request.session['superadmin_name']:
                m=Superadmin.objects.get(user_name=user)
                import json
                cases_=User_doctor_case.objects.all()
                # print(cases_)
                for i in range(len(cases_)):
                    if cases_[i].symptoms !=None:
                        y = json.loads(cases_[i].symptoms)
                        z=get_sympt_by_id(y)
                        cases_[i].symptoms=z
                    else:
                        cases_[i].symptoms=None
                    if cases_[i].diseases !=None:
                        y = json.loads(cases_[i].diseases)
                        z=get_dis_by_id(y)
                        cases_[i].diseases=z
                    else:
                        cases_[i].diseases=None
                    if cases_[i].injury_type !=None:
                        y = json.loads(cases_[i].injury_type)
                        z=get_inj_by_id(y)
                        cases_[i].injury_type=z
                    else:
                        cases_[i].injury_type=None
                return render(request,'dashboard/superadmin/user_health.html',{'user':m,'cases_':cases_})
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("Not Eligible to View 2")
def approveLab(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=Lab.objects.filter(lab_verified=False)
				return render(request,'dashboard/superadmin/approve_lab.html',{'user':m,'user_user':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def manage_labs(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=Lab.objects.all()
				return render(request,'dashboard/superadmin/manage_labs.html',{'user':m,'user_user':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def approvePharm(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=Pharm.objects.all()
				return render(request,'dashboard/superadmin/approve_pharm.html',{'user':m,'user_user':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def manage_pharms(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				m=Superadmin.objects.get(user_name=user)
				t=Pharm.objects.all()
				return render(request,'dashboard/superadmin/manage_pharms.html',{'user':m,'user_user':t})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def getajaxlab(request,user):
    m=Superadmin.objects.get(user_name=user)
    if 'superadmin_name' in request.session:
        if user==request.session['superadmin_name']:
            try:
                case_id=str(request.POST.get('case_id', None))
                User_reports_q=User_reports.objects.filter(user_case=case_id)
                t=[]
                for y in User_reports_q:
                    r={}
                    r['name']=y.name
                    if y.ref_date!=None:
                        r['ref_date']=str(y.ref_date.date())
                    else:
                        r['ref_date']=None
                    if y.deliv_date!=None:
                        r['deliv_date']=str(y.deliv_date.date())
                    else:
                        r['deliv_date']=None                        
                    # r['deliv_date']=str(y.deliv_date)
                    r['is_delivered']=y.is_delivered
                    r['lab_desc']=y.lab_desc
                    Lab_report_files_e=Lab_report_files.objects.filter(user_report=y)
                    temp_f=[]
                    for z in Lab_report_files_e:
                        temp_f.append(z.lab_files.url)
                    r['files']=temp_f
                    t.append(r)
                import json     
                t  = json.dumps(t)
                response_data = {}
                response_data["result"] =t
                return JsonResponse(response_data)                
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"
    return JsonResponse(response_data)
def get_cons_medicine(request,user):
    m=Superadmin.objects.get(user_name=user)
    if 'superadmin_name' in request.session:
        if user==request.session['superadmin_name']:
            try:
                case_id=str(request.GET.get('case_id', None))
                User_doctor_consultancy_q=User_doctor_consultancy.objects.filter(user_case=case_id)
                t=[]
                for x in User_doctor_consultancy_q:
                    cons_id=User_medicine.objects.filter(use_consult=x)
                    for y in cons_id:
                        r={}
                        r['medicine_name']=y.medicine_name
                        r['dosage']=y.dosage
                        r['quantity']=y.quantity
                        r['is_delivered']=y.is_delivered
                        t.append(r)
                import json     
                t  = json.dumps(t)
                response_data = {}
                response_data["result"] =t
                return JsonResponse(response_data)                
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"
    return JsonResponse(response_data)
def get_cons_doc(request,user):
    m=Superadmin.objects.get(user_name=user)
    if 'superadmin_name' in request.session:
        if user==request.session['superadmin_name']:
            try:
                case_id=str(request.GET.get('case_id', None))
                User_doctor_consultancy_q=User_doctor_consultancy.objects.filter(user_case=case_id)
                # lisT_ans=""
                import json
                # for i in range(len(User_doctor_consultancy_q)):
                #   lisT_ans+=str(x.logoutTime)
                #   print(x.logoutTime)
                for i in range(len(User_doctor_consultancy_q)):
                    if User_doctor_consultancy_q[i].symptoms !=None:
                        y = json.loads(User_doctor_consultancy_q[i].symptoms)
                        z=get_sympt_by_id(y)
                        User_doctor_consultancy_q[i].symptoms=z
                    else:
                        User_doctor_consultancy_q[i].symptoms=None
                    if User_doctor_consultancy_q[i].diseases !=None:
                        y = json.loads(User_doctor_consultancy_q[i].diseases)
                        z=get_dis_by_id(y)
                        User_doctor_consultancy_q[i].diseases=z
                    else:
                        User_doctor_consultancy_q[i].diseases=None
                    if User_doctor_consultancy_q[i].injury_type !=None:
                        y = json.loads(User_doctor_consultancy_q[i].injury_type)
                        z=get_inj_by_id(y)
                        User_doctor_consultancy_q[i].injury_type=z
                    else:
                        User_doctor_consultancy_q[i].injury_type=None

                from django.core import serializers
                User_doctor_consultancy_q_S = serializers.serialize("json", User_doctor_consultancy_q)
                response_data = {}
                response_data["result"] =User_doctor_consultancy_q_S
                return JsonResponse(response_data)                
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"
    return JsonResponse(response_data)
def approveLabAJAX(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				doctor_id=request.GET.get('DoctorId', None)
				approval_status=request.GET.get('Approve', None)
				print(doctor_id,approval_status)
				if approval_status=='Y':
					t=Lab.objects.get(lab_verified=False,id=doctor_id)

					t.lab_verified=True
					otp_email=t.email
					otp_name=t.lab_name
					send_email_str=str(otp_name)+"we have activated your account.You can login again at any time"
					send_email(str(otp_email),"UIMPR Activation for pathologist",send_email_str)
					t.save()
					response_txt={
						'data':str('Pathologist having id'+doctor_id+' is Approved')
					}
					print(t.lab_verified,response_txt);

					return JsonResponse(response_txt)
				else:
					t=Doctor.objects.get(doctor_verified=False,id=doctor_id)
					t.doctor_verified=False
					# t.delete()
					otp_email=t.email
					otp_name=t.lab_name
					send_email_str=str(otp_name)+", due to failure in verification of your data, we have deleted your account.You can register again at any time"
					send_email(str(otp_email),"UIMPR Deactivation for pathologist",send_email_str)
					# t.save()
					response_txt={
						'data':('Pathologist having is'+doctor_id+' is Disapproved and deleted')
					}
					return JsonResponse(response_txt)
	except Exception as e:
		print(e)
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def manageLabAJAX(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				doctor_id=request.GET.get('DoctorId', None)
				approval_status=request.GET.get('Approve', None)
				if approval_status=='Y':
					t=Lab.objects.get(id=doctor_id)
					t.lab_verified=False
					otp_email=t.email
					otp_name=t.lab_name
					send_email_str=str(otp_name)+", due to failure in verification of your data, we have unverified your account.It has been added to pending approval"
					send_email(str(otp_email),"UIMPR Deactivation for Pathologist",send_email_str)
					t.save()
					response_txt={
						'data':str('Pathologist having id'+doctor_id+' is deactivated')
					}
					print(t.lab_verified)

					return JsonResponse(response_txt)
				else:
					t=Lab.objects.get(id=doctor_id)
					t.lab_verified=False
					# t.delete()
					otp_email=t.email
					otp_name=t.lab_name
					send_email_str=str(otp_name)+", due to failure in verification of your data, we have deleted your account.You can register again at any time"
					send_email(str(otp_email),"UIMPR Deactivation for Pathologist",send_email_str)
					t.save()
					response_txt={
						'data':('Pathologist having id'+doctor_id+' is Disapproved and deleted')
					}
					return JsonResponse(response_txt)
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def approvePharmAJAX(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				doctor_id=request.GET.get('DoctorId', None)
				approval_status=request.GET.get('Approve', None)
				if approval_status=='Y':
					t=Pharm.objects.get(pharm_verified=False,id=doctor_id)

					t.pharm_verified=True
					otp_email=t.email
					otp_name=t.pharm_name
					send_email_str=str(otp_name)+"we have activated your account.You can login again at any time"
					send_email(str(otp_email),"UIMPR Activation for pathologist",send_email_str)
					t.save()
					response_txt={
						'data':str('Pharmacist having id'+doctor_id+' is Approved')
					}

					return JsonResponse(response_txt)
				else:
					t=Pharm.objects.get(pharm_verified=False,id=doctor_id)
					t.pharm_verified=False
					# t.delete()
					otp_email=t.email
					otp_name=t.pharm_name
					send_email_str=str(otp_name)+", due to failure in verification of your data, we have deleted your account.You can register again at any time"
					send_email(str(otp_email),"UIMPR Deactivation for pathologist",send_email_str)
					# t.save()
					response_txt={
						'data':('Pharmacist having is'+doctor_id+' is Disapproved and deleted')
					}
					return JsonResponse(response_txt)
	except Exception as e:
		print(e)
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def managePharmAJAX(request,user):
	try:
		if 'superadmin_name' in request.session:
			if user==request.session['superadmin_name']:
				doctor_id=request.GET.get('DoctorId', None)
				approval_status=request.GET.get('Approve', None)
				if approval_status=='Y':
					t=Pharm.objects.get(id=doctor_id)
					t.pharm_verified=False
					otp_email=t.email
					otp_name=t.pharm_name
					send_email_str=str(otp_name)+", due to failure in verification of your data, we have unverified your account.It has been added to pending approval"
					send_email(str(otp_email),"UIMPR Deactivation for Pathologist",send_email_str)
					t.save()
					response_txt={
						'data':str('Pathologist having id'+doctor_id+' is deactivated')
					}

					return JsonResponse(response_txt)
				else:
					t=Pharm.objects.get(id=doctor_id)
					t.pharm_verified=False
					# t.delete()
					otp_email=t.email
					otp_name=t.pharm_name
					send_email_str=str(otp_name)+", due to failure in verification of your data, we have deleted your account.You can register again at any time"
					send_email(str(otp_email),"UIMPR Deactivation for Pathologist",send_email_str)
					t.save()
					response_txt={
						'data':('Pathologist having id'+doctor_id+' is Disapproved and deleted')
					}
					return JsonResponse(response_txt)
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
