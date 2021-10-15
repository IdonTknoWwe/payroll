#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView, DetailView
from apps.employee.models import EmployeeModel, DataPayrollModel, PaymentEmployeeSchemaModel
from apps.enterprise.models import EnterpriseModel
from django.core.urlresolvers import reverse_lazy
from apps.cliente.calculos import nomina
from braces.views import LoginRequiredMixin, MultiplePermissionsRequiredMixin
from django.shortcuts import render
from .forms import ClientForm, FileForm
from .models import ClienteModel, FileModel, PayeeIdModel, PermitsModel
from django.http import JsonResponse
from django.utils import timezone
from django.db import IntegrityError, transaction
from django.shortcuts import redirect
from apps.user.views import PermissionMixin
import json
import sys
import re
from django.http import Http404
# from aplicaciones.UserModel.views import PermissionMixin
# Create your views here.

class ClientInfoView(LoginRequiredMixin, DetailView):
	template_name = 'templates/cliente/informacion.html'
	model = ClienteModel

	def get_context_data(self, **kwargs):
		context = super(ClientInfoView, self).get_context_data(**kwargs)
		if not self.request.user:
			raise Http404
		permisos = PermitsModel.objects.filter(user=self.request.user, cliente=self.get_object())
		if len(permisos) == 0:
			raise Http404

		cliente = ClienteModel.objects.get(rfc=self.get_object())
		context['id'] = cliente.id
		context['name'] = cliente.name

		return context

class ClientCreateView(LoginRequiredMixin, PermissionMixin, CreateView):
	model = ClienteModel
	form_class = ClientForm
	template_name = 'templates/cliente/create.html'
	success_url = reverse_lazy('Clientes:listarCliente')
	login_url ='/'
	redirect_field_name = 'login'

class ClientListView(LoginRequiredMixin, PermissionMixin, ListView):
	model = ClienteModel
	template_name = 'templates/cliente/listar.html'
	login_url = '/'
	redirect_field_name = 'login'

class ClientEditView(LoginRequiredMixin, PermissionMixin, UpdateView):
	model = ClienteModel
	form_class =  ClientForm
	template_name = 'templates/cliente/editar.html'
	success_url = reverse_lazy('Clientes:listarCliente')
	login_url = '/'
	redirect_field_name = 'login'

class ClienteNewView(LoginRequiredMixin, PermissionMixin, TemplateView):
	template_name = 'templates/cliente/new.html'
	def post(self, request, *args, **kwargs):
		listaCliente = []
		name = '^([\D]+)$'
		commission = '^(([0-9]){1,2}([.])([0-9]){1,2})$'
		statusClient = '^[1-3]{1}$'
		rfc = '^(([A-Z]{3,4})(([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1]))([A-Z\d]{3}))$'
		primssAgreed = '^(([0-9]){1,2}([.])([0-9]){1,2})$'
		dateConstitution = '^(((19|20)\d{2})-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01]))$'
		datePower = '^(((19|20)\d{2})-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01]))$'
		contador = 0
		try:
			mi_json = json.loads(request.POST['xls'])
			clientes = mi_json['Hoja1']
			for i in clientes:
				if re.match(name, i['NOMBRE']) == None:
					contador +=1
				if re.match(commission, i['COMISION']) == None:
					contador +=1
				if re.match(statusClient, i['PRIORIDAD']) == None:
					contador +=1
				if re.match(rfc, i['RFC']) == None:
					contador +=1
				if re.match(primssAgreed, i['PRIMA ACORDADA']) == None:
					contador +=1
				if re.match(dateConstitution, i['FECHA CONSTITUCION'])== None:
					contador +=1
				if re.match(datePower, i['FECHA PODER']) == None:
					contador +=1

				dicCliente = ({'name': i['NOMBRE'] ,'commission': i['COMISION'], 'statusClient': i['PRIORIDAD'], 'rfc': i['RFC'], 'primssAgreed': i['PRIMA ACORDADA'], 'dateConstitution': i['FECHA CONSTITUCION'], 'datePower': i['FECHA PODER']})
				listaCliente.append(dicCliente)

			if contador > 0:
				raise Http404	
		except:
			raise Http404
		return JsonResponse({'detail': listaCliente})

	login_url = '/'
	redirect_field_name = 'login'

class ClienteSaveView(LoginRequiredMixin, TemplateView):
	def post(self, request, *args, **kwargs):
		mi_json = json.loads(request.POST['xls'])
		try:
			with transaction.atomic():
				for recorre in mi_json:
					cliente = ClienteModel(name = recorre['name'],commission = recorre['commission'], statusClient =recorre['statusClient'], rfc = recorre['rfc'],primssAgreed = recorre['primssAgreed'], dateConstitution = recorre['dateConstitution'], datePower = recorre['datePower'])
					cliente.save()      
		except IntegrityError:
			raise Http404
		return JsonResponse({'detail': 1 })
	login_url = '/'
	redirect_field_name = 'login'


class ClientPayrollView(LoginRequiredMixin, CreateView):	
	model = FileModel
	form_class = FileForm
	template_name = 'templates/payroll/payroll.html'
	success_url = reverse_lazy('Clientes:listarCliente')

	def get_context_data(self, **kwargs):
		context = super(ClientPayrollView, self).get_context_data(**kwargs)
		permisos = PermitsModel.objects.filter(user=self.request.user, cliente=ClienteModel.objects.get(pk=int(self.kwargs['pk'])))
		longitud = len(permisos)
		dias = EmployeeModel.objects.filter(cliente=ClienteModel.objects.get(pk=int(self.kwargs['pk'])))
		listaDias = []
		for i in dias:
			listaDias.append(i.payroll)
		if longitud == 0:
			raise Http404
		cliente = ClienteModel.objects.get(pk=int(self.kwargs['pk']))
		context['id'] = cliente.id
		context['rfcClient'] = cliente.rfcClient
		context['diasNomina'] = sorted(set(listaDias))
		return context

	def post(self, request, *args, **kwargs):
		cadena = '^([\D]+)$'
		rfcClient  = '^(([A-Z]{3,4})(([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1]))([A-Z\d]{3}))$'
		numero = '^(([0-9]*)([.])([0-9]){2})$'
		vFaltas  = '^([0-9]{1,2})$'
		contador = 0
		listaNomina = []
		contadorFaltas = 0 
		contadorIsr = 0
		contadorImss = 0
		contadorGratificacion = 0
		contadorDescuento = 0
		contadorInfonavit = 0
		contadorFonacot = 0
		contadorPension = 0
		contadorOtros = 0
		contadorCaja = 0
		contadorGastos = 0
		contadorPrestamos = 0
		contadorBolsaRepartir = 0
		contadorEfectivo = 0
		contadorAsimilados = 0
		contadorVales = 0
		contadorTerceros = 0
		contadorFamiliares = 0
		contadorSobrante = 0
		listaNomina = []
		listaExcel = []
		errores = 0
		try:

			mi_json = json.loads(request.POST['xls'])
			datos = mi_json['Hoja1']
			select =  json.loads(request.POST['select'])
			listaEmpleados = EmployeeModel.objects.filter(cliente=ClienteModel.objects.get(pk=int(self.kwargs['pk'])))
			listaExcel = []
			for a in datos:
				if re.match(cadena, a['APELLIDO PATERNO']) == None:
					contador +=1
				if re.match(cadena, a['APELLIDO MATERNO']) == None:
					contador +=1
				if re.match(cadena, a['NOMBRE(S)']) == None:
					contador +=1
				if re.match(rfcClient, a['RFC']) == None:
					contador +=1
				if re.match(numero, a['GRATIFICACION']) == None:
					contador +=1
				if re.match(numero, a['DESCUENTO']) == None:
					contador +=1
				if re.match(vFaltas, a['FALTAS']) == None:
					contador +=1
				if re.match(numero, a['CAJA DE AHORRO']) == None:
					contador +=1
				if re.match(numero, a['GASTOS MEDICOS']) == None:
					contador +=1
				if re.match(numero, a['PRESTAMOS']) == None:
					contador +=1
				if re.match(numero, a['OTROS']) == None:
					contador +=1

				if a['RFC'] not in listaExcel:
					listaExcel.append(a['RFC'])


			if contador > 0 :
				errores = -2
			listaActual = []
			for b in listaEmpleados:
				listaActual.append(b.rfc)

			contadorEmpleados =0
			for c in listaExcel:
				existe = c in listaActual
				if existe == True:
					contadorEmpleados +=1

			if len(listaEmpleados) != contadorEmpleados:
				errores = -3
			else:
				try:
					for d in datos:
						empleado = EmployeeModel.objects.get(apPaterno = d['APELLIDO PATERNO'], apMaterno = d['APELLIDO MATERNO'], name = d['NOMBRE(S)'], rfc = d['RFC'])
				# 		if str(empleado.cliente) != str(ClienteModel.objects.get(pk=int(self.kwargs['pk']))):
				# 			raise Http404
						if select == empleado.payroll:
							data = nomina.calculaNomina(empleado.rfc, d['GRATIFICACION'], d['DESCUENTO'], d['FALTAS'] )
							dicNomina = ({'apPaterno': empleado.apPaterno, 'apMaterno': empleado.apMaterno, 'name': empleado.name, 'rfc': empleado.rfc, 'monthlySalary' : round(empleado.realMonthlySalary, 2), 'calculation': data[0], 'salaryImss': round(data[1], 2), 'faults': round(data[2], 2), 'isr': round(data[3], 2), 'imss': round(data[4], 2), 'discounts': round(data[5], 2), 'creditInfonavit': round(data[6], 2), 'creditFonacot': round(data[7], 2), 'alimony': round(data[8], 2), 'others': round(data[9], 2), 'savingsAccount': round(data[10], 2), 'medicalExpenses': round(data[11], 2), 'loans': round(data[12], 2), 'stateTax': round(data[13], 2), 'socialBurden': round(data[14], 2), 'gratification': round(data[15], 2), 'paySalary': round(data[16], 2), 'bagToDeal': round(data[17], 2), 'cash': round(data[18], 2), 'assimilated': round(data[19], 2), 'thirdParties': round(data[20], 2), 'pantryVouchers': round(data[21], 2), 'family': round(data[22], 2), 'surplus': round(data[23], 2), 'netReceived': round(data[24], 2)})
							listaNomina.append(dicNomina)
							contadorFaltas += data[2]
							contadorIsr += data[3]
							contadorImss += data[4]
							contadorDescuento += data[5]
							contadorInfonavit += data[6]
							contadorFonacot += data[7]
							contadorPension += data[8]
							contadorOtros += data[9]
							contadorCaja += data[10]
							contadorGastos += data[11]
							contadorPrestamos += data[12]
							contadorGratificacion += data[15]
							contadorBolsaRepartir += data[17]
							contadorEfectivo += data[18]
							contadorAsimilados += data[19]
							contadorTerceros +=  data[20]
							contadorVales +=  data[21]
							contadorFamiliares += data[22]
							contadorSobrante += data[23]
				except:
					errores = -4
		except :
			errores = -1
		listaContadores = []
		contadores = ({'faltas': contadorFaltas, 'isr': contadorIsr, 'imss': contadorImss, 'descuento': contadorDescuento, 'infonavit': contadorInfonavit, 'fonacot': contadorFonacot, 'pension': contadorPension, 'otros': contadorOtros, 'caja': contadorCaja, 'gastos': contadorGastos, 'prestamos': contadorPrestamos, 'gratificacion': contadorGratificacion, 'bolsa': contadorBolsaRepartir, 'efectivo': contadorEfectivo, 'asimilados': contadorAsimilados, 'terceros': contadorTerceros, 'vales': contadorVales, 'familiares': contadorFamiliares, 'sobrante': contadorSobrante })
		listaContadores.append(contadores)
		return JsonResponse({'error': 0, 'detail': listaNomina, 'contadores': listaContadores})

	login_url = '/'
	redirect_field_name = 'login'

class PayrollSaveView(LoginRequiredMixin, TemplateView):

	def post(self, request, *args, **kwargs):
		clienteRfc =ClienteModel.objects.get(pk=int(self.kwargs['pk']))
		try:
			with transaction.atomic():
				datos = json.loads(request.POST['xls'])
				form = FileForm(request.POST, request.FILES)
				if form.is_valid():
					form.save()
				else:
					raise Http404
				fecha = FileModel.objects.filter(cliente=clienteRfc).latest('createDate')
				for i in datos:
		 			empleado = EmployeeModel.objects.get(rfc= i['rfc'])
		 			rfcCliente = str(empleado.cliente)
		 			empresas = PaymentEmployeeSchemaModel.objects.filter(employeemodel=empleado)
		 			empresaNomina = EnterpriseModel.objects.get(rfc=empresas[0])
		 			empresaEfectivo = EnterpriseModel.objects.get(rfc=empresas[1])
		 			empresaAsimilados = EnterpriseModel.objects.get(rfc=empresas[2])
		 			empresaVales = EnterpriseModel.objects.get(rfc=empresas[3])
		 			empresaTerceros = EnterpriseModel.objects.get(rfc=empresas[4])
		 			empresaFamiliares = EnterpriseModel.objects.get(rfc=empresas[5])
		 			
		 			payroll = DataPayrollModel(apPaterno = i['apPaterno'], apMaterno = i['apMaterno'], name = i['name'] , rfc = i['rfc'], monthlySalary  = i['monthlySalary'], calculation = i['calculation'], salaryImss = i['salaryImss'], faults = i['faults'], isr = i['isr'], imss = i['imss'], discounts = i['discounts'], creditInfonavit = i['creditInfonavit'], creditFonacot = i['creditFonacot'], alimony = i['alimony'], others = i['others'], savingsAccount = i['savingsAccount'], medicalExpenses = i['medicalExpenses'], loans = i['loans'], stateTax = i['stateTax'], socialBurden = i['socialBurden'], gratification = i['gratification'], paySalary = i['paySalary'], bagToDeal = i['bagToDeal'], cash = i['cash'], assimilated = i['assimilated'], thirdParties = i['thirdParties'], pantryVouchers = i['pantryVouchers'], family = i['family'], surplus = i['surplus'], netReceived = i['netReceived'], daysPayroll = empleado.payroll, identifier = fecha.id, statusPayroll = 0 , cliente = rfcCliente, businessRoster = empresaNomina, businessCash = empresaEfectivo, businessAssimilated = empresaAsimilados, businessPantryVouchers = empresaVales, businessTthirdParties = empresaTerceros, businessFamily = empresaFamiliares)
		 			
		 			payroll.save()
		
		except IntegrityError:
			raise Http404
			
		return JsonResponse({'detail': 0})

	login_url = '/'
	redirect_field_name = 'login'

class PayrollStatusView(LoginRequiredMixin,  DetailView):
	template_name = 'templates/payroll/status.html'
	model = ClienteModel

	def get_context_data(self, **kwargs):
		context = super(PayrollStatusView, self).get_context_data(**kwargs)
		if not self.request.user:
			raise Http404
		permisos = PermitsModel.objects.filter(user=self.request.user, cliente=self.get_object())
		if len(permisos) == 0:
			raise Http404
		cliente = FileModel.objects.filter(cliente=self.get_object())
		nominas = []
		for i in cliente:
			dicNomina = ({'id': i.id, 'creacion': i.createDate})
			nominas.append(dicNomina)
		context['nominas'] = nominas
		return context

	login_url = '/'
	redirect_field_name = 'login'


class PayrollQueryView(LoginRequiredMixin, TemplateView):
		
	def get(self, request, *args, **kwargs):
		if not request.GET['id']:
			raise Http404
		cliente = FileModel.objects.get(id=request.GET['id'])
		inicio = cliente.startPayroll
		final = cliente.endPayroll
		pago = cliente.datePayroll
		status = None
		if cliente.status == 0:
			status = 'En Revision'
		elif cliente.status == 1:
			status = 'En Dispersion'
		else:
			status = 'Pagada'

		listaNomina = []
		try:
			nomina = DataPayrollModel.objects.filter(identifier= cliente.id)
			for i in nomina:
				dicNomina = ({'rfc': i.rfc, 'apPaterno': i.apPaterno, 'apMaterno': i.apMaterno, 'nombre': i.name, 'sueldoMensual':i.monthlySalary, 'calculo': i.calculation, 'id': i.id})
				listaNomina.append(dicNomina)

		except IntegrityError:
			raise Http404

		return JsonResponse({'nomina': listaNomina, 'status': status, 'inicio': inicio, 'final': final, 'pago': pago})
	login_url = '/'
	redirect_field_name = 'login'

class PayrollDetailView(LoginRequiredMixin, TemplateView):

	 def get(self, request, *args, **kwargs):
	 	if not request.GET['id']:
	 		raise Http404
	 	detallesNomina = []
	 	datos = DataPayrollModel.objects.get(id =request.GET['id'])
	 	dicNomina = ({'apPaterno': datos.apPaterno, 'apMaterno': datos.apMaterno, 'nombre': datos.name, 'rfc': datos.rfc, 'sueldoMensual': datos.monthlySalary, 'calculo': datos.calculation, 'sueldoImss': datos.salaryImss, 'isr': datos.isr, 'imss': datos.imss, 'gratificacion': datos.gratification, 'descuento': datos.discounts, 'infonavit': datos.creditInfonavit, 'fonacot': datos.creditFonacot, 'pension': datos.alimony, 'otros': datos.others, 'sueldoNomina': datos.paySalary, 'sueldoBolsa': datos.bagToDeal, 'efectivo': datos.cash,  'netoAsimilado': datos.assimilated, 'vales': datos.pantryVouchers, 'terceros': datos.thirdParties, 'familiares': datos.family, 'sobrante': datos.surplus, 'netoRecibido': datos.netReceived, 'diasNomina': datos.daysPayroll})
	 	detallesNomina.append(dicNomina)
	 	return JsonResponse({'detail': detallesNomina})



class PayrollReviewView(LoginRequiredMixin,  DetailView):
	template_name = 'templates/payroll/revisada.html'
	model = ClienteModel

	def get_context_data(self, **kwargs):
		context = super(PayrollReviewView, self).get_context_data(**kwargs)
		if not self.request.user:
			raise Http404
		permisos = PermitsModel.objects.filter(user=self.request.user, cliente=self.get_object())
		if len(permisos) == 0:
			raise Http404
		cliente = FileModel.objects.filter(cliente=self.get_object(), status=0)
		nominas = []
		for i in cliente:
			dicNomina = ({'id': i.id, 'creacion': i.createDate})
			nominas.append(dicNomina)
		context['nominas'] = nominas
		return context

	login_url = '/'
	redirect_field_name = 'login'

class PayrollReviewDetailView(LoginRequiredMixin, TemplateView):

	def get(self, request, *args, **kwargs):
		if not request.GET['id']:
			raise Http404
		nomina = DataPayrollModel.objects.filter(identifier= str(request.GET['id']), paySalary__gt = 0)
		listaNomina = []
		for n in nomina:
			dicNomina = ({'rfc': n.rfc, 'apPaterno':n.apPaterno, 'apMaterno': n.apMaterno, 'nombre': n.name, 'isr': n.isr, 'imss': n.imss, 'nominaPagar': n.paySalary})
			listaNomina.append(dicNomina)
		
		# efectivo = DataPayrollModel.objects.filter(identifier= str(request.GET['id']), cash__gt = 0)
		# for e in efectivo:
		# 	dicEfectivo = ({'rfc': e.rfc, 'apPaterno':e.apPaterno, 'apMaterno': e.apMaterno, 'nombre': e.name, 'efectivo': e.cash})
		# 	listaEfectivo.append(dicEfectivo)
		listaEfectivo = []
		asimilados = DataPayrollModel.objects.filter(identifier= str(request.GET['id']), assimilated__gt = 0)
		for a in asimilados:
			dicAsimilado = ({'rfc': a.rfc, 'apPaterno':a.apPaterno, 'apMaterno': a.apMaterno, 'nombre': a.name, 'efectivo': a.assimilated})
			# listaEfectivo.append(dicAsimilado)

		return JsonResponse({'nomina': listaNomina,'efectivo': listaEfectivo})
	login_url = '/'
	redirect_field_name = 'login'