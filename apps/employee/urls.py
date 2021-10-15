from django.conf.urls import url
from django.contrib import admin
from apps.employee import views


urlpatterns = [
	url(r'^create/$', views.EmployeeCreateView.as_view(), name = 'crearEmpleado'),
	url(r'^list/$', views.EmployeeListView.as_view(), name = 'listarEmpleado'),
	url(r'^edit/(?P<pk>\d+)/$', views.EmployeeEditView.as_view(), name="editarEmpleado"),
	url(r'^new/$', views.EmployeeCreatingView.as_view(), name = 'crearEmpleados'),
	url(r'^save/$', views.EmployeeSaveView.as_view(), name = 'guardarEmpleados'),

]