from django.conf.urls import url
from django.contrib import admin
from apps.administracion import views

urlpatterns = [
	url(r'^scheme/create/$', views.PaymentSchemeCreateView.as_view(), name = 'crearEsquema'),
	url(r'^scheme/list/$', views.PaymentSchemeListView.as_view(), name = 'listarEsquema'),
	url(r'^scheme/edit/(?P<pk>\d+)/$', views.PaymentSchemeEditView.as_view(), name="editarEsquema"),
]