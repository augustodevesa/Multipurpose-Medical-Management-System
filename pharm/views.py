from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .forms import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib import messages
from user.models import User,User_reports,User_doctor_case,User_medicine,Lab_report_files,User_doctor_consultancy
from user.models import *
# from doctor.models import Doctor,Doctor_fb,DoctorLog
# from user.models import User_fb,User,UserLog 
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
				return render(request,'dashboard/pharm/register.html',{'form':loginForm,'message':'passwords does not match'})
			objects = Pharm.objects.all()
			for elt in objects:
				if elt.email==request.POST['email']:
					return render(request,'dashboard/pharm/register.html',{'form':loginForm,'message':'Already Email Registered'}) 
				if elt.user_name==request.POST['user_name']:
					return render(request,'dashboard/pharm/register.html',{'form':loginForm,'message':'Already user_name Registered'})
			otp_user=str(generateOTP())
			otp_email=request.POST['email']
			otp_name=request.POST['pharm_name']
			login_entry=Pharm(
	            pharm_name=request.POST['pharm_name'],
	            user_name=request.POST['user_name'],
	            email=request.POST['email'],
	            password=request.POST['password1'],
	            created_at=datetime.datetime.now(),
	            updated_at=datetime.datetime.now(),
	            pharm_address=request.POST['pharm_address'],
	            pharm_contact_number=request.POST['pharm_contact_number'],
	            User_progress=0,
	            pharm_verified=False,
	            User_otp=otp_user, )
			login_entry.user_photo=loginForm.cleaned_data['user_photo']
			login_entry.cert_image=loginForm.cleaned_data['cert_image']
			login_entry.save()
			send_email_str=str(otp_name)+"The OTP for your Health id is "+str(otp_user)
			send_email(str(otp_email),"UIMPR Authetication OTP",send_email_str)
			return redirect('/pharm/login')
		else:
			return render(request,'dashboard/pharm/register.html',{'form':loginForm,'message':'Invalid Detail'})
	loginForm=Register()
	return render(request,'dashboard/pharm/register.html',{'form':loginForm,'message':''})
def login(request):
	if request.method == 'GET':
		if 'pharm_name_' in request.session:
			username = request.session['pharm_name_']
			return redirect('dashboard/'+username)
		loginForm=Login()
		return render(request,'dashboard/pharm/login.html',{'form':loginForm,'message':'Please Login'})
	if request.method == "POST":
		loginForm=Login(request.POST)
		if loginForm.is_valid():
			try:
				m=Pharm.objects.get(email=loginForm.cleaned_data["email"],password=loginForm.cleaned_data["password"])
				if m.User_progress=='0':
					request.session['pharmverify']=m.user_name
					return redirect('user_verify_email/'+m.user_name)
				if m.pharm_verified==False:
					return render(request,'dashboard/pharm/login.html',{'form':loginForm,'message':'You are still not verified'})
				request.session['pharm_name_']=m.user_name
				user_log_entry=PharmLog(uid=m.id,user_name=m.user_name,userip=get_client_ip(request),loginTime=datetime.datetime.now(),success=False)
				user_log_entry.save()
				return redirect('dashboard/'+m.user_name)
			except ObjectDoesNotExist as e:
				return render(request,'dashboard/pharm/login.html',{'form':loginForm,'message':'Incorrect Credentials'})
		else:
			return render(request,'dashboard/pharm/login.html',{'form':loginForm,'message':'Invalid Captcha'})
	loginForm=Login()
	return render(request,'dashboard/pharm/login.html',{'form':loginForm})
def user_verify_email(request,user):
	try:
		if 'pharmverify' in request.session:
			if user==request.session['pharmverify']:
				m=Pharm.objects.get(user_name=user)
				if request.method=='POST':
					Verify_form=email_verify(request.POST)
					if Verify_form.is_valid():
						try:
							otp_p=request.POST['User_otp']
							if otp_p==m.User_otp:
								m.User_progress=1
								request.session['pharm_name_']=m.user_name
								user_log_entry=PharmLog(uid=m.id,user_name=m.user_name,userip=get_client_ip(request),loginTime=datetime.datetime.now(),success=False)
								user_log_entry.save()
								m.save()
								return redirect('/pharm/dashboard/'+m.user_name)
							else:
								return render(request,'dashboard/pharm/email_verify.html',{'message':'Wrong OTP','user':m})
						except Exception as e:
							return HttpResponse(e)
					else:
						return render(request,'dashboard/pharm/email_verify.html',{'message':'Invalid Form','user':m})
				loginForm=email_verify()
				return render(request,'dashboard/pharm/email_verify.html',{'message':'Enter OTP Details','form':loginForm,'user':m})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def regenerate_otp(request,user):
	try:
		if 'pharmverify' in request.session:
			if user==request.session['pharmverify']:
				user_=str(request.GET.get('user_name', None))
				if user==user_:
					m=Pharm.objects.get(user_name=user)
					otp_user=str(generateOTP())
					otp_email=m.email
					otp_name=m.pharm_name
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
		if 'pharmverify' in request.session:
			if user==request.session['pharmverify']:
				user_=str(request.POST.get('email', None))
				objects = Pharm.objects.only("email")
				for elt in objects:
					if elt.email==request.POST['email']:
						response_data = {}
						response_data['result'] = "Already Email Registered"
						return JsonResponse(response_data) 
				m=Pharm.objects.get(user_name=user)
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
		if 'pharm_name_' in request.session:
			if user==request.session['pharm_name_']:
				m=Pharm.objects.get(user_name=user)
				return render(request,'dashboard/pharm/index.html',{'user':m})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def logout(request,user):
	try:
		if 'pharm_name_' in request.session:
			if user==request.session['pharm_name_']:
				user_log_entry=PharmLog.objects.filter(user_name=user).order_by('-id')[0]
				user_log_entry.logoutTime=datetime.datetime.now()
				user_log_entry.success=True
				user_log_entry.save()
				# del request.session['username']
				request.session.flush()
				return redirect('/pharm/login')
	except  Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to Logout 2")
def activity_log(request,user):
	try:
		if 'pharm_name_' in request.session:
			if user==request.session['pharm_name_']:
				m=Pharm.objects.get(user_name=user)
				user_log_entry=PharmLog.objects.filter(user_name=user).order_by('id')
				return render(request,'dashboard/pharm/activity_log.html',{'user':m,'user_log':user_log_entry})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def profile(request,user):
	try:
		if 'pharm_name_' in request.session:
			if user==request.session['pharm_name_']:
				m=Pharm.objects.get(user_name=user)
				return render(request,'dashboard/pharm/profile.html',{'user':m})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def settings(request,user):
	m=Pharm.objects.get(user_name=user)
	# try:
	if 'pharm_name_' in request.session:
		if user==request.session['pharm_name_']:
			if request.method == "POST":
				loginForm=Update_user(request.POST, request.FILES)
				if loginForm.is_valid():
					objects = Pharm.objects.all()
					for elt in objects:
						if elt.user_name==request.POST['user_name']:
							if elt.user_name !=m.user_name:
								return render(request,'dashboard/pharm/settings.html',{'form':loginForm,'message':'Already user_name Registered','user':m})
					login_entry=Pharm.objects.get(user_name=user)
					login_entry.pharm_name=request.POST['pharm_name']
					login_entry.user_name=request.POST['user_name']
					login_entry.updated_at=datetime.datetime.now()
					login_entry.user_photo=loginForm.cleaned_data['user_photo']
					login_entry.cert_image=loginForm.cleaned_data['cert_image']
					login_entry.pharm_address=loginForm.cleaned_data['pharm_address']
					login_entry.pharm_contact_number=loginForm.cleaned_data['pharm_contact_number']
					login_entry.save()
					return render(request,'dashboard/pharm/settings.html',{'form':loginForm,'message':'SuccessFul Updation','user':m})
				else:
					return render(request,'dashboard/pharm/settings.html',{'form':loginForm,'message':'Invalid Detail','user':m})
			loginForm=Update_user()
			return render(request,'dashboard/pharm/settings.html',{'form':loginForm,'message':'Please Update Details','user':m})
	# except Exception as e:
	# 	return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def chg_passwd(request,user):
	m=Pharm.objects.get(user_name=user)
	# try:
	if 'pharm_name_' in request.session:
		if user==request.session['pharm_name_']:
			if request.method == "POST":
				loginForm=Change_Password(request.POST)
				if loginForm.is_valid():
					if m.password!=request.POST['password']:
						return render(request,'dashboard/pharm/chg_passwd.html',{'form':loginForm,'message':'Your Original password does not match'})
					if request.POST['password1']!=request.POST['password2']:
						return render(request,'dashboard/pharm/chg_passwd.html',{'form':loginForm,'message':'passwords does not match'})
					m.password=request.POST['password1']
					m.updated_at=datetime.datetime.now()
					m.save()
					return render(request,'dashboard/pharm/chg_passwd.html',{'form':loginForm,'message':'SuccessFul Updation','user':m})
				else:
					return render(request,'dashboard/pharm/chg_passwd.html',{'form':loginForm,'message':'Invalid Detail','user':m})
			loginForm=Change_Password()
			return render(request,'dashboard/pharm/chg_passwd.html',{'form':loginForm,'message':'Please Update Details','user':m})
	# except Exception as e:
	# 	return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def forgot_pass(request):
	if request.method == "POST":
		forgotForm=forgot_pass_form(request.POST)
		if forgotForm.is_valid():
			try:
				m=Pharm.objects.get(email=forgotForm.cleaned_data["email"])
				request.session['forget-pass']=m.user_name
				otp_user=str(generateOTP())
				otp_email=m.email
				otp_name=m.pharm_name
				send_email_str=str(otp_name)+"The OTP for your Health id is "+str(otp_user)
				send_email(str(otp_email),"UIMPR Authetication OTP",send_email_str)
				m.User_otp=otp_user
				m.save()
				return redirect('forgot_pass_chg/'+m.user_name)
			except ObjectDoesNotExist as e:
				return render(request,'dashboard/pharm/forgot_pass.html',{'form':forgotForm,'message':'Incorrect Credentials'})
		else:
			return render(request,'dashboard/pharm/forgot_pass.html',{'form':forgotForm,'message':'Invalid Captcha'})
	forgotForm=forgot_pass_form()
	return render(request,'dashboard/pharm/forgot_pass.html',{'form':forgotForm,'message':'Please Enter Details'})
def forgot_pass_chg(request,user):
	if request.method == 'GET':
		try:
			if 'forget-pass' in request.session:
				if user==request.session['forget-pass']:
					m=Pharm.objects.get(user_name=user)
					forgetForm=forgot_pass_form_chg()
					return render(request,'dashboard/pharm/forgot_pass_chg.html',{'form':forgetForm,'message':'Enter password Details','user':m})
		except Exception as e:
			return HttpResponse(e)
	if request.method == "POST":
		try:
			if 'forget-pass' in request.session:
				if user==request.session['forget-pass']:
					m=Pharm.objects.get(user_name=user)
					forgetForm=forgot_pass_form_chg(request.POST)
					if forgetForm.is_valid():
						if forgetForm.cleaned_data['password1']!=forgetForm.cleaned_data['password2']:
							return render(request,'dashboard/pharm/forgot_pass_chg.html',{'form':forgetForm,'message':'passwords does not match'})
						if m.User_otp.strip()==forgetForm.cleaned_data['User_otp'].strip():
							m.password=forgetForm.cleaned_data['password1']
							m.updated_at=datetime.datetime.now()
							m.User_progress=1
							request.session.flush()
							m.save()
							return redirect('/pharm/login')
					return render(request,'dashboard/pharm/forgot_pass_chg.html',{'form':forgetForm,'message':'Invalid Captcha'})
		except Exception as e:
			return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def givefeed(request,user):
	m=Pharm.objects.get(user_name=user)
	if 'pharm_name_' in request.session:
		if user==request.session['pharm_name_']:
			if request.method == "POST":
				uform=lab_feedback_form(request.POST)
				if uform.is_valid():
					feedback_entry=Pharm_fb(uid=m.id,user_name=m.user_name,created_at=datetime.datetime.now(),\
						content=uform.cleaned_data['content'],subject=uform.cleaned_data['subject'])
					feedback_entry.save()
					return render(request,'dashboard/pharm/givefeed.html',{'form':uform,'message':'SuccessFul Updation','user':m})
				else:
					return render(request,'dashboard/pharm/givefeed.html',{'form':uform,'message':'Invalid Detail','user':m})
			uform=lab_feedback_form()
			return render(request,'dashboard/pharm/givefeed.html',{'form':uform,'message':'Please Update Fill Form. Once Done cannot be \
				undone','user':m})
	# except Exception as e:
	# 	return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def showfeed(request,user):
	m=Pharm.objects.get(user_name=user)
	if 'pharm_name_' in request.session:
		if user==request.session['pharm_name_']:
			try:
				ftb=Pharm_fb.objects.filter(user_name=user)
				return render(request,'dashboard/pharm/showfeed.html',{'user':m,'ftable':ftb})
			except Exception as e:
				return render(request,'dashboard/pharm/showfeed.html',{'user':m})
	# 	return HttpResponse(e)	
	# except Exception as e:
	# 	return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def takepatient(request,user):
    m=Pharm.objects.get(user_name=user)
    if 'pharm_name_' in request.session:
        if user==request.session['pharm_name_']:
            # try:
                if request.method=='POST':
                    lab_consult_user_login_f=pharm_consult_user_login(request.POST)
                    if lab_consult_user_login_f.is_valid():
                        try:
                            user_id=request.POST['id']
                            t=User.objects.get(user_name=user_id)
                            # from dateutil import tz
                            # india_tz= tz.gettz('Asia/Kolkata')
                            time_now=datetime.datetime.now(datetime.timezone.utc)
                            # time_now=time_now.astimezone(india_tz)
                            time_db=t.User_otp_created
                            # time_db=time_db.astimezone(india_tz)
                            time_db=time_db-datetime.timedelta(hours=5, minutes=30)
                            time_diff=time_now-time_db
                            # print(time_now,time_db,time_diff.seconds)
                            if time_diff.seconds>660:
                                return render(request,'dashboard/pharm/takepatient.html',{'user':m,'message':"Regenerate OTP,it has lapsed 10 minutes span"})
                            if t.User_otp==lab_consult_user_login_f.cleaned_data['User_otp']:
                                t.User_otp=None
                                t.save()
                                request.session['lab_user_login']=t.user_name
                                return redirect('/pharm/enter_case/'+m.user_name)
                            return render(request,'dashboard/pharm/takepatient.html',{'user':m,'message':"OTP Incorrect"})
                        except ObjectDoesNotExist as e:
                            return render(request,'dashboard/pharm/takepatient.html',{'user':m,'message':"Invalid UserID"})
                    return render(request,'dashboard/pharm/takepatient.html',{'user':m,'message':"Invalid Details"})
                return render(request,'dashboard/pharm/takepatient.html',{'user':m,'message':""})
            # except Exception as e:
            #     return render(request,'dashboard/doctor/takepatient.html',{'user':m,'message':e})
    return HttpResponse("Not Eligible to View 2")
def takepatient_otp_user(request,user):
    m=Pharm.objects.get(user_name=user)
    if 'pharm_name_' in request.session:
        if user==request.session['pharm_name_']:
            try:
                user_id=str(request.POST.get('userid', None))
                try:
                    t=User.objects.get(user_name=user_id)
                    if t.User_progress==0:
                        response_data = {}
                        response_data['result'] = "User's Email address is yet to be verified"
                        return JsonResponse(response_data)
                    try:
                        kkk=User_medical.objects.get(user=t)
                    except ObjectDoesNotExist as e:
                        response_data = {}
                        response_data['result'] = "User's Has not filled Basic Details"
                        return JsonResponse(response_data)
                    otp_user=str(generateOTP())
                    otp_email=t.email
                    otp_name=t.firstname+" "+t.lastname
                    send_email_str="Mr./Mrs. "+str(otp_name)+" the OTP for your Health id is "+str(otp_user)+" reffered by Pharm . "+m.pharm_name
                    send_email(str(otp_email),"UIMPR Authetication for user approval OTP",send_email_str)
                    t.User_otp=otp_user
                    t.User_otp_created=datetime.datetime.now()
                    t.save()
                    response_data = {}
                    response_data['result'] = "Successed Otp send to "+str(otp_name)+" at "+str(datetime.datetime.now())
                    return JsonResponse(response_data)
                except ObjectDoesNotExist as e:
                    response_data = {}
                    response_data['result'] = "User Name does'nt exist"
                    return JsonResponse(response_data)
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"+request.session
    return JsonResponse(response_data)
def enter_case(request,user):
    m=Pharm.objects.get(user_name=user)
    if 'pharm_name_' in request.session:
        if user==request.session['pharm_name_']:
            User_e=User.objects.get(user_name=request.session['lab_user_login'])
            user_case_e=User_doctor_case.objects.filter(user=User_e)
            ii=[]
            for z in user_case_e:
	            User_doctor_cons_e=User_doctor_consultancy.objects.filter(user_case=z)
	            t=[]
	            for x in User_doctor_cons_e:
	                User_medicine_e=User_medicine.objects.filter(use_consult=x,is_delivered=False)
	                rr=[]
	                for ee in User_medicine_e:
	                	rr.append(ee)
	                t.append(rr)
	            ii.append(t)
            return render(request,'dashboard/pharm/enter_case.html',{'user':m,'message':"",'medicines':ii,'user_user':User_e})
    return HttpResponse("Not Eligible to View 2")
def medicine_deliver(request,user):
    m=Pharm.objects.get(user_name=user)
    if 'pharm_name_' in request.session:
        if user==request.session['pharm_name_']:
            try:
                caseid=request.POST.get('caseid',None)
                User_medicine_e=User_medicine.objects.get(id=caseid)
                User_medicine_e.is_delivered=True
                User_medicine_e.save()
                Lab_rec_e=Pharm_rec(pharmacist=m,user_cons=User_medicine_e.use_consult)
                Lab_rec_e.save()
                response_data = {}
                response_data['result'] = "Medicine of request with caseid "+caseid+" approved"
                return JsonResponse(response_data)
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"+request.session
    return JsonResponse(response_data)
def prev_cases(request,user):
    m=Pharm.objects.get(user_name=user)
    if 'pharm_name_' in request.session:
        if user==request.session['pharm_name_']:
            Pharm_rec_e=Pharm_rec.objects.filter(pharmacist=m)
            t=[]
            for z in Pharm_rec_e:
            	User_medicine_e=User_medicine.objects.filter(use_consult=z.user_cons)
            	t.append(User_medicine_e)
            return render(request,'dashboard/pharm/prev_cases.html',{'user':m,'message':"",'ftable':Pharm_rec_e,'medicines':t})
    return HttpResponse("Not Eligible to View 2")
