from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .forms import Login,Register,Update_user,Change_Password,forgot_pass_form_chg,forgot_pass_form,doctor_feedback_form,email_verify,doctor_consult_user_login
from .models import Doctor,DoctorLog,Doctor_fb,SymptomCat,Symptoms,DiseaseCat,Diseases,Injury
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib import messages
import smtplib
import pgeocode
from user.models import User,User_doctor_consultancy,User_doctor_case,User_medical,User_surgery,User_contacts,User_medicine,User_medicine_own,User_reports,Lab_report_files
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

isoCountries = {
    'AF' : 'Afghanistan',
    'AX' : 'Aland Islands',
    'AL' : 'Albania',
    'DZ' : 'Algeria',
    'AS' : 'American Samoa',
    'AD' : 'Andorra',
    'AO' : 'Angola',
    'AI' : 'Anguilla',
    'AQ' : 'Antarctica',
    'AG' : 'Antigua And Barbuda',
    'AR' : 'Argentina',
    'AM' : 'Armenia',
    'AW' : 'Aruba',
    'AU' : 'Australia',
    'AT' : 'Austria',
    'AZ' : 'Azerbaijan',
    'BS' : 'Bahamas',
    'BH' : 'Bahrain',
    'BD' : 'Bangladesh',
    'BB' : 'Barbados',
    'BY' : 'Belarus',
    'BE' : 'Belgium',
    'BZ' : 'Belize',
    'BJ' : 'Benin',
    'BM' : 'Bermuda',
    'BT' : 'Bhutan',
    'BO' : 'Bolivia',
    'BA' : 'Bosnia And Herzegovina',
    'BW' : 'Botswana',
    'BV' : 'Bouvet Island',
    'BR' : 'Brazil',
    'IO' : 'British Indian Ocean Territory',
    'BN' : 'Brunei Darussalam',
    'BG' : 'Bulgaria',
    'BF' : 'Burkina Faso',
    'BI' : 'Burundi',
    'KH' : 'Cambodia',
    'CM' : 'Cameroon',
    'CA' : 'Canada',
    'CV' : 'Cape Verde',
    'KY' : 'Cayman Islands',
    'CF' : 'Central African Republic',
    'TD' : 'Chad',
    'CL' : 'Chile',
    'CN' : 'China',
    'CX' : 'Christmas Island',
    'CC' : 'Cocos (Keeling) Islands',
    'CO' : 'Colombia',
    'KM' : 'Comoros',
    'CG' : 'Congo',
    'CD' : 'Congo, Democratic Republic',
    'CK' : 'Cook Islands',
    'CR' : 'Costa Rica',
    'CI' : 'Cote D\'Ivoire',
    'HR' : 'Croatia',
    'CU' : 'Cuba',
    'CY' : 'Cyprus',
    'CZ' : 'Czech Republic',
    'DK' : 'Denmark',
    'DJ' : 'Djibouti',
    'DM' : 'Dominica',
    'DO' : 'Dominican Republic',
    'EC' : 'Ecuador',
    'EG' : 'Egypt',
    'SV' : 'El Salvador',
    'GQ' : 'Equatorial Guinea',
    'ER' : 'Eritrea',
    'EE' : 'Estonia',
    'ET' : 'Ethiopia',
    'FK' : 'Falkland Islands (Malvinas)',
    'FO' : 'Faroe Islands',
    'FJ' : 'Fiji',
    'FI' : 'Finland',
    'FR' : 'France',
    'GF' : 'French Guiana',
    'PF' : 'French Polynesia',
    'TF' : 'French Southern Territories',
    'GA' : 'Gabon',
    'GM' : 'Gambia',
    'GE' : 'Georgia',
    'DE' : 'Germany',
    'GH' : 'Ghana',
    'GI' : 'Gibraltar',
    'GR' : 'Greece',
    'GL' : 'Greenland',
    'GD' : 'Grenada',
    'GP' : 'Guadeloupe',
    'GU' : 'Guam',
    'GT' : 'Guatemala',
    'GG' : 'Guernsey',
    'GN' : 'Guinea',
    'GW' : 'Guinea-Bissau',
    'GY' : 'Guyana',
    'HT' : 'Haiti',
    'HM' : 'Heard Island & Mcdonald Islands',
    'VA' : 'Holy See (Vatican City State)',
    'HN' : 'Honduras',
    'HK' : 'Hong Kong',
    'HU' : 'Hungary',
    'IS' : 'Iceland',
    'IN' : 'India',
    'ID' : 'Indonesia',
    'IR' : 'Iran, Islamic Republic Of',
    'IQ' : 'Iraq',
    'IE' : 'Ireland',
    'IM' : 'Isle Of Man',
    'IL' : 'Israel',
    'IT' : 'Italy',
    'JM' : 'Jamaica',
    'JP' : 'Japan',
    'JE' : 'Jersey',
    'JO' : 'Jordan',
    'KZ' : 'Kazakhstan',
    'KE' : 'Kenya',
    'KI' : 'Kiribati',
    'KR' : 'Korea',
    'KW' : 'Kuwait',
    'KG' : 'Kyrgyzstan',
    'LA' : 'Lao People\'s Democratic Republic',
    'LV' : 'Latvia',
    'LB' : 'Lebanon',
    'LS' : 'Lesotho',
    'LR' : 'Liberia',
    'LY' : 'Libyan Arab Jamahiriya',
    'LI' : 'Liechtenstein',
    'LT' : 'Lithuania',
    'LU' : 'Luxembourg',
    'MO' : 'Macao',
    'MK' : 'Macedonia',
    'MG' : 'Madagascar',
    'MW' : 'Malawi',
    'MY' : 'Malaysia',
    'MV' : 'Maldives',
    'ML' : 'Mali',
    'MT' : 'Malta',
    'MH' : 'Marshall Islands',
    'MQ' : 'Martinique',
    'MR' : 'Mauritania',
    'MU' : 'Mauritius',
    'YT' : 'Mayotte',
    'MX' : 'Mexico',
    'FM' : 'Micronesia, Federated States Of',
    'MD' : 'Moldova',
    'MC' : 'Monaco',
    'MN' : 'Mongolia',
    'ME' : 'Montenegro',
    'MS' : 'Montserrat',
    'MA' : 'Morocco',
    'MZ' : 'Mozambique',
    'MM' : 'Myanmar',
    'NA' : 'Namibia',
    'NR' : 'Nauru',
    'NP' : 'Nepal',
    'NL' : 'Netherlands',
    'AN' : 'Netherlands Antilles',
    'NC' : 'New Caledonia',
    'NZ' : 'New Zealand',
    'NI' : 'Nicaragua',
    'NE' : 'Niger',
    'NG' : 'Nigeria',
    'NU' : 'Niue',
    'NF' : 'Norfolk Island',
    'MP' : 'Northern Mariana Islands',
    'NO' : 'Norway',
    'OM' : 'Oman',
    'PK' : 'Pakistan',
    'PW' : 'Palau',
    'PS' : 'Palestinian Territory, Occupied',
    'PA' : 'Panama',
    'PG' : 'Papua New Guinea',
    'PY' : 'Paraguay',
    'PE' : 'Peru',
    'PH' : 'Philippines',
    'PN' : 'Pitcairn',
    'PL' : 'Poland',
    'PT' : 'Portugal',
    'PR' : 'Puerto Rico',
    'QA' : 'Qatar',
    'RE' : 'Reunion',
    'RO' : 'Romania',
    'RU' : 'Russian Federation',
    'RW' : 'Rwanda',
    'BL' : 'Saint Barthelemy',
    'SH' : 'Saint Helena',
    'KN' : 'Saint Kitts And Nevis',
    'LC' : 'Saint Lucia',
    'MF' : 'Saint Martin',
    'PM' : 'Saint Pierre And Miquelon',
    'VC' : 'Saint Vincent And Grenadines',
    'WS' : 'Samoa',
    'SM' : 'San Marino',
    'ST' : 'Sao Tome And Principe',
    'SA' : 'Saudi Arabia',
    'SN' : 'Senegal',
    'RS' : 'Serbia',
    'SC' : 'Seychelles',
    'SL' : 'Sierra Leone',
    'SG' : 'Singapore',
    'SK' : 'Slovakia',
    'SI' : 'Slovenia',
    'SB' : 'Solomon Islands',
    'SO' : 'Somalia',
    'ZA' : 'South Africa',
    'GS' : 'South Georgia And Sandwich Isl.',
    'ES' : 'Spain',
    'LK' : 'Sri Lanka',
    'SD' : 'Sudan',
    'SR' : 'Suriname',
    'SJ' : 'Svalbard And Jan Mayen',
    'SZ' : 'Swaziland',
    'SE' : 'Sweden',
    'CH' : 'Switzerland',
    'SY' : 'Syrian Arab Republic',
    'TW' : 'Taiwan',
    'TJ' : 'Tajikistan',
    'TZ' : 'Tanzania',
    'TH' : 'Thailand',
    'TL' : 'Timor-Leste',
    'TG' : 'Togo',
    'TK' : 'Tokelau',
    'TO' : 'Tonga',
    'TT' : 'Trinidad And Tobago',
    'TN' : 'Tunisia',
    'TR' : 'Turkey',
    'TM' : 'Turkmenistan',
    'TC' : 'Turks And Caicos Islands',
    'TV' : 'Tuvalu',
    'UG' : 'Uganda',
    'UA' : 'Ukraine',
    'AE' : 'United Arab Emirates',
    'GB' : 'United Kingdom',
    'US' : 'United States',
    'UM' : 'United States Outlying Islands',
    'UY' : 'Uruguay',
    'UZ' : 'Uzbekistan',
    'VU' : 'Vanuatu',
    'VE' : 'Venezuela',
    'VN' : 'Viet Nam',
    'VG' : 'Virgin Islands, British',
    'VI' : 'Virgin Islands, U.S.',
    'WF' : 'Wallis And Futuna',
    'EH' : 'Western Sahara',
    'YE' : 'Yemen',
    'ZM' : 'Zambia',
    'ZW' : 'Zimbabwe'
};
def generateOTP() :
	import math,random 
	digits = "0123456789"
	OTP = "" 
	for i in range(4) : 
	    OTP += digits[math.floor(random.random() * 10)]   
	return OTP
def get_key(my_dict,val): 
    for key, value in my_dict.items(): 
         if val == value: 
             return key
    return None

# Create your views here.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def getselected_area(request):
   country=str(request.GET.get('country', None))
   pincode=str(request.GET.get('pincode', None))
   cnt=get_key(isoCountries,country)
   nomi = pgeocode.Nominatim(cnt)
   paal=nomi.query_postal_code(pincode).place_name.split(',')
   areas=[]
   for x in paal:
      # if typeof(x)=='string:
      areas.append(x.strip())
   coords=[nomi.query_postal_code(pincode).latitude,nomi.query_postal_code(pincode).longitude]
   response_data = {}
   response_data['result'] = areas
   response_data['coords'] = coords
   response_data['community_name'] = nomi.query_postal_code(pincode).community_name#Taluka
   response_data['county_name'] = nomi.query_postal_code(pincode).county_name#District Name
   response_data['state_name'] = nomi.query_postal_code(pincode).state_name
   response_data['lat']= str(nomi.query_postal_code(pincode).latitude)
   response_data['lon']= str(nomi.query_postal_code(pincode).longitude)
   response_data['accuracy']=str(nomi.query_postal_code(pincode).accuracy)
   return JsonResponse(response_data)

def register(request):
	if request.method == "POST":
		loginForm=Register(request.POST, request.FILES)
		if loginForm.is_valid():
			if request.POST['password1']!=request.POST['password2']:
				return render(request,'dashboard/doctor/register.html',{'form':loginForm,'message':'passwords does not match'})
			objects = Doctor.objects.all()
			for elt in objects:
				if elt.email==request.POST['email']:
					return render(request,'dashboard/doctor/register.html',{'form':loginForm,'message':'Already Email Registered'}) 
				if elt.user_name==request.POST['user_name']:
					return render(request,'dashboard/doctor/register.html',{'form':loginForm,'message':'Already user_name Registered'})
			otp_user=str(generateOTP())
			otp_email=request.POST['email']
			otp_name=request.POST['firstname']+request.POST['lastname']
			login_entry=Doctor(
	            firstname=request.POST['firstname'],	
	            lastname=request.POST['lastname'],
	            gender=request.POST['gender'],
	            user_name=request.POST['user_name'],
	            country=request.POST['country'],
	            state=request.POST['state'],
	            district=request.POST['district'],
	            city=request.POST['city'],
	            area=request.POST['area'],
	            society=request.POST['society'],
	            landmark=request.POST['landmark'],
	            house_no=request.POST['house_no'],
	            pincode=request.POST['pincode'],
	            blood_group=request.POST['blood_group'],
	            aadhar_card_no=request.POST['aadhar_card_no'],
	            dateofBirth=request.POST['dateofBirth'],
	            phone_number=request.POST['phone_number'],
	            email=request.POST['email'],
	            password=request.POST['password1'],
	            User_progress=0,
	            User_otp=otp_user,

	            doctor_specialization_level=request.POST['doctor_specialization_level'],
	            doctor_degree_name=request.POST['doctor_degree_name'],
	            doctor_license_no=request.POST['doctor_license_no'],
	            doctor_hospital_name=request.POST['doctor_hospital_name'],
	            doctor_specialization_field=request.POST['doctor_specialization_field'],            
	            doctor_verified=False,	

	            created_at=datetime.datetime.now(),
	            updated_at=datetime.datetime.now(), )
			login_entry.doctor_degree_cert=loginForm.cleaned_data['doctor_degree_cert']
			login_entry.doctor_licencse_cert=loginForm.cleaned_data['doctor_licencse_cert']
			login_entry.user_photo=loginForm.cleaned_data['user_photo']
			login_entry.save()
			send_email_str=str(otp_name)+"The OTP for your Health id is "+str(otp_user)
			send_email(str(otp_email),"UIMPR Authetication OTP",send_email_str)
			return redirect('/doctor/login')
		else:
			return render(request,'dashboard/doctor/register.html',{'form':loginForm,'message':'Invalid Detail'})
	loginForm=Register()
	cname=[]
	for y in isoCountries:
		cname.append(isoCountries[y])
	cname.sort()
	return render(request,'dashboard/doctor/register.html',{'form':loginForm,'message':'Please Fill the Details as required','country_drop':cname})
def login(request):
	if request.method == 'GET':
		if 'doctorname' in request.session:
			username = request.session['doctorname']
			return redirect('dashboard/'+username)
		loginForm=Login()
		return render(request,'dashboard/doctor/login.html',{'form':loginForm,'message':'Please Login'})
	if request.method == "POST":
		loginForm=Login(request.POST)
		if loginForm.is_valid():
			try:
				m=Doctor.objects.get(email=loginForm.cleaned_data["email"],password=loginForm.cleaned_data["password"])
				if m.User_progress=='0':
					request.session['doctorverify']=m.user_name
					return redirect('user_verify_email/'+m.user_name)
				if m.doctor_verified==False:
					return render(request,'dashboard/doctor/login.html',{'form':loginForm,'message':'You are still not verified'})
				request.session['doctorname']=m.user_name
				user_log_entry=DoctorLog(uid=m.id,user_name=m.user_name,userip=get_client_ip(request),loginTime=datetime.datetime.now(),success=False)
				user_log_entry.save()
				return redirect('dashboard/'+m.user_name)
			except ObjectDoesNotExist as e:
				return render(request,'dashboard/doctor/login.html',{'form':loginForm,'message':'Incorrect Credentials'})
		else:
			return render(request,'dashboard/doctor/login.html',{'form':loginForm,'message':'Invalid Captcha'})
	loginForm=Login()
	return render(request,'dashboard/doctor/login.html',{'form':loginForm})
def user_verify_email(request,user):
	try:
		if 'doctorverify' in request.session:
			if user==request.session['doctorverify']:
				m=Doctor.objects.get(user_name=user)
				if request.method=='POST':
					Verify_form=email_verify(request.POST)
					if Verify_form.is_valid():
						try:
							otp_p=request.POST['User_otp']
							if otp_p==m.User_otp:
								m.User_progress=1
								m.save()
								return redirect('/doctor/login')
							else:
								return render(request,'dashboard/doctor/email_verify.html',{'message':'Wrong OTP','user':m})
						except Exception as e:
							return HttpResponse(e)
					else:
						return render(request,'dashboard/doctor/email_verify.html',{'message':'Invalid Form','user':m})
				loginForm=email_verify()
				return render(request,'dashboard/doctor/email_verify.html',{'message':'Enter OTP Details','form':loginForm,'user':m})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def regenerate_otp(request,user):
	try:
		if 'doctorverify' in request.session:
			if user==request.session['doctorverify']:
				user_=str(request.GET.get('user_name', None))
				if user==user_:
					m=Doctor.objects.get(user_name=user)
					otp_user=str(generateOTP())
					otp_email=m.email
					otp_name=m.firstname+" "+m.lastname
					send_email_str=str(otp_name)+"The OTP for your Health id is "+str(otp_user)
					send_email(str(otp_email),"UIMPR Authetication OTP",send_email_str)
					m.User_otp=otp_user
					m.save()
					response_data = {}
					response_data['result'] = "Successed Otp send"
					return JsonResponse(response_data)
		response_data = {}
		response_data['result'] = "Authorization Breach"
		return JsonResponse(response_data)
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def otp_email_chg(request,user):
	try:
		if 'userverify' in request.session:
			if user==request.session['userverify']:
				user_=str(request.POST.get('email', None))
				objects = Doctor.objects.only("email")
				for elt in objects:
					if elt.email==request.POST['email']:
						response_data = {}
						response_data['result'] = "Already Email Registered"
						return JsonResponse(response_data) 
				m=User.objects.get(user_name=user)
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
		if 'doctorname' in request.session:
			if user==request.session['doctorname']:
				m=Doctor.objects.get(user_name=user)
				return render(request,'dashboard/doctor/index.html',{'user':m})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def logout(request,user):
	try:
		if 'doctorname' in request.session:
			if user==request.session['doctorname']:
				user_log_entry=DoctorLog.objects.filter(user_name=user).order_by('-id')[0]
				user_log_entry.logoutTime=datetime.datetime.now()
				user_log_entry.success=True
				user_log_entry.save()
				# del request.session['doctorname']
				request.session.flush()
				return redirect('/doctor/login')
	except  Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to Logout 2")
def activity_log(request,user):
	try:
		if 'doctorname' in request.session:
			if user==request.session['doctorname']:
				m=Doctor.objects.get(user_name=user)
				user_log_entry=DoctorLog.objects.filter(user_name=user).order_by('id')
				return render(request,'dashboard/doctor/activity_log.html',{'user':m,'user_log':user_log_entry})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def profile(request,user):
	try:
		if 'doctorname' in request.session:
			if user==request.session['doctorname']:
				m=Doctor.objects.get(user_name=user)
				return render(request,'dashboard/doctor/profile.html',{'user':m})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def settings(request,user):
	m=Doctor.objects.get(user_name=user)
	# try:
	if 'doctorname' in request.session:
		if user==request.session['doctorname']:
			if request.method == "POST":
				loginForm=Update_user(request.POST, request.FILES)
				if loginForm.is_valid():
					objects = Doctor.objects.all()
					for elt in objects:
						if elt.user_name==request.POST['user_name']:
							if elt.user_name !=m.user_name:
								return render(request,'dashboard/doctor/settings.html',{'form':loginForm,'message':'Already user_name Registered','user':m})
					login_entry=Doctor.objects.get(user_name=user)
					login_entry.firstname=request.POST['firstname']	
					login_entry.lastname=request.POST['lastname']
					login_entry.gender=request.POST['gender']
					login_entry.user_name=request.POST['user_name']
					login_entry.country=request.POST['country']
					login_entry.state=request.POST['state']
					login_entry.district=request.POST['district']
					login_entry.city=request.POST['city']
					login_entry.area=request.POST['area']
					login_entry.society=request.POST['society']
					login_entry.landmark=request.POST['landmark']
					login_entry.house_no=request.POST['house_no']
					login_entry.pincode=request.POST['pincode']
					login_entry.blood_group=request.POST['blood_group']
					login_entry.aadhar_card_no=request.POST['aadhar_card_no']
					login_entry.dateofBirth=request.POST['dateofBirth']
					login_entry.phone_number=request.POST['phone_number']

					# doctor_specialization_level=request.POST['doctor_specialization_level'],
					# doctor_degree_name=request.POST['doctor_degree_name']
					# doctor_license_no=request.POST['doctor_license_no']
					doctor_hospital_name=request.POST['doctor_hospital_name']
					doctor_specialization_field=request.POST['doctor_specialization_field']

					# doctor_degree_cert=loginForm.cleaned_data['doctor_degree_cert']
					# doctor_licencse_cert=loginForm.cleaned_data['doctor_licencse_cert']

					login_entry.updated_at=datetime.datetime.now()
					# print("check1")
					login_entry.user_photo=loginForm.cleaned_data['user_photo']
					# print("check2")
					login_entry.save()
					print("check3")
					return render(request,'dashboard/doctor/settings.html',{'form':loginForm,'message':'SuccessFul Updation','user':m})
				else:
					return render(request,'dashboard/doctor/settings.html',{'form':loginForm,'message':'Invalid Detail','user':m})
			loginForm=Update_user()
			
			return render(request,'dashboard/doctor/settings.html',{'form':loginForm,'message':'Please Update Details','user':m})
	# except Exception as e:
	# 	return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def chg_passwd(request,user):
	m=Doctor.objects.get(user_name=user)
	# try:
	if 'doctorname' in request.session:
		if user==request.session['doctorname']:
			if request.method == "POST":
				loginForm=Change_Password(request.POST)
				if loginForm.is_valid():
					if m.password!=request.POST['password']:
						return render(request,'dashboard/doctor/chg_passwd.html',{'form':loginForm,'message':'Your Original passworddoes not match'})
					if request.POST['password1']!=request.POST['password2']:
						return render(request,'dashboard/doctor/chg_passwd.html',{'form':loginForm,'message':'passwords does not match'})
					m.password=request.POST['password1']
					m.updated_at=datetime.datetime.now()
					m.save()
					return render(request,'dashboard/doctor/chg_passwd.html',{'form':loginForm,'message':'SuccessFul Updation','user':m})
				else:
					return render(request,'dashboard/doctor/chg_passwd.html',{'form':loginForm,'message':'Invalid Detail','user':m})
			loginForm=Change_Password()
			return render(request,'dashboard/doctor/chg_passwd.html',{'form':loginForm,'message':'Please Update Details','user':m})
	# except Exception as e:
	# 	return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def forgot_pass(request):
	if request.method == "POST":
		forgotForm=forgot_pass_form(request.POST)
		if forgotForm.is_valid():
			try:
				m=Doctor.objects.get(email=forgotForm.cleaned_data["email"],dateofBirth=forgotForm.cleaned_data['dateofBirth'])
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
				return render(request,'dashboard/doctor/forgot_pass.html',{'form':forgotForm,'message':'Incorrect Credentials'})
		else:
			return render(request,'dashboard/doctor/forgot_pass.html',{'form':forgotForm,'message':'Invalid Captcha'})
	forgotForm=forgot_pass_form()
	return render(request,'dashboard/doctor/forgot_pass.html',{'form':forgotForm,'message':'Please Enter Details'})

# def forgot_pass(request):
# 	if request.method == "POST":
# 		forgotForm=forgot_pass_form(request.POST)
# 		if forgotForm.is_valid():
# 			try:
# 				m=Doctor.objects.get(email=forgotForm.cleaned_data["email"],user_name=forgotForm.cleaned_data['user_name'])
# 				request.session['forget-pass']=m.user_name
# 				return redirect('forgot_pass_chg/'+m.user_name)
# 			except ObjectDoesNotExist as e:
# 				return render(request,'dashboard/doctor/forgot_pass.html',{'form':forgotForm,'message':'Incorrect Credentials'})
# 		else:
# 			return render(request,'dashboard/doctor/forgot_pass.html',{'form':forgotForm,'message':'Invalid Captcha'})
# 	forgotForm=forgot_pass_form()
# 	return render(request,'dashboard/doctor/forgot_pass.html',{'form':forgotForm,'message':'Please Enter Details'})
# def forgot_pass_chg(request,user):
# 	if request.method == 'GET':
# 		try:
# 			if 'forget-pass' in request.session:
# 				if user==request.session['forget-pass']:
# 					m=Doctor.objects.get(user_name=user)
# 					forgetForm=forgot_pass_form_chg()
# 					return render(request,'dashboard/doctor/forgot_pass_chg.html',{'form':forgetForm,'message':'Enter password Details','user':m})
# 		except Exception as e:
# 			return HttpResponse(e)
# 	if request.method == "POST":
# 		try:
# 			if 'forget-pass' in request.session:
# 				if user==request.session['forget-pass']:
# 					m=Doctor.objects.get(user_name=user)
# 					forgetForm=forgot_pass_form_chg(request.POST)
# 					if forgetForm.is_valid():
# 						if forgetForm.cleaned_data['password1']!=forgetForm.cleaned_data['password2']:
# 							return render(request,'dashboard/doctor/forgot_pass.html',{'form':forgetForm,'message':'passwords does not match'})
# 						if m.secret_ans.strip()==forgetForm.cleaned_data['secret_ans'].strip():
# 							m.password=forgetForm.cleaned_data['password1']
# 							m.updated_at=datetime.datetime.now()
# 							request.session.flush()
# 							m.save()
# 							return redirect('/doctor/login')
# 					return render(request,'dashboard/doctor/forgot_pass_chg.html',{'form':forgetForm,'message':'Invalid Captcha'})
# 		except Exception as e:
# 			return HttpResponse(e)
# 	return HttpResponse("Not Eligible to View 2")
def forgot_pass_chg(request,user):
	if request.method == 'GET':
		try:
			if 'forget-pass' in request.session:
				if user==request.session['forget-pass']:
					m=Doctor.objects.get(user_name=user)
					forgetForm=forgot_pass_form_chg()
					return render(request,'dashboard/doctor/forgot_pass_chg.html',{'form':forgetForm,'message':'Enter password Details','user':m})
		except Exception as e:
			return HttpResponse(e)
	if request.method == "POST":
		try:
			if 'forget-pass' in request.session:
				if user==request.session['forget-pass']:
					m=Doctor.objects.get(user_name=user)
					forgetForm=forgot_pass_form_chg(request.POST)
					if forgetForm.is_valid():
						if forgetForm.cleaned_data['password1']!=forgetForm.cleaned_data['password2']:
							return render(request,'dashboard/doctor/forgot_pass_chg.html',{'form':forgetForm,'message':'passwords does not match'})
						if m.User_otp.strip()==forgetForm.cleaned_data['User_otp'].strip():
							m.password=forgetForm.cleaned_data['password1']
							m.updated_at=datetime.datetime.now()
							m.User_progress=1
							request.session.flush()
							m.save()
							return redirect('/doctor/login')
					return render(request,'dashboard/doctor/forgot_pass_chg.html',{'form':forgetForm,'message':'Invalid Captcha'})
		except Exception as e:
			return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def givefeed(request,user):
	m=Doctor.objects.get(user_name=user)
	if 'doctorname' in request.session:
		if user==request.session['doctorname']:
			if request.method == "POST":
				uform=doctor_feedback_form(request.POST)
				if uform.is_valid():
					feedback_entry=Doctor_fb(uid=m.id,user_name=m.user_name,created_at=datetime.datetime.now(),\
						content=uform.cleaned_data['content'],subject=uform.cleaned_data['subject'])
					feedback_entry.save()
					return render(request,'dashboard/doctor/givefeed.html',{'form':uform,'message':'SuccessFul Updation','user':m})
				else:
					return render(request,'dashboard/doctor/givefeed.html',{'form':uform,'message':'Invalid Detail','user':m})
			uform=doctor_feedback_form()
			return render(request,'dashboard/doctor/givefeed.html',{'form':uform,'message':'Please Update Fill Form. Once Done cannot be \
				undone','user':m})
	# except Exception as e:
	# 	return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def showfeed(request,user):
	m=Doctor.objects.get(user_name=user)
	if 'doctorname' in request.session:
		if user==request.session['doctorname']:
			try:
				ftb=Doctor_fb.objects.filter(user_name=user)
				return render(request,'dashboard/doctor/showfeed.html',{'user':m,'ftable':ftb})
			except Exception as e:
				return render(request,'dashboard/doctor/showfeed.html',{'user':m})
	# 	return HttpResponse(e)	
	# except Exception as e:
	# 	return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")
def takepatient(request,user):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            # try:
                if request.method=='POST':
                    doctor_consult_user_login_f=doctor_consult_user_login(request.POST)
                    if doctor_consult_user_login_f.is_valid():
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
                                return render(request,'dashboard/doctor/takepatient.html',{'user':m,'message':"Regenerate OTP,it has lapsed 10 minutes span"})
                            if t.User_otp==doctor_consult_user_login_f.cleaned_data['User_otp']:
                                t.User_otp=None
                                t.save()
                                request.session['doctor_user_login']=t.user_name
                                if request.POST['case_status']=="1":
                                    o=User_doctor_case(user=t,is_accidental=False)
                                    o.save()
                                    r=User_doctor_consultancy(doctor=m,user_case=o,loginTime=datetime.datetime.now(),success=False,is_accidental=False)
                                    r.save()
                                    request.session['case_id']=o.id
                                    request.session['consult_id']=r.id
                                    return redirect('/doctor/new_case_pageone/'+m.user_name)
                                else:
                                    return redirect('/doctor/enter_case/'+m.user_name)
                            return render(request,'dashboard/doctor/takepatient.html',{'user':m,'message':"OTP Incorrect"})
                        except ObjectDoesNotExist as e:
                            return render(request,'dashboard/doctor/takepatient.html',{'user':m,'message':"Invalid UserID"})
                    return render(request,'dashboard/doctor/takepatient.html',{'user':m,'message':"Invalid Details"})
                return render(request,'dashboard/doctor/takepatient.html',{'user':m,'message':""})
            # except Exception as e:
            #     return render(request,'dashboard/doctor/takepatient.html',{'user':m,'message':e})
    return HttpResponse("Not Eligible to View 2")
def takepatient_otp_user(request,user):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
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
                    send_email_str="Mr./Mrs. "+str(otp_name)+" the OTP for your Health id is "+str(otp_user)+" reffered by Dr. "+m.firstname+" "+m.lastname
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
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            try:
                if 'doctor_user_login' in request.session:
                    t=User.objects.get(user_name=request.session['doctor_user_login'])
                    cases_=User_doctor_case.objects.filter(user=t)
                    import json
                    
                    cases_=User_doctor_case.objects.filter(user=t)
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
                    return render(request,'dashboard/doctor/enter_case.html',{'user':m,'user_patient':t,'cases_':cases_})
                return HttpResponse("Not Eligible to View 3 Please Enter user id")
            except Exception as e:
                return render(request,'dashboard/doctor/enter_case.html',{'user':m})
    return HttpResponse("Not Eligible to View 2")
def select_case(request,user,case_id):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            try:
                if 'doctor_user_login' in request.session:
                    t=User.objects.get(user_name=request.session['doctor_user_login'])
                    try:
                    	o=User_doctor_case.objects.get(user=t,id=case_id)
                    	request.session['case_id']=o.id
                    	r=User_doctor_consultancy(doctor=m,user_case=o,loginTime=datetime.datetime.now(),success=False,is_accidental=False)
                    	r.save()
                    	request.session['consult_id']=r.id
                    	request.session['case_id']=o.id
                    	return redirect('/doctor/new_case_pageone/'+m.user_name)
                    except ObjectDoesNotExist as e:
                    	return redirect('/doctor/enter_case/'+m.user_name)
                     
                return HttpResponse("Not Eligible to View 3 Please Enter user id")
            except Exception as e:
                return render(request,'dashboard/doctor/new_case_pageone.html',{'user':m,'message':e})
    return HttpResponse("Not Eligible to View 2")

def new_case_pageone(request,user):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            try:
                if 'doctor_user_login' in request.session:
                    if request.method=='POST':
                        symptoms=str(request.POST.get('symptoms', None))
                        diseases=str(request.POST.get('diseases', None))
                        final_injury_type=str(request.POST.get('injury_type', None))
                        general_notes=str(request.POST.get('general_notes', None))
                        personal_notes=str(request.POST.get('personal_notes', None))
                        is_accidental=request.POST['is_accidental']
                        t=User.objects.get(user_name=request.session['doctor_user_login'])
                        case_id=request.session['case_id']
                        consult_id=request.session['consult_id']
                        case_u=User_doctor_case.objects.get(id=case_id)
                        cons_u=User_doctor_consultancy.objects.get(id=consult_id)
                        try:
                            med_name=str(request.POST.get('med_name', None))
                            med_dos=str(request.POST.get('med_dos', None))
                            med_qnt=str(request.POST.get('med_qnt', None))
                            import json
                            med_name_arr = json.loads(med_name)
                            med_dos_arr = json.loads(med_dos)
                            med_qnt_arr = json.loads(med_qnt)
                            for i_ind in range(len(med_name_arr)):
                                User_medicine_e=User_medicine(use_consult=cons_u,medicine_name=med_name_arr[i_ind],dosage=med_dos_arr[i_ind],quantity=med_qnt_arr[i_ind],is_delivered=False)
                                User_medicine_e.save()
                                User_medicine_own_e=User_medicine_own(user=t,medicine_name=med_name_arr[i_ind],dosage=med_dos_arr[i_ind],quantity=med_qnt_arr[i_ind])
                                User_medicine_own_e.save()
                            lab_test=str(request.POST.get('lab_test', None))
                            lab_test_arr = json.loads(lab_test)
                            for i_ind in range(len(lab_test_arr)):
                            	User_reports_e=User_reports(user_case=case_u,name=lab_test_arr[i_ind],doctor=m,ref_date=datetime.datetime.now(),is_delivered=False)
                            	User_reports_e.save()
                        except Exception as e:
                            return HttpResponse(e)
                        cons_u.logoutTime=datetime.datetime.now()
                        cons_u.success=True
                        cons_u.symptoms=symptoms
                        cons_u.diseases=diseases
                        cons_u.general_notes=general_notes
                        cons_u.personal_notes=personal_notes
                        cons_u.is_accidental=is_accidental
                        cons_u.injury_type=final_injury_type

                        case_u.symptoms=symptoms
                        case_u.diseases=diseases
                        case_u.injury_type=final_injury_type
                        case_u.general_notes=general_notes
                        case_u.personal_notes=personal_notes
                        case_u.is_accidental=is_accidental
                        case_u.is_closed=request.POST['is_closed']
                        cons_u.is_accidental=is_accidental
                        case_u.save()
                        cons_u.save()

                        return redirect('/doctor/takepatient/'+m.user_name)
                    t=User.objects.get(user_name=request.session['doctor_user_login'])
                    case_id=request.session['case_id']
                    consult_id=request.session['consult_id']
                    b=User_medical.objects.get(user=t)
                    s=User_surgery.objects.filter(user=t)
                    # sys=Symptoms.objects.all()
                    import json
                    user_medicines_e=User_medicine_own.objects.filter(user=t)
                    cases_=User_doctor_case.objects.filter(user=t)
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
                    sys_cat=SymptomCat.objects.all()
                    dis_cat=DiseaseCat.objects.all()
                    inj_sel=Injury.objects.all()
                    return render(request,'dashboard/doctor/new_case_pageone.html',{'user':m,'user_patient':t,'user_medicines_e':user_medicines_e,'case_id':case_id,\
                        'consult_id':consult_id,'surgery':s,'basic_med':b,'sys_cat':sys_cat,'dis_cat':dis_cat,'inj_sel':inj_sel,'cases_':cases_})
                return HttpResponse("Not Eligible to View 3 Please Enter user id")
            except Exception as e:
                return render(request,'dashboard/doctor/new_case_pageone.html',{'user':m,'message':e})
    return HttpResponse("Not Eligible to View 2")
def addsymptcatajax(request,user):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            try:
                if 'doctor_user_login' in request.session:
                    symptom_name=str(request.POST.get('symptom_name', None))
                    symptom_desc=str(request.POST.get('symptom_desc', None))
                    try:
                        SymptomCat_e=SymptomCat(doctor=m,name=symptom_name,description=symptom_desc)
                        SymptomCat_e.save()
                        response_data = {}
                        response_data['result'] ="Symptom Category Saved"
                        return JsonResponse(response_data)
                    except ObjectDoesNotExist as e:
                        response_data = {}
                        response_data['result'] = str(e)
                        return JsonResponse(response_data)
                response_data = {}
                response_data['result'] = "Authorization Breach 2"
                return JsonResponse(response_data)
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"
    return JsonResponse(response_data)
def addsymptajax(request,user):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            try:
                if 'doctor_user_login' in request.session:
                    symptom_name=str(request.POST.get('symptom_name', None))
                    symptom_desc=str(request.POST.get('symptom_desc', None))
                    symptom_cat=SymptomCat.objects.get(id=request.POST.get('symptom_cat_select_modal', None))
                    alternate_names=str(request.POST.get('alternate_name', None))
                    try:
                        SymptomCat_e=Symptoms(doctor=m,name=symptom_name,description=symptom_desc,Symptomcat=symptom_cat,alternate_names=alternate_names)
                        SymptomCat_e.save()
                        response_data = {}
                        response_data['result'] ="Symptom Saved"
                        return JsonResponse(response_data)
                    except ObjectDoesNotExist as e:
                        response_data = {}
                        response_data['result'] = str(e)
                        return JsonResponse(response_data)
                response_data = {}
                response_data['result'] = "Authorization Breach 2"
                return JsonResponse(response_data)
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"
    return JsonResponse(response_data)
def addinjajax(request,user):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            try:
                if 'doctor_user_login' in request.session:
                    injury_name=str(request.POST.get('injury_name', None))
                    inj_sev=str(request.POST.get('inj_sev', None))
                    injury_desc=str(request.POST.get('injury_desc', None))
                    alternate_names=str(request.POST.get('inj_alternate_name', None))
                    Injury_e=Injury(doctor=m,name=injury_name,description=injury_desc,alternate_names=alternate_names,disease_intensity=inj_sev)
                    Injury_e.save()
                    response_data = {}
                    response_data['result'] =" New Injury Saved"
                    return JsonResponse(response_data)                
                response_data = {}
                response_data['result'] = "Authorization Breach 2"
                return JsonResponse(response_data)
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"
    return JsonResponse(response_data)
def getsymptajax(request,user):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            try:
                if 'doctor_user_login' in request.session:
                    catid=str(request.GET.get('catid', None))
                    sympt_resp=Symptoms.objects.filter(Symptomcat=catid)
                    names=[]
                    desc=[]
                    ids=[]
                    alt_names=[]
                    for x in sympt_resp:
                        names.append(x.name)
                        desc.append(x.description)
                        alt_names.append(x.alternate_names)
                        ids.append(x.id)
                    response_data = {}
                    response_data['names'] =names
                    response_data['desc'] =desc
                    response_data['alt_names'] =alt_names
                    response_data['ids'] =ids
                    return JsonResponse(response_data)
                response_data = {}
                response_data['result'] = "Authorization Breach 2"
                return JsonResponse(response_data)
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"
    return JsonResponse(response_data)
def adddiseasecatajax(request,user):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            try:
                if 'doctor_user_login' in request.session:
                    disease_cat_name=str(request.POST.get('disease_cat_name', None))
                    disease_cat_desc=str(request.POST.get('disease_cat_desc', None))
                    try:
                        DiseaseCat_e=DiseaseCat(doctor=m,name=disease_cat_name,description=disease_cat_desc)
                        DiseaseCat_e.save()
                        response_data = {}
                        response_data['result'] ="Disease Category Saved"
                        return JsonResponse(response_data)
                    except ObjectDoesNotExist as e:
                        response_data = {}
                        response_data['result'] = str(e)
                        return JsonResponse(response_data)
                response_data = {}
                response_data['result'] = "Authorization Breach 2"
                return JsonResponse(response_data)
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"
    return JsonResponse(response_data)
def adddiseaseajax(request,user):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            try:
                if 'doctor_user_login' in request.session:
                    disease_name=str(request.POST.get('disease_name', None))
                    disease_desc=str(request.POST.get('disease_desc', None))
                    disease_cat=DiseaseCat.objects.get(id=request.POST.get('disease_cat_select_modal', None))
                    alternate_name=str(request.POST.get('alternate_name', None))
                    dis_int=str(request.POST.get('dis_int', None))
                    try:
                        disease_e=Diseases(doctor=m,name=disease_name,description=disease_desc,DiseaseCat=disease_cat,\
                            alternate_names=alternate_name,disease_intensity=dis_int)
                        disease_e.save()
                        response_data = {}
                        response_data['result'] ="Disease Saved"
                        return JsonResponse(response_data)
                    except ObjectDoesNotExist as e:
                        response_data = {}
                        response_data['result'] = str(e)
                        return JsonResponse(response_data)
                response_data = {}
                response_data['result'] = "Authorization Breach 2"
                return JsonResponse(response_data)
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"
    return JsonResponse(response_data)
def getdisajax(request,user):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            try:
                if 'doctor_user_login' in request.session:
                    catid=str(request.GET.get('catid', None))
                    sympt_resp=Diseases.objects.filter(DiseaseCat=catid)
                    names=[]
                    desc=[]
                    ids=[]
                    alt_names=[]
                    for x in sympt_resp:
                        names.append(x.name)
                        desc.append(x.description)
                        alt_names.append(x.alternate_names)
                        ids.append(x.id)
                    response_data = {}
                    response_data['names'] =names
                    response_data['desc'] =desc
                    response_data['alt_names'] =alt_names
                    response_data['ids'] =ids
                    return JsonResponse(response_data)
                response_data = {}
                response_data['result'] = "Authorization Breach 2"
                return JsonResponse(response_data)
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"
    return JsonResponse(response_data)
def get_cons_doc(request,user):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            try:
                if 'doctor_user_login' in request.session:
                    case_id=str(request.GET.get('case_id', None))
                    try:
                        user_case=User_doctor_case.objects.get(id=case_id)
                    except Exception as e:
                        response_data = {}
                        response_data['result'] = ""
                        return JsonResponse(response_data)

                    User_doctor_consultancy_q=User_doctor_consultancy.objects.filter(user_case=user_case)
                    # lisT_ans=""
                    import json
                    # for i in range(len(User_doctor_consultancy_q)):
                    # 	lisT_ans+=str(x.logoutTime)
                    # 	print(x.logoutTime)
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
                    # print(User_doctor_consultancy_q_S)
                    response_data["result"] =User_doctor_consultancy_q_S
                    return JsonResponse(response_data)
                response_data = {}
                response_data['result'] = "Authorization Breach 2"
                return JsonResponse(response_data)
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"
    return JsonResponse(response_data)
def delete_med_entry(request,user):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            try:
                if 'doctor_user_login' in request.session:
                    case_id=str(request.POST.get('case_id', None))
                    print(case_id)
                    try:
                        User_medicine_own_e=User_medicine_own.objects.get(id=case_id)
                        User_medicine_own_e.delete()
                        response_data = {}
                        response_data['result'] ="Medicine deleted"
                        return JsonResponse(response_data)
                    except ObjectDoesNotExist as e:
                        response_data = {}
                        response_data['result'] = "Case Id does'nt exist"
                        return JsonResponse(response_data)
                response_data = {}
                response_data['result'] = "Authorization Breach 2"
                return JsonResponse(response_data)
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"
    return JsonResponse(response_data)
def get_cons_medicine(request,user):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            try:
                if 'doctor_user_login' in request.session:
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
                response_data = {}
                response_data['result'] = "Authorization Breach 2"
                return JsonResponse(response_data)
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"
    return JsonResponse(response_data)
def getajaxlab(request,user):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            try:
                if 'doctor_user_login' in request.session:
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
                response_data = {}
                response_data['result'] = "Authorization Breach 2"
                return JsonResponse(response_data)
            except Exception as e:
                response_data = {}
                response_data['result'] = str(e)
                return JsonResponse(response_data)
    response_data = {}
    response_data['result'] = "Authorization Breach"
    return JsonResponse(response_data)
def prev_cases(request,user):
    m=Doctor.objects.get(user_name=user)
    if 'doctorname' in request.session:
        if user==request.session['doctorname']:
            try:
                User_doctor_consultancy_q=User_doctor_consultancy.objects.filter(doctor=m)
                import json
                # for i in range(len(User_doctor_consultancy_q)):
                #   lisT_ans+=str(x.logoutTime)
                #   print(x.logoutTime)
                users_arr=[]    
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
                    
                    if User_doctor_consultancy_q[i].user_case !=None:
                        y = User_doctor_consultancy_q[i].user_case
                        temp2=User.objects.get(id=y.user.id)
                        z=str(str(temp2.firstname)+"  "+ str(temp2.lastname))
                        users_arr.append(z)
                    else:
                        users_arr.append('None')

                from django.core import serializers
                User_doctor_consultancy_q_S = serializers.serialize("json", User_doctor_consultancy_q)
                users_arr = json.dumps(users_arr)
                User_doctor_consultancy_q=User_doctor_consultancy.objects.filter(doctor=m)
                t=[]
                for x in User_doctor_consultancy_q:
                    cons_id=User_medicine.objects.filter(use_consult=x)
                    for y in cons_id:
                        r={}
                        print(y.use_consult.id)
                        r['use_consult']=y.use_consult.id
                        r['logoutTime']=y.use_consult.logoutTime
                        r['medicine_name']=y.medicine_name
                        r['dosage']=y.dosage
                        r['quantity']=y.quantity
                        r['is_delivered']=y.is_delivered
                        t.append(r)
                

                return render(request,'dashboard/doctor/prev_cases.html',{'user':m,'ftable':User_doctor_consultancy_q_S,\
                    'users_arr':users_arr,'users_med':t})
            except Exception as e:
                print(e)
                return render(request,'dashboard/doctor/prev_cases.html',{'user':m})
    #   return HttpResponse(e)  
    # except Exception as e:
    #   return HttpResponse(e)
    return HttpResponse("Not Eligible to View 2")