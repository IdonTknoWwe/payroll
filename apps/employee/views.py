from django.shortcuts import render
from django.views.generic import FormView, ListView, TemplateView, UpdateView, View
from braces.views import LoginRequiredMixin
from .models import EmployeeModel, PaymentEmployeeSchemaModel
from apps.cliente.models import ClienteModel
from apps.administracion.models import PaymentSchemeModel
from .forms import EmployeeForm, Employee2Form
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from apps.enterprise.models import EnterpriseModel
from django.db import IntegrityError, transaction
from django.http import Http404
from apps.user.views import PermissionMixin
import json 
import sys
import re
# Create your views here.


class EmployeeCreateView(LoginRequiredMixin, PermissionMixin,  FormView):
	model = EmployeeModel
	form_class = EmployeeForm
	second_form_class = Employee2Form
	template_name = 'templates/employee/create.html'
	success_url = reverse_lazy('Empleados:listarEmpleado')

	def get_context_data(self, **kwargs):
	    context = super(EmployeeCreateView, self).get_context_data(**kwargs)
	    if 'form' not in context:
	    	context['form'] = self.form_class(self.request.GET)
	    if 'form2' not in context:
	    	context['form2'] = self.second_form_class(self.request.GET)	
	    return context


	def post(self, request, *args, **kwargs):
		datos = self.form_class(request.POST)
		listaenterprises = []
		listaresultados = []
		for key, valor in request.POST.iteritems():
			if key.find('enterprise') > -1:
				listaenterprises.append({key : valor})

		for key, valor in request.POST.iteritems():
			if key.find('typePayment') > -1:
				numero = key.split('typePayment')[1]
				for i in listaenterprises:
					if 'enterprise{}'.format(numero) in i:
						diccionario_nuevo = i
						diccionario_nuevo[key] = valor
						listaresultados.append(diccionario_nuevo)

		if datos.is_valid():
			try:
				with transaction.atomic():
					empleado = datos.save()
					for i in listaresultados:
						nuevo_diccionario = {}
						for key, valor in i.iteritems():
							clave = key
							clave = clave.replace('1', '')
							clave = clave.replace('2', '')
							clave = clave.replace('3', '')
							clave = clave.replace('4', '')
							clave = clave.replace('5', '')
							clave = clave.replace('6', '')
							nuevo_diccionario[clave] = valor
						referencia_model = PaymentEmployeeSchemaModel(typePayment = int(nuevo_diccionario['typePayment']), enterprise = EnterpriseModel.objects.get(pk=int(nuevo_diccionario['enterprise'])))
						referencia_model.save()
						empleado.paymentSchema.add(referencia_model)
						empleado.isActive = True
						empleado.save()
			except IntegrityError:
				print ('OCURRIO UN PROBLEMA')
		else:
			print (datos.errors)
		return HttpResponseRedirect(self.get_success_url())

	    

	login_url ='/'
	redirect_field_name = 'login'

class EmployeeListView(LoginRequiredMixin, PermissionMixin,  ListView):
	model = EmployeeModel
	template_name = 'templates/employee/listar.html'
	login_url = '/'
	redirect_field_name = 'login'

class EmployeeEditView(LoginRequiredMixin, PermissionMixin, UpdateView):
	model = EmployeeModel
	second_model = PaymentEmployeeSchemaModel
	template_name = 'templates/employee/editar.html'
	form_class =  EmployeeForm
	second_form_class = Employee2Form
	success_url = reverse_lazy('Empleados:listarEmpleado')

	login_url = '/'
	redirect_field_name = 'login'

	def get_context_data(self, **kwargs):
		context = super(EmployeeEditView, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk', 0)
		empleado = self.model.objects.get(id=pk)
		empresas = self.second_model.objects.filter(employeemodel=empleado)
		if 'form' not in context:
			context['form'] = self.form_class

		formularios_empresas_nomina = []
		for i in empresas:
			formularios_empresas_nomina.append(self.second_form_class(instance=i))
		
		context['form2'] = formularios_empresas_nomina
		return context

	def post(self, request, *args, **kwargs):
		empresas = {}
		tipo_pago = {}
		for key, value in request.POST.iteritems():
			if key.find('enterprise') >-1:
				empresas[key] = int(value)
			if key.find('typePayment') >-1:
				tipo_pago[key] = int(value)
		super(EmployeeEditView, self).post(request, *args, **kwargs)
		self.object.paymentSchema.all().delete()
		for key, value in empresas.iteritems():

			try:
				with transaction.atomic():
					referencia_model = PaymentEmployeeSchemaModel(typePayment = int(tipo_pago['typePayment'+key[-1:]]), enterprise = EnterpriseModel.objects.get(pk=int(value)))
					referencia_model.save()
					self.object.paymentSchema.add(referencia_model)
					self.object.save()	
			except IntegrityError:
				print ('ocurrio un problema en transacciones atomicas')
		return HttpResponseRedirect(self.get_success_url())



	login_url = '/'
	redirect_field_name = 'login'

class EmployeeCreatingView(LoginRequiredMixin, PermissionMixin, TemplateView):
	template_name = 'templates/employee/new.html'

	def post(self, request, *args, **kwargs):
		listaEmpleado = []
		keyNoi = '^([0-9]+)$'
		apPaterno = '^([\D]+)$'
		apMaterno = '^([\D]+)$'
		name = '^([\D]+)$'
		bankName = '^([\D]+)$'
		countName = '^([0-9]+)$'
		interbankKey = '^([0-9]+)$'
		dateAntiquity = '^(((19|20)\d{2})-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01]))$'
		realMonthlySalary = '^(([0-9]+)([.])([0-9]){2})$'
		lastDateImss = '^(((19|20)\d{2})-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01]))$'
		registeredSalary = '^(([0-9]+)([.])([0-9]){2})$'
		realSalary = '^(([0-9]+)([.])([0-9]){2})$'
		creditInfonavit = '^(([0-9]+)([.])([0-9]){2})$'
		creditFonacot = '^(([0-9]+)([.])([0-9]){2})$'
		gratification = '^(([0-9]+)([.])([0-9]){2})$'
		discounts = '^(([0-9]+)([.])([0-9]){2})$'
		remainder = '^(([0-9]+)([.])([0-9]){2})$'
		alimony = '^(([0-9]+)([.])([0-9]){2})$'
		gender = '^[0-1]{1}$'
		rfc = '^(([A-Z]{3,4})(([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1]))([A-Z\d]{3}))$'
		curp = '^([A-Z]{4})(([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1]))([A-Z]{6})([0-9]{2})$'
		domicilie = '^([\D\d]+)$'
		workstation = '^([\D\d]+)$'
		workday = '^([0-7]{1})$'
		timetable = '^([\D\d]+)$'
		restday = '^([\D\d]+)$'
		calculation = '^[0-2]{1}$'
		diasNomina = '^(1|7|10|14|15|30)$'
		vdistribucion = '^(1|2|3|4)$'

		contador = 0
		try:
			mi_json = json.loads(request.POST['xls'])
			empleados = mi_json['Hoja1']
			for i in empleados:
				if re.match(keyNoi, i['NO NOI']) == None:
					contador +=1
				if re.match(apPaterno, i['APELLIDO PATERNO']) == None:
					contador +=1
				if re.match(apMaterno, i['APELLIDO MATERNO']) == None:
					contador +=1
				if re.match(name, i['NOMBRE(S)']) == None:
					contador +=1
				if re.match(bankName, i['BANCO']) == None:
					contador +=1
				if re.match(countName, i['CUENTA BANCARIA'])== None:
					contador +=1
				if re.match(interbankKey, i['CLABE INTERBANCARIA']) == None:
					contador +=1
				if re.match(dateAntiquity, i['FECHA ANTIGUEDAD REAL']) == None:
					contador +=1
				if re.match(realMonthlySalary, i['SUELDO MENSUAL REAL']) == None:
					contador +=1
				if re.match(lastDateImss, i['FECHA ULTIMA ALTA IMSS']) == None:
					contador +=1
				if re.match(registeredSalary, i['SUELDO REGISTRADO IMSS']) == None:
					contador +=1
				if re.match(realSalary, i['SUELDO REAL']) == None:
					contador +=1
				if re.match(creditInfonavit, i['CREDITO INFONAVIT']) == None:
					contador +=1
				if re.match(creditFonacot, i['CREDITO FONACOT']) == None:
					contador +=1
				if re.match(gratification, i['GRATIFICACION']) == None:
					contador +=1
				if re.match(discounts, i['DESCUENTO']) == None:
					contador +=1
				if re.match(remainder, i['REMANENTE']) == None:
					contador +=1
				if re.match(alimony, i['PENSION ALIMENTICIA']) == None:
					contador +=1
				if re.match(gender, i['SEXO']) == None:
					contador +=1
				if re.match(rfc, i['RFC']) == None:
					contador +=1
				if re.match(curp, i['CURP']) == None:
					contador +=1
				if re.match(domicilie, i['DOMICILIO']) == None:
					contador +=1
				if re.match(workstation, i['PUESTO CONTRATADO']) == None:
					contador +=1
				if re.match(workday, i['JORNADA LABORAL']) == None:
					contador +=1
				if re.match(timetable, i['HORARIO']) == None:
					contador +=1
				if re.match(restday, i['DIAS DE DESCANSO']) == None:
					contador +=1
				if re.match(calculation, i['CALCULO']) == None:
					contador +=1
				if re.match(diasNomina, i['DIAS NOMINA']) == None:
					contador +=1
				if re.match(vdistribucion, i['DISTRIBUCION']) == None:
					contador +=1


				esquema = PaymentSchemeModel.objects.get(identifier = i['ESQUEMA PAGO'])
				cliente = ClienteModel.objects.get(rfc = i['RFC CLIENTE'])
				enterpriseNomina = EnterpriseModel.objects.get(rfc = i['EMPRESA NOMINA'])
				enterpriseEfectivo = EnterpriseModel.objects.get(rfc = i['EMPRESA EFECTIVO'])
				enterpriseAsimilados = EnterpriseModel.objects.get(rfc = i['EMPRESA ASIMILADOS'])
				enterpriseVales = EnterpriseModel.objects.get(rfc = i['EMPRESA VALES'])
				enterpriseTerceros = EnterpriseModel.objects.get(rfc = i['EMPRESA TERCEROS'])
				enterpriseFamiliares = EnterpriseModel.objects.get(rfc = i['EMPRESA FAMILIARES'])
				dicEmpleado = ({'keyNoi': i['NO NOI'], 'apPaterno': i['APELLIDO PATERNO'], 'apMaterno': i['APELLIDO MATERNO'], 'name': i['NOMBRE(S)'], 'bankName': i['BANCO'], 'countName': i['CUENTA BANCARIA'], 'interbankKey': i['CLABE INTERBANCARIA'], 'dateAntiquity': i['FECHA ANTIGUEDAD REAL'], 'realMonthlySalary': i['SUELDO MENSUAL REAL'], 'lastDateImss': i['FECHA ULTIMA ALTA IMSS'], 'registeredSalary': i['SUELDO REGISTRADO IMSS'], 'realSalary': i['SUELDO REAL'], 'creditInfonavit': i['CREDITO INFONAVIT'], 'creditFonacot': i['CREDITO FONACOT'], 'gratification': i['GRATIFICACION'], 'discounts': i['DESCUENTO'], 'remainder': i['REMANENTE'], 'alimony': i['PENSION ALIMENTICIA'], 'gender': i['SEXO'], 'rfc': i['RFC'], 'curp': i['CURP'], 'domicilie': i['DOMICILIO'], 'workstation': i['PUESTO CONTRATADO'], 'workday': i['JORNADA LABORAL'], 'timetable': i['HORARIO'], 'restday' : i['DIAS DE DESCANSO'], 'calculation': i['CALCULO'], 'distribute': i['DISTRIBUCION'] , 'scheme': esquema.identifier, 'cliente': cliente.name, 'payroll': i['DIAS NOMINA'], 'rfcNomina': enterpriseNomina.rfc, 'rfcEfectivo': enterpriseEfectivo.rfc, 'rfcAsimilados': enterpriseAsimilados.rfc,'rfcTerceros': enterpriseTerceros.rfc, 'rfcVales': enterpriseVales.rfc,  'rfcFamiliares': enterpriseFamiliares.rfc})
				listaEmpleado.append(dicEmpleado)
			if contador > 0:
				raise Http404
		except:
			raise Http404
		return JsonResponse({'detail': listaEmpleado })

	login_url = '/'
	redirect_field_name = 'login'

class EmployeeSaveView(LoginRequiredMixin, TemplateView):
	success_url = reverse_lazy('Empleados:listarEmpleado')
	def post(self, request, *args, **kwargs):
		try:
			mi_json = json.loads(request.POST['empleado'])
			with transaction.atomic():
				for recorre in mi_json:
					cliente = ClienteModel.objects.get(name = recorre['cliente'])
					esquema = PaymentSchemeModel.objects.get(identifier = recorre['scheme'])
					empleado = EmployeeModel(keyNoi = recorre['keyNoi'], apPaterno = recorre['apPaterno'], apMaterno = recorre['apMaterno'], name =recorre['name'], bankName = recorre['bankName'], countName = recorre['countName'], interbankKey = recorre['interbankKey'], dateAntiquity = recorre['dateAntiquity'], realMonthlySalary = recorre['realMonthlySalary'], lastDateImss = recorre['lastDateImss'], registeredSalary = recorre['registeredSalary'], realSalary =recorre['realSalary'],  creditInfonavit = recorre['creditInfonavit'], creditFonacot = recorre['creditFonacot'], gratification = recorre['gratification'], discounts = recorre['discounts'], remainder = recorre['remainder'], alimony = recorre['alimony'], gender=recorre['gender'], rfc = recorre['rfc'], curp = recorre['curp'], domicilie = recorre['domicilie'], workstation = recorre['workstation'], workday = recorre['workday'], timetable =recorre['timetable'], restday = recorre['restday'], calculation = recorre['calculation'], scheme = esquema, distribute = recorre['distribute'], cliente = cliente,  payroll = recorre['payroll'])
					empleado.save()
					listaEmpresas = [recorre['rfcNomina'],recorre['rfcEfectivo'], recorre['rfcAsimilados'], recorre['rfcTerceros'], recorre['rfcVales'], recorre['rfcFamiliares']]
					contador = 0 
					for i in listaEmpresas:
						contador += 1
						empresa = EnterpriseModel.objects.get(rfc=i)
						idEmpresa = empresa.id
						referencia = PaymentEmployeeSchemaModel(typePayment= contador, enterprise_id = idEmpresa)
						referencia.save()
						empleado.paymentSchema.add(referencia)
						empleado.save()
		except IntegrityError:
			raise Http404
		return JsonResponse({'detail':0})
		success_url = reverse_lazy('Empleados:listarEmpleado')
	login_url = '/'
	redirect_field_name = 'login'