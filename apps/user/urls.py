from django.conf.urls import url
from django.contrib import admin
from .views import LoginView, LogoutView, CreateUser

urlpatterns = [
	url(r'^login/$', LoginView, name = 'login'),
	url(r'^logout/$', LogoutView, name = 'logout'),
	url(r'^register/$', CreateUser.as_view(), name = 'registrar'),
]