from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^login/',views.login_user,name='login'),
    url(r'^logout/',views.logout_user,name='logout'),
    url(r'^register/',views.register,name='register'),
    url(r'^dashboard/user',views.bUser,name='bUser'),
    url(r'^dashboard/',views.dashboard,name='dashboard'),
	  url('^details/(?P<cid>[0-9]+)/',views.details,name="details"),
	  url('^update/(?P<cid>[0-9]+)/',views.update,name="update"),			  
    url(r'^manage/',views.mClass,name='mClass'),
    url(r'^addClass/',views.addClass,name="addClass"),
    url(r'^delete/(?P<cid>[0-9]+)/',views.delete,name="delete"),
    url(r'^sDetails/(?P<studentid>[0-9]+)/(?P<cid>[0-9]+)/delete/',views.sDelete,name="sDelete"),
    url(r'^manageStudents/',views.mStudent,name="mStudent"),
    url(r'^sDetails/(?P<studentid>[0-9]+)/(?P<cid>[0-9]+)/',views.sDetails,name="sDetails"),
    url(r'^regInstructor/(?P<uid>[0-9]+)/',views.RegInstructor,name='RegInstructor'),
    url(r'^manageInstructor/',views.mInstructor,name='mInstructor'),
    url(r'^addInstructor/',views.addInstructor,name='addInstructor'),
<<<<<<< HEAD
    url(r'^deleteInstructor/(?P<iid>[0-999]+)/',views.deleteInstructor,name='deleteInstructor'),
    url(r'^instructordetails/(?P<iid>[0-999]+)/',views.instructordetails,name='instructordetails'), 
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^clone/(?P<cid>[0-999]+)/',views.clone,name="clone"),
	url(r'^calendar/',views.calendar,name='calendar'),
    url(r'^search/',views.search,name='search'),
=======
    url(r'^deleteInstructor/(?P<iid>[0-9]+)/',views.deleteInstructor,name='deleteInstructor'),
    url(r'^instructordetails/(?P<iid>[0-9]+)/',views.instructordetails,name='instructordetails'), 
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^clone/(?P<cid>[0-9]+)/',views.clone,name="clone"),
	url(r'^calendar/',views.calendar,name='calendar'),
    url(r'^search/',views.search,name='search'),
    url(r'^csearch/',views.csearch,name='csearch'),
    url(r'^msearch/',views.msearch,name='msearch'),
>>>>>>> dbbfffd1c4188f935f01bc76dda88bbbd4e6509b
]