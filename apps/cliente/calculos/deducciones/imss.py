def calculoImss(sueldoDiarioRegistrado, primaRiesgo):
	mes = float(30)
	vacaciones = float(6)
	fs = float(vacaciones / 365)
	primaVacacional = float(0.25)
	vac_pri = (fs * primaVacacional)			
	aguinaldo = float(0.04109589)
	factorIntegracion = float(vac_pri + aguinaldo + 1)
	sbc = (sueldoDiarioRegistrado * factorIntegracion)
	salarioMinimoDf = float(75.49)#80.04
	prima_riesgo = float(1.07184 / 100) # se debe obtener de la empresa
	uma = float(salarioMinimoDf * 3)
	porEspecie = float(0.4 / 100)
	porPrestacion = float(0.250 / 100)
	porPension = float(0.375 / 100)
	porInvalidez = float(0.625 / 100)
	porVejez = float(1.125 / 100)
	especieExcedente = 0
	if sbc > uma:
		especieExcedente = (((sbc - (uma)) * 15) * porEspecie)
	else:
		especieExcedente = 0 
	prestacion = ((sbc * mes) * porPrestacion)
	pension = ((sbc * mes) * porPension)
	invalidez = ((sbc * mes) * porInvalidez)
	vejez = ((sbc * mes)* porVejez)
	imss = float(especieExcedente + prestacion + pension + invalidez + vejez)
	return imss
