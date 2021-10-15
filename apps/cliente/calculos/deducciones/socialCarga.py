from apps.administracion.models import  SocialBurdenModel

def cargaSocial(sueldoDiarioRegistrado, primaRiesgo):
	sueldoDiarioRegistrado = 104.52
	cargaSocial = SocialBurdenModel.objects.all()
	contadorClienteMensual = 0
	contadorEmpleadoMensual = 0
	contadorClienteBimestral = 0
	contadorEmpleadoBimestral = 0
	contadorClienteEmpleado = 0 
	divisor = float(100.00)
	valorCliente = float(219.12)
	valorEmpleado = float(73.04) 
	for i in cargaSocial:
		dias = float(i.days)
		porcentajeCliente = float(i.percentageClient) / divisor
		porcentajeEmpleado = float(i.percentageEmployee) / divisor

		if i.identifier == 2: 
			contadorClienteMensual += ((valorCliente * dias) * porcentajeCliente)
			contadorEmpleadoMensual += ((valorEmpleado * dias) * porcentajeEmpleado)

		elif i.identifier == 3:
			contadorClienteMensual += (((sueldoDiarioRegistrado - valorCliente) * dias) * porcentajeCliente)
			contadorEmpleadoMensual += (((sueldoDiarioRegistrado - valorCliente) * dias) * porcentajeEmpleado)

		elif i.identifier == 6 or i.identifier == 7 or i.identifier == 10:
			contadorClienteBimestral += ((sueldoDiarioRegistrado * dias) * porcentajeCliente)

		elif i.identifier == 9:
			contadorClienteMensual += ((sueldoDiarioRegistrado * dias) * (primaRiesgo / divisor))
			contadorEmpleadoMensual += ((sueldoDiarioRegistrado * dias) * porcentajeEmpleado)

		else:
			contadorClienteMensual += ((sueldoDiarioRegistrado * dias) * porcentajeCliente)
			contadorEmpleadoMensual += ((sueldoDiarioRegistrado * dias) * porcentajeEmpleado)
	
	contadorClienteEmpleado = (contadorClienteMensual + contadorEmpleadoMensual)
	return contadorClienteMensual, contadorEmpleadoMensual, contadorClienteBimestral, contadorClienteEmpleado