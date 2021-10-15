from django.shortcuts import render
from .forms import EnterpriseForm
from .models import EnterpriseModel
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, UpdateView
from django.db import IntegrityError, transaction
from django.http import JsonResponse
import json
import sys
import re
#django-braces importacion 
from braces.views import LoginRequiredMixin
from apps.user.views import PermissionMixin
from django.http import Http404

# Create your views here.

class EnterpriseCreateView(LoginRequiredMixin, PermissionMixin, CreateView):
	model = EnterpriseModel
	form_class = EnterpriseForm
	template_name = 'templates/enterprise/create.html'
	success_url = reverse_lazy('Empresas:listarEmpresa')
	login_url = '/'
	redirect_field_name = 'login'

class EnterpriseListView(LoginRequiredMixin, PermissionMixin, ListView):
	model = EnterpriseModel
	template_name = 'templates/enterprise/listar.html'
	login_url = '/'
	redirect_field_name = 'login'

class EnterpriseEditView(LoginRequiredMixin, PermissionMixin, UpdateView):
	model = EnterpriseModel
	form_class =  EnterpriseForm
	template_name = 'templates/enterprise/editar.html'
	success_url = reverse_lazy('Empresas:listarEmpresa')
	login_url = '/'
	redirect_field_name = 'login'

class EnterpriseNewView(LoginRequiredMixin, PermissionMixin, TemplateView):
	template_name = 'templates/enterprise/new.html'

	def post(self, request, *args, **kwargs):
		listaEmpresa = []
		name = '^([\D]+)$'
		primss = '^(([0-9]){1,2}([.])([0-9]){2})$'
		rfc = '^(([A-Z]{3,4})(([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1]))([A-Z\d]{3}))$'
		dateConstitution = '^(((19|20)\d{2})-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01]))$'
		datePower = '^(((19|20)\d{2})-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01]))$'

		contador = 0
		try:
			mi_json = json.loads(request.POST['xls'])
			empresas = mi_json['Hoja1']
			for i in empresas:
				if re.match(name, i['NOMBRE']) == None:
					contador +=1
				if re.match(primss, i['PRIMA RIESGO']) == None:
					contador +=1
				if re.match(rfc, i['RFC']) == None:
					contador +=1
				if re.match(dateConstitution, i['FECHA CONSTITUCION'])== None:
					contador +=1
				if re.match(datePower, i['FECHA PODER']) == None:
					contador +=1
				dicEmpresa = ({'name': i['NOMBRE'], 'primss': i['PRIMA RIESGO'], 'rfc': i['RFC'], 'dateConstitution': i['FECHA CONSTITUCION'], 'datePower': i['FECHA PODER']})
				listaEmpresa.append(dicEmpresa)

			if contador > 0:
				raise Http404
		except:
			raise Http404
		return JsonResponse({'detail': listaEmpresa})

	login_url = '/'
	redirect_field_name = 'login'

class EnterpriseSaveView(LoginRequiredMixin, TemplateView):
	def post(self, request, *args, **kwargs):
		mi_json = json.loads(request.POST['xls'])
		try:
			with transaction.atomic():
				for recorre in mi_json:
					empresa = EnterpriseModel(name = recorre['name'],primss = recorre['primss'], rfc = recorre['rfc'], dateConstitution = recorre['dateConstitution'], datePower = recorre['datePower'])
					empresa.save()
                            
		except IntegrityError:
			raise Http404
		return JsonResponse({'detail': 1 })
	login_url = '/'
	redirect_field_name = 'login'