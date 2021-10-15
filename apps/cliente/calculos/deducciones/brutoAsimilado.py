from apps.cliente.calculos.deducciones import isr

def consultaIsr(sueldoBuscado):
	sueldoMensual  = sueldoBuscado
	buscaIsr = isr.consultaCuotaFija(sueldoMensual)
	limiteInferiorCuotaFija = buscaIsr[0]
	porcentajeCuotaFija = buscaIsr[1]
	cuotaFija = buscaIsr[2]
	excedente = (sueldoMensual - limiteInferiorCuotaFija)
	impuestoAntesCuotaFija = (excedente * porcentajeCuotaFija)
	isrDeterminado = (impuestoAntesCuotaFija + cuotaFija)
	subtotal = (sueldoMensual - isrDeterminado)
	return sueldoMensual, subtotal

def calculoInverso(sueldoNeto):
	sueldoNeto  = float(sueldoNeto)	
	sueldoBuscado = float(0.00)
	diferencia1 = float(0.00)
	diferencia2 = float(0.00)

	encuentraCalculoInverso = False
	while encuentraCalculoInverso == False:
		millares = False
		while millares == False:
			sueldoBuscado = sueldoBuscado + float(1000.00)
			consulta  = consultaIsr(sueldoBuscado)
			diferencia1 = sueldoNeto - consulta[1]
			diferencia2 = consulta[1] - sueldoNeto

			if diferencia1 < float(0.01) and diferencia2 < float(0.01):
				millares = True
			else:
				if consulta[1] > sueldoNeto:
					sueldoBuscado = sueldoBuscado - float(1000.00)
					millares=True

		centenas = False
		while centenas == False:
			sueldoBuscado += float(100.00)
			consulta = consultaIsr(sueldoBuscado)
			diferencia1 = sueldoNeto - consulta[1]
			diferencia2 = consulta[1] - sueldoNeto

			if diferencia1 < float(0.01) and diferencia2 < float(0.01):
				centenas = True
			else:
				if consulta[1] > sueldoNeto:
					sueldoBuscado -= float(100.00)
					centenas=True

		decenas = False
		while decenas == False:
			sueldoBuscado += float(10.00)
			consulta = consultaIsr(sueldoBuscado)
			diferencia1 = sueldoNeto - consulta[1]
			diferencia2 = consulta[1] - sueldoNeto

			if diferencia1 < float(0.01) and diferencia2 < float(0.01):
				decenas = True
			else:
				if consulta[1] > sueldoNeto:
					sueldoBuscado -= float(10.00)
					decenas = True

		unidades = False
		while unidades == False:
			sueldoBuscado += float(1.00)
			consulta = consultaIsr(sueldoBuscado)
			diferencia1 = sueldoNeto - consulta[1]
			diferencia2 = consulta[1] - sueldoNeto

			if diferencia1 < float(0.01) and diferencia2 < float(0.01):
				unidades = True
			else:
				if consulta[1] > sueldoNeto:
					sueldoBuscado -= float(1.00)
					unidades = True

		decimalDecenas = False
		while decimalDecenas == False:
			sueldoBuscado += float(0.1)					
			consulta = consultaIsr(sueldoBuscado)
			diferencia1 = sueldoNeto - consulta[1]
			diferencia2 = consulta[1] - sueldoNeto

			if diferencia1 < float(0.01) and diferencia2 < float(0.01):
				decimalDecenas = True
			else:
				if consulta[1] > sueldoNeto:
					sueldoBuscado -= float(0.1)
					decimalDecenas=True	

		decimalUnidades = False
		while decimalUnidades == False:
			sueldoBuscado += float(0.01)					
			consulta = consultaIsr(sueldoBuscado)
			diferencia1 = sueldoNeto - consulta[1]
			diferencia2 = consulta[1] - sueldoNeto

			if diferencia1 < float(0.01) and diferencia2 < float(0.01):
				decimalUnidades = True
			else:
				if consulta[1] > sueldoNeto:
					sueldoBuscado -= float(0.01)
					decimalUnidades=True	


		encuentraCalculoInverso = True
	print (consulta[0], 'esto', consulta[1])
	return sueldoBuscado


