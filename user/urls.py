from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.login, name='login'),
	url(r'^getselected_area$',views.getselected_area,name='getselected_area'),
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
	url(r'^givefeed/(?P<user>\w+)$',views.givefeed,name='givefeed'),
	url(r'^showfeed/(?P<user>\w+)$',views.showfeed,name='showfeed'),
	url(r'^basic_med/(?P<user>\w+)$',views.basic_med,name='basic_med'),
	url(r'^surgical_data/(?P<user>\w+)$',views.surgical_data,name='surgical_data'),
	url(r'^medicinal_data/(?P<user>\w+)$',views.medicinal_data,name='medicinal_data'),
	url(r'^emergency_data/(?P<user>\w+)$',views.emergency_data,name='emergency_data'),
	url(r'^delete_emergency_contact/(?P<user>\w+)$',views.delete_emergency_contact,name='delete_emergency_contact'),
	url(r'^delete_surgical_data/(?P<user>\w+)$',views.delete_surgical_data,name='delete_surgical_data'),

	url(r'^prv_cases/(?P<user>\w+)$',views.prv_cases,name='prv_cases'),
	url(r'^curr_med/(?P<user>\w+)$',views.curr_med,name='curr_med'),
	url(r'^pend_rep/(?P<user>\w+)$',views.pend_rep,name='pend_rep'),
	url(r'^prev_rep/(?P<user>\w+)$',views.prev_rep,name='prev_rep'),
	url(r'^getajaxlab/(?P<user>\w+)$',views.getajaxlab,name='getajaxlab'),
	url(r'^get_cons_medicine/(?P<user>\w+)$',views.get_cons_medicine,name='get_cons_medicine'),
	url(r'^get_cons_doc/(?P<user>\w+)$',views.get_cons_doc,name='get_cons_doc'),
]