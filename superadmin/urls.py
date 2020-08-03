from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.login, name='login'),
	url(r'^login$',views.login, name='login'),
	url(r'^forgot_pass$',views.forgot_pass, name='forgot_pass'),
	url(r'^forgot_pass_chg/(?P<user>\w+)$',views.forgot_pass_chg, name='forgot_pass_chg'),
	url(r'^user_verify_email/(?P<user>\w+)$',views.user_verify_email, name='user_verify_email'),
	url(r'^regenerate_otp/(?P<user>\w+)$',views.regenerate_otp, name='regenerate_otp'),
	url(r'^otp_email_chg/(?P<user>\w+)$',views.otp_email_chg, name='otp_email_chg'),
	url(r'^dashboard/(?P<user>\w+)$',views.dashboard, name='dashboard'),
	url(r'^logout/(?P<user>\w+)$',views.logout, name='logout'),
	url(r'^register$',views.register, name='register'),
	url(r'^activity_log/(?P<user>\w+)$',views.activity_log,name='activity_log'),
	url(r'^profile/(?P<user>\w+)$',views.profile,name='profile'),
	url(r'^settings/(?P<user>\w+)$',views.settings,name='settings'),
	url(r'^chg_passwd/(?P<user>\w+)$',views.chg_passwd,name='chg_passwd'),
	url(r'^approveDoctor/(?P<user>\w+)$',views.approveDoctor,name='approveDoctor'),
	url(r'^manageDoctorAJAX/(?P<user>\w+)$',views.manageDoctorAJAX,name='manageDoctorAJAX'),
	
	url(r'^manageLabAJAX/(?P<user>\w+)$',views.manageLabAJAX,name='manageLabAJAX'),
	url(r'^manage_doctors/(?P<user>\w+)$',views.manage_doctors,name='manage_doctors'),
	url(r'^approveDoctor/approveDoctorAJAX/(?P<user>\w+)$',views.approveDoctorAJAX,name='approveDoctorAJAX'),
	url(r'^user_feedback/(?P<user>\w+)$',views.user_feedback,name='user_feedback'),
	url(r'^user_session/(?P<user>\w+)$',views.user_session,name='user_session'),
	url(r'^manage_users/(?P<user>\w+)$',views.manage_users,name='manage_users'),
	url(r'^manage_users/manage_usersAJAX/(?P<user>\w+)$',views.manage_usersAJAX,name='manage_usersAJAX'),
	url(r'^doctor_session/(?P<user>\w+)$',views.doctor_session,name='doctor_session'),
	url(r'^doctor_feedback/(?P<user>\w+)$',views.doctor_feedback,name='doctor_feedback'),
	url(r'^lab_sesssion/(?P<user>\w+)$',views.lab_sesssion,name='lab_sesssion'),
	url(r'^lab_feedback/(?P<user>\w+)$',views.lab_feedback,name='lab_feedback'),
	url(r'^pharm_session/(?P<user>\w+)$',views.pharm_session,name='pharm_session'),
	url(r'^pharm_feedback/(?P<user>\w+)$',views.pharm_feedback,name='pharm_feedback'),


	url(r'^user_emergency/(?P<user>\w+)$',views.user_emergency,name='user_emergency'),
	url(r'^user_health/(?P<user>\w+)$',views.user_health,name='user_health'),
	url(r'^approveLab/(?P<user>\w+)$',views.approveLab,name='approveLab'),
	url(r'^approveLabAJAX/(?P<user>\w+)$',views.approveLabAJAX,name='approveLabAJAX'),
	url(r'^manage_labs/(?P<user>\w+)$',views.manage_labs,name='manage_labs'),
	url(r'^approvePharm/(?P<user>\w+)$',views.approvePharm,name='approvePharm'),
	url(r'^manage_pharms/(?P<user>\w+)$',views.manage_pharms,name='manage_pharms'),
	url(r'^approvePharmAJAX/(?P<user>\w+)$',views.approvePharmAJAX,name='approvePharmAJAX'),
	url(r'^managePharmAJAX/(?P<user>\w+)$',views.managePharmAJAX,name='managePharmAJAX'),

	url(r'^getajaxlab/(?P<user>\w+)$',views.getajaxlab,name='getajaxlab'),
	url(r'^get_cons_medicine/(?P<user>\w+)$',views.get_cons_medicine,name='get_cons_medicine'),
	url(r'^get_cons_doc/(?P<user>\w+)$',views.get_cons_doc,name='get_cons_doc'),



]