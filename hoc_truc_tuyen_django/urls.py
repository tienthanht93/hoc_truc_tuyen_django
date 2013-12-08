from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hoc_truc_tuyen_django.views.home', name='home'),
    # url(r'^hoc_truc_tuyen_django/', include('hoc_truc_tuyen_django.foo.urls')),

    url(r'^$','trac_nghiem.views.home'),
    url(r'^lession/(?P<lession>\d+)','trac_nghiem.views.lession'),
    url(r'^reload-lession/(?P<lession>\d+)','trac_nghiem.views.reload_lesssion'),
    url(r'^add','trac_nghiem.views.add'),
    url(r'^account/auth','trac_nghiem.views.auth_view'),
    url(r'^account/logout','trac_nghiem.views.logout'),
    url(r'^account/loggedin','trac_nghiem.views.loggedin'),
    url(r'^account/invalid','trac_nghiem.views.invalid_login'),
    url(r'^account/register/','trac_nghiem.views.register_user'),
    url(r'^account/register_success/','trac_nghiem.views.register_success'),
    url(r'^create-question','trac_nghiem.views.createQuestion'),
    url(r'^check-answer','trac_nghiem.views.check_answer'),
    url(r'^statistic','trac_nghiem.views.statistic'),
    url(r'^ignore-question','trac_nghiem.views.ignore_question'),
    url(r'^doimatkhau','trac_nghiem.views.changePassword'),
    url(r'^profile','trac_nghiem.views.profile'),
    url(r'^question-list','trac_nghiem.views.questionList'),
    url(r'^edit-question','trac_nghiem.views.editQuestion'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
