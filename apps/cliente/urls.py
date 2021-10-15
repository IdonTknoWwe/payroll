from django.conf.urls import url
from django.contrib import admin
from apps.cliente import views



urlpatterns = [
	url(r'^information/(?P<pk>\d+)/$', views.ClientInfoView.as_view(), name="informacionCliente"),
	url(r'^create/$', views.ClientCreateView.as_view(), name = 'crearCliente'),
	url(r'^list/$', views.ClientListView.as_view(), name = 'listarCliente'),
	url(r'^edit/(?P<pk>\d+)/$', views.ClientEditView.as_view(), name = 'editarCliente'),
	url(r'^new/$', views.ClienteNewView.as_view(), name = 'nuevoCliente'),
	url(r'^save/$', views.ClienteSaveView.as_view(), name = 'guardaCliente'),
	url(r'^(?P<pk>\d+)/payroll/$', views.ClientPayrollView.as_view(), name = 'nominaEmpleado'),
	url(r'^(?P<pk>\d+)/process/$', views.PayrollSaveView.as_view(), name = 'guardaNominaEmpleado'),
	url(r'^(?P<pk>\d+)/statusPayroll/$', views.PayrollStatusView.as_view(), name = 'statusNomina'),
	url(r'^queryPayroll/$', views.PayrollQueryView.as_view(), name = 'consultaNomina'),
	url(r'^queryPayrollEmployee/$', views.PayrollDetailView.as_view(), name = 'consultaNominaEmpleado'),
	url(r'^(?P<pk>\d+)/revised/$', views.PayrollReviewView.as_view(), name= 'revisadaNomina'),
	url(r'^detail/$', views.PayrollReviewDetailView.as_view(), name= 'nominaEjecutivo'),


]