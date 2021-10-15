from apps.administracion.models import IsrModel

def consultaCuotaFija(sueldoMensualImss):
	cuotafija = IsrModel.objects.all()
	limiteInferior, porcentaje, cuotaFija = 0,0,0
	for recorre in cuotafija:
		if sueldoMensualImss >= recorre.lowerLimit and sueldoMensualImss <= recorre.upperLimit:
			cuotaFija = float(recorre.fixedFee)
			limiteInferior = float(recorre.lowerLimit)
			porcentaje = float(recorre.percentage/100)
			break
		elif recorre.upperLimit == 0:
			cuotaFija = float(recorre.fixedFee)
			limiteInferior = float(recorre.lowerLimit)
			porcentaje = float(recorre.percentage/100)
		else:
			pass
	return limiteInferior, porcentaje, cuotaFija