from apps.cliente.calculos.deducciones import isr, subsidio, imss, inversoAsimilados, calculosAsimilados, brutoAsimilado, socialCarga
from apps.employee.models import EmployeeModel, PaymentEmployeeSchemaModel
from apps.administracion.models import PaymentSchemeModel
from apps.cliente.models import ClienteModel
from apps.enterprise.models import EnterpriseModel
def calculaNomina(rfc, otrasGratificacion, otrosDescuentos, faltas):

	lista = []
	mes = float(30.0)
	# Consulta al empleado por el rfc y sus datos del empleado 
	empleado = EmployeeModel.objects.get(rfc = rfc)

	# Dias Nomina
	diasPercepcion = float(empleado.payroll)

	gratificacion = float(empleado.gratification)
	descuento = float(empleado.discounts)

	# Faltas
	faltas = float(faltas)
	# Descuentos Extra Ordinarios
	cajaAhorro = float(0.0)
	prestamos = float(0.0)
	gastosMedicos = float(0.0)
	otros = float(0.0)
	infonavit = float(empleado.creditInfonavit)
	fonacot = float(empleado.creditFonacot)
	pension = float(empleado.alimony)

	cliente = ClienteModel.objects.get(rfc=empleado.cliente)
	primaRiesgo = float(cliente.primssAgreed)
	
	comisionEstatal = float(0.0)
	bolsaRepartir = float(0.0)
	efectivoPagar = float(0.0)
	asimiladosPagar = float(0.0)
	tercerosPagar = float(0.0)
	valesPagar = float(0.0)
	familiaresPagar  = float(0.0)
	sobrante = float(0.0)

	
	sueldoMensualImss = (float(empleado.registeredSalary) * mes) 
	sueldoDiarioRegistrado = float(empleado.registeredSalary)
	totalCargaSocial = float(0.0)
	# carga = socialCarga.cargaSocial(sueldoDiarioRegistrado, primaRiesgo)
	textoideal = ''
	if empleado.calculation == 0:
		

		textoideal = 'BRUTO'
		
		sueldoImssActual = sueldoDiarioRegistrado * (diasPercepcion - faltas )
		comisionEstatal = sueldoImssActual * (float(3.0) / float(100))

		# Calculo Isr Mensual
		calculoIsr = isr.consultaCuotaFija(sueldoMensualImss)

		# Valores del Isr 
		limiteInferiorCuotaFija = calculoIsr[0]
		porcentajeCuotaFija = calculoIsr[1]
		cuotaFija = calculoIsr[2]

		# Calculos para obtener la cantidad del isrMensual
		excedente = (sueldoMensualImss - limiteInferiorCuotaFija)
		impuestoAntesCuotaFija = (excedente * porcentajeCuotaFija)
		isrMensual = (impuestoAntesCuotaFija + cuotaFija)
		# Calculo Subsidio Mensual
		subsidioMensual = subsidio.consultaSubsidio(sueldoMensualImss)

		# Suma del IsrMensual y SubsidioMensual
		netoIsrMensual = (isrMensual + subsidioMensual)
	
		# Calculo Imss Mensual 
		imssMensual = imss.calculoImss(sueldoDiarioRegistrado, primaRiesgo)

		# Deducciones por la nomina
		isrPercepcion = ((netoIsrMensual / mes) * diasPercepcion)
		imssPercepcion= ((imssMensual / mes) * diasPercepcion)
		descuentoPercepcion = ((descuento / mes) * diasPercepcion)
		infonavitPercepcion = ((infonavit / mes) * diasPercepcion)
		fonacotPercepcion = ((fonacot / mes) * diasPercepcion)
		pensionPercepcion = ((pension / mes) * diasPercepcion)
		gratificacionPercepcion = ((gratificacion / mes) * diasPercepcion)
		

		sueldoNomina = ((sueldoImssActual - imssPercepcion) - isrPercepcion)
	
		sueldoNominaPagar = (sueldoNomina - (descuentoPercepcion + infonavitPercepcion + fonacotPercepcion + pensionPercepcion + cajaAhorro + prestamos + gastosMedicos + otros))
		nominaPagar = sueldoNominaPagar 

		netoRecibido = (sueldoNominaPagar + gratificacionPercepcion)
	
		lista = ([textoideal, sueldoImssActual, faltas, isrPercepcion, imssPercepcion, descuentoPercepcion, infonavitPercepcion, fonacotPercepcion, pensionPercepcion, otros, cajaAhorro, gastosMedicos, prestamos, comisionEstatal, totalCargaSocial, gratificacionPercepcion, nominaPagar, bolsaRepartir, efectivoPagar, asimiladosPagar, tercerosPagar, valesPagar, familiaresPagar, sobrante, netoRecibido])

	else:
		textoideal = 'NETO'

		totalFaltas  = faltas * sueldoDiarioRegistrado

		sueldoImssActual = sueldoDiarioRegistrado * diasPercepcion
		comisionEstatal = sueldoImssActual * (float(3.0) / float(100))
		
		# Calculo Isr Mensual
		calculoIsr = isr.consultaCuotaFija(sueldoMensualImss)

		# Valores del Isr 
		limiteInferiorCuotaFija = calculoIsr[0]
		porcentajeCuotaFija = calculoIsr[1]
		cuotaFija = calculoIsr[2]

		# Calculos para obtener la cantidad del isrMensual
		excedente = (sueldoMensualImss - limiteInferiorCuotaFija)
		impuestoAntesCuotaFija = (excedente * porcentajeCuotaFija)
		isrMensual = (impuestoAntesCuotaFija + cuotaFija)

		# Calculo Subsidio Mensual
		subsidioMensual = subsidio.consultaSubsidio(sueldoMensualImss)

		# Suma del IsrMensual y SubsidioMensual
		netoIsrMensual = (isrMensual + subsidioMensual)
		
		# Calculo Imss Mensual 
		imssMensual = imss.calculoImss(sueldoDiarioRegistrado, primaRiesgo)

		# Deducciones por la nomina
		isrPercepcion = ((netoIsrMensual / mes) * diasPercepcion)
		imssPercepcion= ((imssMensual / mes) * diasPercepcion)
		descuentoPercepcion = ((descuento / mes) * diasPercepcion)
		infonavitPercepcion = ((infonavit / mes) * diasPercepcion)
		fonacotPercepcion = ((fonacot / mes) * diasPercepcion)
		pensionPercepcion = ((pension / mes) * diasPercepcion)
		gratificacionPercepcion = ((gratificacion / mes) * diasPercepcion)


		sueldoNomina = (((sueldoDiarioRegistrado * diasPercepcion) - imssPercepcion) - (isrPercepcion))
		sueldoNominaPagar = (sueldoNomina - (infonavitPercepcion + fonacotPercepcion + pensionPercepcion))

		nominaPagar = sueldoNominaPagar 

		sueldoNeto = (float(empleado.realSalary) * diasPercepcion )
		diferencia = 0
		if sueldoNeto > sueldoNomina:
			diferencia = ((sueldoNeto - sueldoNomina) - totalFaltas) 

		bolsaRepartir = diferencia
		if empleado.distribute == 1:
			efectivoPagar = bolsaRepartir
		elif empleado.distribute == 2:
			asimiladosPagar = bolsaRepartir
		elif empleado.distribute == 3:
			tercerosPagar = bolsaRepartir
		else:
			familiaresPagar = bolsaRepartir

		netoRecibido = sueldoNominaPagar + efectivoPagar + asimiladosPagar + tercerosPagar +familiaresPagar
		netoRecibido = (sueldoNominaPagar + (gratificacionPercepcion + bolsaRepartir))

		lista = ([textoideal, sueldoImssActual, faltas, isrPercepcion, imssPercepcion, descuentoPercepcion, infonavitPercepcion, fonacotPercepcion, pensionPercepcion, otros, cajaAhorro, gastosMedicos, prestamos, comisionEstatal, totalCargaSocial, gratificacionPercepcion, nominaPagar, bolsaRepartir, efectivoPagar, asimiladosPagar, tercerosPagar, valesPagar, familiaresPagar, sobrante, netoRecibido])
	return lista