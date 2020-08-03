from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import Login, Register, Update_user, Change_Password, forgot_pass_form_chg, forgot_pass_form, user_feedback_form, email_verify, user_emergency_contacts, basic_med_form,user_surgery_f
from .models import User, UserLog, User_fb, User_contacts, User_medical,User_surgery,User_doctor_case,User_doctor_consultancy,User_doctor_case,User_surgery,User_contacts,User_medicine,User_medicine_own,User_reports,Lab_report_files
from doctor.models import Doctor,DoctorLog,Doctor_fb,SymptomCat,Symptoms,DiseaseCat,Diseases,Injury
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib import messages
import pgeocode
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

def send_email(receiver_address, subject, mail_content):
	sender_address = 'healthp74@gmail.com'
	sender_pass = '123@mohit'
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = receiver_address
	message['Subject'] = str(subject)
	message.attach(MIMEText(mail_content, 'plain'))
	# Create SMTP session for sending the mail
	session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
	session.starttls()  # enable security
	session.login(sender_address, sender_pass)  # login with mail_id and password
	text = message.as_string()
	session.sendmail(sender_address, receiver_address, text)
	session.quit()


# Create your views here.
isoCountries = {
    'AF': 'Afghanistan',
    'AX': 'Aland Islands',
    'AL': 'Albania',
    'DZ': 'Algeria',
    'AS': 'American Samoa',
    'AD': 'Andorra',
    'AO': 'Angola',
    'AI': 'Anguilla',
    'AQ': 'Antarctica',
    'AG': 'Antigua And Barbuda',
    'AR': 'Argentina',
    'AM': 'Armenia',
    'AW': 'Aruba',
    'AU': 'Australia',
    'AT': 'Austria',
    'AZ': 'Azerbaijan',
    'BS': 'Bahamas',
    'BH': 'Bahrain',
    'BD': 'Bangladesh',
    'BB': 'Barbados',
    'BY': 'Belarus',
    'BE': 'Belgium',
    'BZ': 'Belize',
    'BJ': 'Benin',
    'BM': 'Bermuda',
    'BT': 'Bhutan',
    'BO': 'Bolivia',
    'BA': 'Bosnia And Herzegovina',
    'BW': 'Botswana',
    'BV': 'Bouvet Island',
    'BR': 'Brazil',
    'IO': 'British Indian Ocean Territory',
    'BN': 'Brunei Darussalam',
    'BG': 'Bulgaria',
    'BF': 'Burkina Faso',
    'BI': 'Burundi',
    'KH': 'Cambodia',
    'CM': 'Cameroon',
    'CA': 'Canada',
    'CV': 'Cape Verde',
    'KY': 'Cayman Islands',
    'CF': 'Central African Republic',
    'TD': 'Chad',
    'CL': 'Chile',
    'CN': 'China',
    'CX': 'Christmas Island',
    'CC': 'Cocos (Keeling) Islands',
    'CO': 'Colombia',
    'KM': 'Comoros',
    'CG': 'Congo',
    'CD': 'Congo, Democratic Republic',
    'CK': 'Cook Islands',
    'CR': 'Costa Rica',
    'CI': 'Cote D\'Ivoire',
    'HR': 'Croatia',
    'CU': 'Cuba',
    'CY': 'Cyprus',
    'CZ': 'Czech Republic',
    'DK': 'Denmark',
    'DJ': 'Djibouti',
    'DM': 'Dominica',
    'DO': 'Dominican Republic',
    'EC': 'Ecuador',
    'EG': 'Egypt',
    'SV': 'El Salvador',
    'GQ': 'Equatorial Guinea',
    'ER': 'Eritrea',
    'EE': 'Estonia',
    'ET': 'Ethiopia',
    'FK': 'Falkland Islands (Malvinas)',
    'FO': 'Faroe Islands',
    'FJ': 'Fiji',
    'FI': 'Finland',
    'FR': 'France',
    'GF': 'French Guiana',
    'PF': 'French Polynesia',
    'TF': 'French Southern Territories',
    'GA': 'Gabon',
    'GM': 'Gambia',
    'GE': 'Georgia',
    'DE': 'Germany',
    'GH': 'Ghana',
    'GI': 'Gibraltar',
    'GR': 'Greece',
    'GL': 'Greenland',
    'GD': 'Grenada',
    'GP': 'Guadeloupe',
    'GU': 'Guam',
    'GT': 'Guatemala',
    'GG': 'Guernsey',
    'GN': 'Guinea',
    'GW': 'Guinea-Bissau',
    'GY': 'Guyana',
    'HT': 'Haiti',
    'HM': 'Heard Island & Mcdonald Islands',
    'VA': 'Holy See (Vatican City State)',
    'HN': 'Honduras',
    'HK': 'Hong Kong',
    'HU': 'Hungary',
    'IS': 'Iceland',
    'IN': 'India',
    'ID': 'Indonesia',
    'IR': 'Iran, Islamic Republic Of',
    'IQ': 'Iraq',
    'IE': 'Ireland',
    'IM': 'Isle Of Man',
    'IL': 'Israel',
    'IT': 'Italy',
    'JM': 'Jamaica',
    'JP': 'Japan',
    'JE': 'Jersey',
    'JO': 'Jordan',
    'KZ': 'Kazakhstan',
    'KE': 'Kenya',
    'KI': 'Kiribati',
    'KR': 'Korea',
    'KW': 'Kuwait',
    'KG': 'Kyrgyzstan',
    'LA': 'Lao People\'s Democratic Republic',
    'LV': 'Latvia',
    'LB': 'Lebanon',
    'LS': 'Lesotho',
    'LR': 'Liberia',
    'LY': 'Libyan Arab Jamahiriya',
    'LI': 'Liechtenstein',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'MO': 'Macao',
    'MK': 'Macedonia',
    'MG': 'Madagascar',
    'MW': 'Malawi',
    'MY': 'Malaysia',
    'MV': 'Maldives',
    'ML': 'Mali',
    'MT': 'Malta',
    'MH': 'Marshall Islands',
    'MQ': 'Martinique',
    'MR': 'Mauritania',
    'MU': 'Mauritius',
    'YT': 'Mayotte',
    'MX': 'Mexico',
    'FM': 'Micronesia, Federated States Of',
    'MD': 'Moldova',
    'MC': 'Monaco',
    'MN': 'Mongolia',
    'ME': 'Montenegro',
    'MS': 'Montserrat',
    'MA': 'Morocco',
    'MZ': 'Mozambique',
    'MM': 'Myanmar',
    'NA': 'Namibia',
    'NR': 'Nauru',
    'NP': 'Nepal',
    'NL': 'Netherlands',
    'AN': 'Netherlands Antilles',
    'NC': 'New Caledonia',
    'NZ': 'New Zealand',
    'NI': 'Nicaragua',
    'NE': 'Niger',
    'NG': 'Nigeria',
    'NU': 'Niue',
    'NF': 'Norfolk Island',
    'MP': 'Northern Mariana Islands',
    'NO': 'Norway',
    'OM': 'Oman',
    'PK': 'Pakistan',
    'PW': 'Palau',
    'PS': 'Palestinian Territory, Occupied',
    'PA': 'Panama',
    'PG': 'Papua New Guinea',
    'PY': 'Paraguay',
    'PE': 'Peru',
    'PH': 'Philippines',
    'PN': 'Pitcairn',
    'PL': 'Poland',
    'PT': 'Portugal',
    'PR': 'Puerto Rico',
    'QA': 'Qatar',
    'RE': 'Reunion',
    'RO': 'Romania',
    'RU': 'Russian Federation',
    'RW': 'Rwanda',
    'BL': 'Saint Barthelemy',
    'SH': 'Saint Helena',
    'KN': 'Saint Kitts And Nevis',
    'LC': 'Saint Lucia',
    'MF': 'Saint Martin',
    'PM': 'Saint Pierre And Miquelon',
    'VC': 'Saint Vincent And Grenadines',
    'WS': 'Samoa',
    'SM': 'San Marino',
    'ST': 'Sao Tome And Principe',
    'SA': 'Saudi Arabia',
    'SN': 'Senegal',
    'RS': 'Serbia',
    'SC': 'Seychelles',
    'SL': 'Sierra Leone',
    'SG': 'Singapore',
    'SK': 'Slovakia',
    'SI': 'Slovenia',
    'SB': 'Solomon Islands',
    'SO': 'Somalia',
    'ZA': 'South Africa',
    'GS': 'South Georgia And Sandwich Isl.',
    'ES': 'Spain',
    'LK': 'Sri Lanka',
    'SD': 'Sudan',
    'SR': 'Suriname',
    'SJ': 'Svalbard And Jan Mayen',
    'SZ': 'Swaziland',
    'SE': 'Sweden',
    'CH': 'Switzerland',
    'SY': 'Syrian Arab Republic',
    'TW': 'Taiwan',
    'TJ': 'Tajikistan',
    'TZ': 'Tanzania',
    'TH': 'Thailand',
    'TL': 'Timor-Leste',
    'TG': 'Togo',
    'TK': 'Tokelau',
    'TO': 'Tonga',
    'TT': 'Trinidad And Tobago',
    'TN': 'Tunisia',
    'TR': 'Turkey',
    'TM': 'Turkmenistan',
    'TC': 'Turks And Caicos Islands',
    'TV': 'Tuvalu',
    'UG': 'Uganda',
    'UA': 'Ukraine',
    'AE': 'United Arab Emirates',
    'GB': 'United Kingdom',
    'US': 'United States',
    'UM': 'United States Outlying Islands',
    'UY': 'Uruguay',
    'UZ': 'Uzbekistan',
    'VU': 'Vanuatu',
    'VE': 'Venezuela',
    'VN': 'Viet Nam',
    'VG': 'Virgin Islands, British',
    'VI': 'Virgin Islands, U.S.',
    'WF': 'Wallis And Futuna',
    'EH': 'Western Sahara',
    'YE': 'Yemen',
    'ZM': 'Zambia',
    'ZW': 'Zimbabwe'
};


def generateOTP():
	import math
	import random
	digits = "0123456789"
	OTP = ""
	for i in range(4):
	    OTP += digits[math.floor(random.random() * 10)]
	return OTP


def get_key(my_dict, val):
    for key, value in my_dict.items():
         if val == value:
             return key
    return None


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def getselected_area(request):
   country = str(request.GET.get('country', None))
   pincode = str(request.GET.get('pincode', None))
   cnt = get_key(isoCountries, country)
   nomi = pgeocode.Nominatim(cnt)
   paal = nomi.query_postal_code(pincode).place_name.split(',')
   areas = []
   for x in paal:
      # if typeof(x)=='string:
      areas.append(x.strip())
   coords = [nomi.query_postal_code(
       pincode).latitude, nomi.query_postal_code(pincode).longitude]
   response_data = {}
   response_data['result'] = areas
   response_data['coords'] = coords
   response_data['community_name'] = nomi.query_postal_code(
       pincode).community_name  # Taluka
   response_data['county_name'] = nomi.query_postal_code(
       pincode).county_name  # District Name
   response_data['state_name'] = nomi.query_postal_code(pincode).state_name
   response_data['lat'] = str(nomi.query_postal_code(pincode).latitude)
   response_data['lon'] = str(nomi.query_postal_code(pincode).longitude)
   response_data['accuracy'] = str(nomi.query_postal_code(pincode).accuracy)
   return JsonResponse(response_data)


def register(request):
	if request.method == "POST":
		loginForm = Register(request.POST, request.FILES)
		if loginForm.is_valid():
			if request.POST['password1'] != request.POST['password2']:
				return render(request, 'dashboard/user/register.html', {'form': loginForm, 'message': 'passwords does not match'})
			objects = User.objects.all()
			for elt in objects:
				if elt.email == request.POST['email']:
					return render(request, 'dashboard/user/register.html', {'form': loginForm, 'message': 'Already Email Registered'})
				if elt.user_name == request.POST['user_name']:
					return render(request, 'dashboard/user/register.html', {'form': loginForm, 'message': 'Already user_name Registered'})
			otp_user = str(generateOTP())
			otp_email = request.POST['email']
			otp_name = request.POST['firstname']+request.POST['lastname']
			login_entry = User(
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
	            created_at=datetime.datetime.now(),
	            updated_at=datetime.datetime.now(),
	            User_progress=0,
	            User_otp=otp_user,
	            )
			login_entry.user_photo = loginForm.cleaned_data['user_photo']
			login_entry.save()
			send_email_str = str(otp_name) + \
			                     "The OTP for your Health id is "+str(otp_user)
			send_email(str(otp_email), "UIMPR Authetication OTP", send_email_str)
			return redirect('/user/login')
		else:
			return render(request, 'dashboard/user/register.html', {'form': loginForm, 'message': 'Invalid Detail'})
	loginForm = Register()
	cname = []
	for y in isoCountries:
		cname.append(isoCountries[y])
	cname.sort()
	return render(request, 'dashboard/user/register.html', {'form': loginForm, 'message': 'Please Fill the Details to create account', 'country_drop': cname})


def login(request):
	if request.method == 'GET':
		if 'username' in request.session:
			username = request.session['username']
			redirect('dashboard/'+username)
		loginForm = Login()
		return render(request, 'dashboard/user/login.html', {'form': loginForm, 'message': 'Please Login'})
	if request.method == "POST":
		loginForm = Login(request.POST)
		if loginForm.is_valid():
			try:
				m = User.objects.get(
				    email=loginForm.cleaned_data["email"], password=loginForm.cleaned_data["password"])
				if m.User_progress == '0':
					request.session['userverify'] = m.user_name
					return redirect('user_verify_email/'+m.user_name)
					# return HttpResponse("You have to Verify Email")
				# return HttpResponse(m.User_progress=='0')
				request.session['username'] = m.user_name
				user_log_entry = UserLog(uid=m.id, user_name=m.user_name, userip=get_client_ip(
				    request), loginTime=datetime.datetime.now(), success=False)
				user_log_entry.save()
				return redirect('dashboard/'+m.user_name)
			except ObjectDoesNotExist as e:
				return render(request, 'dashboard/user/login.html', {'form': loginForm, 'message': 'Incorrect Credentials'})
		else:
			return render(request, 'dashboard/user/login.html', {'form': loginForm, 'message': 'Invalid Captcha'})
	loginForm = Login()
	return render(request, 'dashboard/user/login.html', {'form': loginForm})


def user_verify_email(request, user):
    try:
        if 'userverify' in request.session:
            if user == request.session['userverify']:
                m = User.objects.get(user_name=user)
                if request.method == 'POST':
                    Verify_form = email_verify(request.POST)
                    if Verify_form.is_valid():
                        try:
                            otp_p = request.POST['User_otp']
                            if otp_p == m.User_otp:
                                m.User_progress = 1
                                request.session['username'] = m.user_name
                                m.save()
                                user_log_entry = UserLog(uid=m.id, user_name=m.user_name, userip=get_client_ip(request), loginTime=datetime.datetime.now(), success=False)
                                user_log_entry.save()
                                return redirect('/user/dashboard/'+m.user_name)
                            else:
                                return render(request, 'dashboard/user/email_verify.html', {'message': 'Wrong OTP', 'user': m})
                        except Exception as e:
                            return HttpResponse(e)
                    else:
                        return render(request, 'dashboard/user/email_verify.html', {'message': 'Invalid Form', 'user': m})
                loginForm = email_verify()
                return render(request, 'dashboard/user/email_verify.html', {'message': 'Enter OTP Details', 'form': loginForm, 'user': m})
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("Not Eligible to View 2")



def regenerate_otp(request, user):
	try:
		if 'userverify' in request.session:
			if user == request.session['userverify']:
				user_ = str(request.GET.get('user_name', None))
				if user == user_:
					m = User.objects.get(user_name=user)
					otp_user = str(generateOTP())
					otp_email = m.email
					otp_name = m.firstname+" "+m.lastname
					send_email_str = str(otp_name) + \
					                     "The OTP for your Health id is "+str(otp_user)
					send_email(str(otp_email), "UIMPR Authetication OTP", send_email_str)
					m.User_otp = otp_user
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


def otp_email_chg(request, user):
	try:
		if 'userverify' in request.session:
			if user == request.session['userverify']:
				user_ = str(request.POST.get('email', None))
				objects = User.objects.only("email")
				for elt in objects:
					if elt.email == request.POST['email']:
						response_data = {}
						response_data['result'] = "Already Email Registered"
						return JsonResponse(response_data)
				m = User.objects.get(user_name=user)
				m.email = user_
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


def dashboard(request, user):
	try:
		if 'username' in request.session:
			if user == request.session['username']:
				m = User.objects.get(user_name=user)
				return render(request, 'dashboard/user/index.html', {'user': m})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")


def logout(request, user):
	try:
		if 'username' in request.session:
			if user == request.session['username']:
				user_log_entry = UserLog.objects.filter(user_name=user).order_by('-id')[0]
				user_log_entry.logoutTime = datetime.datetime.now()
				user_log_entry.success = True
				user_log_entry.save()
				# del request.session['username']
				request.session.flush()
				return redirect('/user/login')
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to Logout 2")


def activity_log(request, user):
	try:
		if 'username' in request.session:
			if user == request.session['username']:
				m = User.objects.get(user_name=user)
				user_log_entry = UserLog.objects.filter(user_name=user).order_by('id')
				return render(request, 'dashboard/user/activity_log.html', {'user': m, 'user_log': user_log_entry})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")


def profile(request, user):
	try:
		if 'username' in request.session:
			if user == request.session['username']:
				m = User.objects.get(user_name=user)
				return render(request, 'dashboard/user/profile.html', {'user': m})
	except Exception as e:
		return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")


def settings(request, user):
	m = User.objects.get(user_name=user)
	# try:
	if 'username' in request.session:
		if user == request.session['username']:
			if request.method == "POST":
				loginForm = Update_user(request.POST, request.FILES)
				if loginForm.is_valid():
					objects = User.objects.all()
					for elt in objects:
						# print(type(elt),elt.email)
						if elt.user_name == request.POST['user_name']:
							if elt.user_name != m.user_name:
								return render(request, 'dashboard/user/settings.html', {'form': loginForm, 'message': 'Already user_name Registered', 'user': m})
					login_entry = User.objects.get(user_name=user)
					login_entry.firstname = request.POST['firstname']
					login_entry.lastname = request.POST['lastname']
					login_entry.gender = request.POST['gender']
					login_entry.user_name = request.POST['user_name']
					login_entry.country = request.POST['country']
					login_entry.state = request.POST['state']
					login_entry.district = request.POST['district']
					login_entry.city = request.POST['city']
					login_entry.area = request.POST['area']
					login_entry.society = request.POST['society']
					login_entry.landmark = request.POST['landmark']
					login_entry.house_no = request.POST['house_no']
					login_entry.pincode = request.POST['pincode']
					login_entry.blood_group = request.POST['blood_group']
					login_entry.aadhar_card_no = request.POST['aadhar_card_no']
					login_entry.dateofBirth = request.POST['dateofBirth']
					login_entry.phone_number = request.POST['phone_number']
					login_entry.updated_at = datetime.datetime.now()
					print("check1")
					login_entry.user_photo = loginForm.cleaned_data['user_photo']
					print("check2")
					login_entry.save()
					print("check3")
					return render(request, 'dashboard/user/settings.html', {'form': loginForm, 'message': 'SuccessFul Updation', 'user': m})
				else:
					return render(request, 'dashboard/user/settings.html', {'form': loginForm, 'message': 'Invalid Detail', 'user': m})
			loginForm = Update_user()
			cname = []
			for y in isoCountries:
				cname.append(isoCountries[y])
			cname.sort()
			return render(request, 'dashboard/user/settings.html', {'form': loginForm, 'message': 'Please Update Details', 'user': m, 'country_drop': cname})
	# except Exception as e:
	# 	return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")


def chg_passwd(request, user):
	m = User.objects.get(user_name=user)
	# try:
	if 'username' in request.session:
		if user == request.session['username']:
			if request.method == "POST":
				loginForm = Change_Password(request.POST)
				if loginForm.is_valid():
					if m.password != request.POST['password']:
						return render(request, 'dashboard/user/chg_passwd.html', {'form': loginForm, 'message': 'Your Original passworddoes not match'})
					if request.POST['password1'] != request.POST['password2']:
						return render(request, 'dashboard/user/chg_passwd.html', {'form': loginForm, 'message': 'passwords does not match'})
					m.password = request.POST['password1']
					m.updated_at = datetime.datetime.now()
					m.save()
					return render(request, 'dashboard/user/chg_passwd.html', {'form': loginForm, 'message': 'SuccessFul Updation', 'user': m})
				else:
					return render(request, 'dashboard/user/chg_passwd.html', {'form': loginForm, 'message': 'Invalid Detail', 'user': m})
			loginForm = Change_Password()
			return render(request, 'dashboard/user/chg_passwd.html', {'form': loginForm, 'message': 'Please Update Details', 'user': m})
	# except Exception as e:
	# 	return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")


def forgot_pass(request):
	if request.method == "POST":
		forgotForm = forgot_pass_form(request.POST)
		if forgotForm.is_valid():
			try:
				m = User.objects.get(
				    email=forgotForm.cleaned_data["email"], dateofBirth=forgotForm.cleaned_data['dateofBirth'])
				request.session['forget-pass'] = m.user_name
				otp_user = str(generateOTP())
				otp_email = m.email
				otp_name = m.firstname+" "+m.lastname
				send_email_str = str(otp_name) + \
				                     "The OTP for your Health id is "+str(otp_user)
				send_email(str(otp_email), "UIMPR Authetication OTP", send_email_str)
				m.User_otp = otp_user
				m.save()
				return redirect('forgot_pass_chg/'+m.user_name)
			except ObjectDoesNotExist as e:
				return render(request, 'dashboard/user/forgot_pass.html', {'form': forgotForm, 'message': 'Incorrect Credentials'})
		else:
			return render(request, 'dashboard/user/forgot_pass.html', {'form': forgotForm, 'message': 'Invalid Captcha'})
	forgotForm = forgot_pass_form()
	return render(request, 'dashboard/user/forgot_pass.html', {'form': forgotForm, 'message': 'Please Enter Details'})


def forgot_pass_chg(request, user):
	if request.method == 'GET':
		try:
			if 'forget-pass' in request.session:
				if user == request.session['forget-pass']:
					m = User.objects.get(user_name=user)
					forgetForm = forgot_pass_form_chg()
					return render(request, 'dashboard/user/forgot_pass_chg.html', {'form': forgetForm, 'message': 'Enter password Details', 'user': m})
		except Exception as e:
			return HttpResponse(e)
	if request.method == "POST":
		try:
			if 'forget-pass' in request.session:
				if user == request.session['forget-pass']:
					m = User.objects.get(user_name=user)
					forgetForm = forgot_pass_form_chg(request.POST)
					if forgetForm.is_valid():
						if forgetForm.cleaned_data['password1'] != forgetForm.cleaned_data['password2']:
							return render(request, 'dashboard/user/forgot_pass_chg.html', {'form': forgetForm, 'message': 'passwords does not match'})
						if m.User_otp.strip() == forgetForm.cleaned_data['User_otp'].strip():
							m.password = forgetForm.cleaned_data['password1']
							m.updated_at = datetime.datetime.now()
							m.User_progress = 1
							request.session.flush()

							m.save()
							return redirect('/user/login')
					return render(request, 'dashboard/user/forgot_pass_chg.html', {'form': forgetForm, 'message': 'Invalid Captcha'})
		except Exception as e:
			return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")


def givefeed(request, user):
	m = User.objects.get(user_name=user)
	if 'username' in request.session:
		if user == request.session['username']:
			if request.method == "POST":
				uform = user_feedback_form(request.POST)
				if uform.is_valid():
					feedback_entry = User_fb(uid=m.id, user_name=m.user_name, created_at=datetime.datetime.now(),
						content=uform.cleaned_data['content'], subject=uform.cleaned_data['subject'])
					feedback_entry.save()
					return render(request, 'dashboard/user/givefeed.html', {'form': uform, 'message': 'SuccessFul Updation', 'user': m})
				else:
					return render(request, 'dashboard/user/givefeed.html', {'form': uform, 'message': 'Invalid Detail', 'user': m})
			uform = user_feedback_form()
			return render(request, 'dashboard/user/givefeed.html', {'form': uform, 'message': 'Please Update Fill Form. Once Done cannot be \
				undone', 'user': m})
	# except Exception as e:
	# 	return HttpResponse(e)
	return HttpResponse("Not Eligible to View 2")


def showfeed(request, user):
    m = User.objects.get(user_name=user)
    if 'username' in request.session:
        if user == request.session['username']:
            try:
                ftb = User_fb.objects.filter(user_name=user)
                return render(request, 'dashboard/user/showfeed.html', {'user': m, 'ftable': ftb})
            except Exception as e:
                return render(request, 'dashboard/user/showfeed.html', {'user': m})
    #   return HttpResponse(e)
    # except Exception as e:
    #   return HttpResponse(e)
    return HttpResponse("Not Eligible to View 2")


def basic_med(request, user):
    m = User.objects.get(user_name=user)
    t = User_medical.objects.filter(user=m)
    if 'username' in request.session:
        if user == request.session['username']:
            try:
                if request.method == 'POST':
                    if len(t) > 0:
                        User_medical_entry = User_medical.objects.get(user=m)
                        User_medical_entry.height = request.POST['height']
                        User_medical_entry.weight = request.POST['weight']
                        User_medical_entry.martial_s = request.POST['martial_s']
                        User_medical_entry.disability_status = request.POST['disability_status']
                        User_medical_entry.disability_type = request.POST['disability_type']
                        User_medical_entry.disability_other = request.POST['disability_other']
                        User_medical_entry.pregnency = request.POST['pregnency']
                        User_medical_entry.vision = request.POST['vision']
                        User_medical_entry.alcohol = request.POST['alcohol']
                        User_medical_entry.smoking = request.POST['smoking']
                        User_medical_entry.drugs = request.POST['drugs']
                        User_medical_entry.color_vison = request.POST['color_vison']
                        User_medical_entry.masturbating = request.POST['masturbating']
                        User_medical_entry.other_details = request.POST['other_details']
                        User_medical_entry.updated_at = datetime.datetime.now()
                        User_medical_entry.save()
                        return render(request, 'dashboard/user/basic_med.html', {'user': m, 'message': 'Successfully Updated', 'Uploaded': t})
                    else:
                        User_medical_entry = User_medical(user=m,
                            height=request.POST['height'],
                            weight=request.POST['weight'],
                            martial_s=request.POST['martial_s'],
                            disability_status=request.POST['disability_status'],
                            disability_type=request.POST['disability_type'],
                            disability_other=request.POST['disability_other'],
                            pregnency=request.POST['pregnency'],
                            vision=request.POST['vision'],
                            alcohol=request.POST['alcohol'],
                            smoking=request.POST['smoking'],
                            drugs=request.POST['drugs'],
                            color_vison=request.POST['color_vison'],
                            masturbating=request.POST['masturbating'],
                            other_details=request.POST['other_details'],
                            updated_at=datetime.datetime.now(),
                            )
                        User_medical_entry.save()
                        return render(request, 'dashboard/user/basic_med.html', {'user': m, 'message': 'Successfully saved', 'Uploaded': t})
                if len(t) > 0:
                    return render(request, 'dashboard/user/basic_med.html', {'user': m, 'message': 'You have submitted once but you can update', 'Uploaded': t})
                return render(request, 'dashboard/user/basic_med.html', {'user': m, 'message': 'Please add Your details'})
            except Exception as e:
                return render(request, 'dashboard/user/basic_med.html', {'user': m, 'message': e})
    return HttpResponse("Not Eligible to View 2")


def surgical_data(request, user):
    m = User.objects.get(user_name=user)
    t = User_surgery.objects.filter(user=m)
    if 'username' in request.session:
        if user == request.session['username']:
            try:
                if request.method == 'POST':
                    user_surgery_f_e=user_surgery_f(request.POST,request.FILES)
                    if len(t)>=10:
                        return render(request,'dashboard/user/surgical_data.html',{'user':m,'form':user_surgery_f_e,'message':'MAX 4 Entries are allowed','ftable':t})
                    if user_surgery_f_e.is_valid():
                        User_surgery_entry=User_surgery(user=m,
                            surgery_type=user_surgery_f_e.cleaned_data['surgery_type'],
                            surgery_description=user_surgery_f_e.cleaned_data['surgery_description'],
                            dateofSurgery=user_surgery_f_e.cleaned_data['dateofSurgery'],
                            hospital_location=user_surgery_f_e.cleaned_data['hospital_location'],
                            hospital_name=user_surgery_f_e.cleaned_data['hospital_name'],
                            surgery_file=user_surgery_f_e.cleaned_data['surgery_file'],
                            )
                        User_surgery_entry.save()
                        return render(request,'dashboard/user/surgical_data.html',{'user':m,'form':user_surgery_f_e,'message':'Successfully Added','ftable':t})
                    return render(request,'dashboard/user/surgical_data.html',{'user':m,'form':user_surgery_f_e,'message':'Invalid Details','ftable':t})
                user_surgery_f_e=user_surgery_f()   
                return render(request,'dashboard/user/surgical_data.html',{'user':m,'form':user_surgery_f_e,'message':'','ftable':t})
            except Exception as e:
                return render(request,'dashboard/user/surgical_data.html',{'user':m,'message':e})
    return HttpResponse("Not Eligible to View 2")
def delete_surgical_data(request,user):
    try:
        if 'username' in request.session:
            if user==request.session['username']:
                surgeryid=str(request.GET.get('surgeryid', None))
                m=User.objects.get(user_name=user)
                t=User_surgery.objects.filter(user=m,id=surgeryid)
                t.delete();
                response_data = {}
                response_data['result'] = "Successfully Deleted Contact"
                return JsonResponse(response_data)
        response_data = {}
        response_data['result'] = "Authorization Breach"
        return JsonResponse(response_data)
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("Not Eligible to View 2")

def medicinal_data(request,user):
    m=User.objects.get(user_name=user)
    if 'username' in request.session:
        if user==request.session['username']:
            try:
                ftb=User_fb.objects.filter(user_name=user)
                return render(request,'dashboard/user/medicinal_data.html',{'user':m,'ftable':ftb})
            except Exception as e:
                return render(request,'dashboard/user/medicinal_data.html',{'user':m})
    #   return HttpResponse(e)  
    # except Exception as e:
    #   return HttpResponse(e)
    return HttpResponse("Not Eligible to View 2")
def emergency_data(request,user):
    m=User.objects.get(user_name=user)
    t=User_contacts.objects.filter(user=m)
    # return HttpResponse(len(t))
    if 'username' in request.session:
        if user==request.session['username']:
            try:
                if request.method=='POST':
                    emergency_contacts_f=user_emergency_contacts(request.POST)
                    if len(t)>=4:
                        return render(request,'dashboard/user/emergency_data.html',{'user':m,'form':emergency_contacts_f,'message':'MAX 4 Entries are allowed','ftable':t})
                    if emergency_contacts_f.is_valid():
                        if emergency_contacts_f.cleaned_data['phone_number']==emergency_contacts_f.cleaned_data['phone_number_2']:
                            return render(request,'dashboard/user/emergency_data.html',{'user':m,'form':emergency_contacts_f,'message':'Invalid Details','ftable':t})
                        User_contacts_entry=User_contacts(user=m,
                            name=emergency_contacts_f.cleaned_data['name'],
                            email=emergency_contacts_f.cleaned_data['email'],
                            phone_number=emergency_contacts_f.cleaned_data['phone_number'],
                            address=emergency_contacts_f.cleaned_data['address'],
                            phone_number_2=emergency_contacts_f.cleaned_data['phone_number_2'],
                            relationship=emergency_contacts_f.cleaned_data['relationship'],
                            )
                        User_contacts_entry.save()
                        return render(request,'dashboard/user/emergency_data.html',{'user':m,'form':emergency_contacts_f,'message':'Successfully Added','ftable':t})
                    return render(request,'dashboard/user/emergency_data.html',{'user':m,'form':emergency_contacts_f,'message':'Invalid Details','ftable':t})
                emergency_contacts_f=user_emergency_contacts()   
                return render(request,'dashboard/user/emergency_data.html',{'user':m,'form':emergency_contacts_f,'message':'','ftable':t})
            except Exception as e:
                return render(request,'dashboard/user/emergency_data.html',{'user':m,'form':emergency_contacts_f,'message':e,'ftable':t})
    #   return HttpResponse(e)  
    # except Exception as e:
    #   return HttpResponse(e)
    return HttpResponse("Not Eligible to View 2")
def delete_emergency_contact(request,user):
    try:
        if 'username' in request.session:
            if user==request.session['username']:
                Contactid=str(request.GET.get('Contactid', None))
                m=User.objects.get(user_name=user)
                t=User_contacts.objects.filter(user=m,id=Contactid)
                t.delete();
                response_data = {}
                response_data['result'] = "Successfully Deleted Contact"
                return JsonResponse(response_data)
        response_data = {}
        response_data['result'] = "Authorization Breach"
        return JsonResponse(response_data)
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("Not Eligible to View 2")
def prv_cases(request,user):
    m=User.objects.get(user_name=user)
    if 'username' in request.session:
        if user==request.session['username']:
            try:
                import json
                cases_=User_doctor_case.objects.filter(user=m)
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
                return render(request,'dashboard/user/prv_cases.html',{'user':m,'cases_':cases_})
            except Exception as e:
                return render(request,'dashboard/user/prv_cases.html',{'user':m,'cases_':str(e)})
    return HttpResponse("Not Eligible to View 2")

def curr_med(request,user):
    m=User.objects.get(user_name=user)
    if 'username' in request.session:
        if user==request.session['username']:
            try:
                user_medicines_e=User_medicine_own.objects.filter(user=m)
                return render(request,'dashboard/user/curr_med.html',{'user':m,'user_medicines_e':user_medicines_e})
            except Exception as e:
                return render(request,'dashboard/user/curr_med.html',{'user':m})
    return HttpResponse("Not Eligible to View 2")

def pend_rep(request,user):
    m=User.objects.get(user_name=user)
    if 'username' in request.session:
        if user==request.session['username']:
            try:
                ftb=User_fb.objects.filter(user_name=user)
                return render(request,'dashboard/user/pend_rep.html',{'user':m,'ftable':ftb})
            except Exception as e:
                return render(request,'dashboard/user/pend_rep.html',{'user':m})
    return HttpResponse("Not Eligible to View 2")

def prev_rep(request,user):
    m=User.objects.get(user_name=user)
    if 'username' in request.session:
        if user==request.session['username']:
            try:
                
                return render(request,'dashboard/user/prev_rep.html',{'user':m})
            except Exception as e:
                return render(request,'dashboard/user/prev_rep.html',{'user':m})
    return HttpResponse("Not Eligible to View 2")
def getajaxlab(request,user):
    m=User.objects.get(user_name=user)
    if 'username' in request.session:
        if user==request.session['username']:
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
    m=User.objects.get(user_name=user)
    if 'username' in request.session:
        if user==request.session['username']:
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
    m=User.objects.get(user_name=user)
    if 'username' in request.session:
        if user==request.session['username']:
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

