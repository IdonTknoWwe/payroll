from django.shortcuts import render
from apps.administracion.models import PaymentSchemeModel
from apps.administracion.serializer import PaymentSchemeSerializer
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import PaymentSchemeModel 
from .forms import PaymentSchemeForm
from django.core.urlresolvers import reverse_lazy
from braces.views import LoginRequiredMixin
from apps.user.views import PermissionMixin


#class PaymentSchemeViewset(viewset.ModelViewset):
#    serializer_class = PaymentSchemeSerializer
#    queryset = PaymentSchemeModel.objects.all()

class PaymentSchemeCreateView(LoginRequiredMixin, PermissionMixin, CreateView):
	model = PaymentSchemeModel
	form_class = PaymentSchemeForm
	template_name = 'templates/administracion/create.html'
	success_url = reverse_lazy('Administracion:listarEsquema')
	login_url = '/'
	redirect_field_name = 'login'

class PaymentSchemeListView(LoginRequiredMixin, PermissionMixin, ListView):
	model = PaymentSchemeModel
	template_name = 'templates/administracion/listar.html'
	login_url = '/'
	redirect_field_name = 'login'

class PaymentSchemeEditView(LoginRequiredMixin, PermissionMixin, UpdateView):
	model = PaymentSchemeModel
	form_class = PaymentSchemeForm
	template_name = 'templates/administracion/editar.html'
	success_url = reverse_lazy('Administracion:listarEsquema')
	login_url = '/'
	redirect_field_name = 'login'