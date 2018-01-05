from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^login/',views.login_user,name='login'),
     url(r'^logout/',views.logout_user,name='logout'),
      url(r'^register/',views.register,name='register'),
      url(r'^dashboard/user',views.bUser,name='bUser'),
      url(r'^dashboard/',views.dashboard,name='dashboard'),
	  	url(r'^details/(?P<cid>[0-9]+)/',views.details,name='details'),
	url(r'^enroll/(?P<cid>[0-9]+)/',views.enroll,name='enroll'),
	url(r'^display/',views.display,name='display'),  
        url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'), 
        url(r'^search/',views.search,name='search'),
		url(r'^calendar/',views.calendar,name='calendar'),
        
    
]