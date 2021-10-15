from apps.administracion.models import SubsidoModel

def consultaSubsidio(sueldo):
	tsubsidio = SubsidoModel.objects.all()
	subsidio = 0 
	for recorre in tsubsidio:
		if  sueldo > float(recorre.minimum) and sueldo < float(recorre.maximum) and float(recorre.quantity) > 0:
			subsidio = float((recorre.quantity)*-1) 
			break
		elif float(recorre.quantity) == 0:
			subsidio = float((recorre.quantity)*-1)
		else:
			pass
	return subsidio
