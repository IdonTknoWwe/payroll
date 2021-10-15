from django.conf.urls import url
from django.contrib import admin
from apps.enterprise import views


urlpatterns = [
	url(r'^create/$', views.EnterpriseCreateView.as_view(), name = 'crearEmpresa'),
	url(r'^list/$', views.EnterpriseListView.as_view(), name = 'listarEmpresa'),
	url(r'^edit/(?P<pk>\d+)/$', views.EnterpriseEditView.as_view(), name="editarEmpresa"),
	url(r'^new/$', views.EnterpriseNewView.as_view(), name = 'nuevaEmpresa'),
	url(r'^save/$', views.EnterpriseSaveView.as_view(), name = 'guardarEmpresa'),
]