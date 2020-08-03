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
	url(r'^showfeed/(?P<user>\w+)$',views.showfeed,name='showfeed'),
	url(r'^givefeed/(?P<user>\w+)$',views.givefeed,name='givefeed'),
	url(r'^takepatient/(?P<user>\w+)$',views.takepatient,name='takepatient'),
	url(r'^takepatient_otp_user/(?P<user>\w+)$',views.takepatient_otp_user,name='takepatient_otp_user'),
	url(r'^enter_case/(?P<user>\w+)$',views.enter_case,name='enter_case'),
	url(r'^medicine_deliver/(?P<user>\w+)$',views.medicine_deliver,name='medicine_deliver'),
	url(r'^prev_cases/(?P<user>\w+)$',views.prev_cases,name='prev_cases')
]