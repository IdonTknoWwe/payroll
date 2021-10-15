from apps.cliente.calculos.deducciones import isr

def consultaInverso(cantidad):
	mes = float(30)
	sueldoMensual = float(cantidad * mes)
	isrCf = isr.consultaCuotaFija(sueldoMensual)
	cantidadCf = isrCf[0]
	limiteInfCf = isrCf[1]
	porcentajeCf = isrCf[2]
	excedente = (sueldoMensual - limiteInfCf)
	impAntsCF = (excedente * porcentajeCf)
	isrResul = (impAntsCF + cantidadCf)
	return sueldoMensual

def calculaAsimilados(sueldo):
	sueldoDeseado = float(sueldo)
	sueldoCalculado = float(0.00)
	diferencia1 = float(0.00)
	diferencia2 = float(0.00)
	encuentraCalculoInverso = False
	while encuentraCalculoInverso == False:

		millares = False
		while millares == False:
			sueldoCalculado = sueldoCalculado + float(1000.00)
			calculo1 = float(consultaInverso(sueldoCalculado))
			diferencia1 = sueldoDeseado - calculo1
			diferencia2 = calculo1 - sueldoDeseado

			if diferencia1 < float(0.01) and diferencia2 < float(0.01):
				millares = True
			else:
				if calculo1 > sueldoDeseado:
					sueldoCalculado = sueldoCalculado - float(1000.00)
					millares=True

		centenas = False
		while centenas == False:
			sueldoCalculado += float(100.00)
			calculo1 = float(consultaInverso(sueldoCalculado))
			diferencia1 = sueldoDeseado - calculo1
			diferencia2 = calculo1 - sueldoDeseado

			if diferencia1 < float(0.01) and diferencia2 < float(0.01):
				centenas = True
			else:
				if calculo1 > sueldoDeseado:
					sueldoCalculado -= float(100.00)
					centenas=True

		decenas = False
		while decenas == False:
			sueldoCalculado += float(10.00)
			calculo1 = float(consultaInverso(sueldoCalculado))
			diferencia1 = sueldoDeseado - calculo1
			diferencia2 = calculo1 - sueldoDeseado

			if diferencia1 < float(0.01) and diferencia2 < float(0.01):
				decenas = True
			else:
				if calculo1 > sueldoDeseado:
					sueldoCalculado -= float(10.00)
					decenas = True

		unidades = False
		while unidades == False:
			sueldoCalculado += float(1.00)
			calculo1 = float(consultaInverso(sueldoCalculado))
			diferencia1 = sueldoDeseado - calculo1
			diferencia2 = calculo1 - sueldoDeseado

			if diferencia1 < float(0.01) and diferencia2 < float(0.01):
				unidades = True
			else:
				if calculo1 > sueldoDeseado:
					sueldoCalculado -= float(1.00)
					unidades=True

		decimalDecenas = False
		while decimalDecenas == False:
			sueldoCalculado += float(0.1)					
			calculo1 = float(consultaInverso(sueldoCalculado))
			diferencia1 = sueldoDeseado - calculo1
			diferencia2 = calculo1 - sueldoDeseado

			if diferencia1 < float(0.01) and diferencia2 < float(0.01):
				decimalDecenas = True
			else:
				if calculo1 > sueldoDeseado:
					sueldoCalculado -= float(0.1)
					decimalDecenas=True

		decimalUnidades = False
		while decimalUnidades == False:
			sueldoCalculado += float(0.01)					
			calculo1 = float(consultaInverso(sueldoCalculado))
			diferencia1 = sueldoDeseado - calculo1
			diferencia2 = calculo1 - sueldoDeseado

			if diferencia1 < float(0.01) and diferencia2 < float(0.01):
				decimalUnidades = True
			else:
				if calculo1 > sueldoDeseado:
					sueldoCalculado -= float(0.01)
					decimalUnidades = True

		decimal3 = False		
		while decimal3 == False:
				sueldoCalculado += float(0.001)					
				calculo1 = float(consultaInverso(sueldoCalculado))
				diferencia1 = sueldoDeseado - calculo1
				diferencia2 = calculo1 - sueldoDeseado

				if diferencia1 < float(0.01) and diferencia2 < float(0.01):
					decimal3 = True
				else:
					if calculo1 > sueldoDeseado:
						sueldoCalculado -= float(0.001)
						decimal3 = True

		decimal4 = False
		while decimal4 == False:
			sueldoCalculado += float(0.0001)					
			calculo1 = float(consultaInverso(sueldoCalculado))
			diferencia1 = sueldoDeseado - calculo1
			diferencia2 = calculo1 - sueldoDeseado

			if diferencia1 < float(0.01) and diferencia2 < float(0.01):
				decimal4 = True
			else:
				if calculo1 > sueldoDeseado:
					sueldoCalculado -= float(0.0001)
					decimal4 = True

		encuentraCalculoInverso = True
		return sueldoCalculado
