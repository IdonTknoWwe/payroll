from apps.cliente.calculos.deducciones import isr

def asimilados(sueldoDiario):
	mes = float(30)
	sueldoMensual = float(sueldoDiario * mes)
	isrCf = isr.consultaCuotaFija(sueldoMensual)
	cantidadCf = isrCf[0]
	limiteInfCf = isrCf[1]
	porcentajeCf = isrCf[2]
	excedente = (sueldoMensual - limiteInfCf)
	impAntsCF = (excedente * porcentajeCf)
	isrResul = (impAntsCF + cantidadCf)
	isrPercepcion = float((isrResul))
	total = sueldoMensual + isrPercepcion
	return total, isrPercepcion

