from __future__ import unicode_literals
from apps.enterprise.models import EnterpriseModel
from apps.user.models import UserModel
from django.db import models

# Create your models here.

class ClienteModel(models.Model):
	CLIENT_STATUS = (
		(1, 'ALTA'),
		(2, 'MEDIA'),
		(3, 'BAJA'),
		)
	name = models.CharField(blank=False, max_length=80) 
	commission = models.DecimalField(blank=False, max_digits=9, decimal_places=2) 
	statusClient = models.SmallIntegerField(choices=CLIENT_STATUS) 
	rfcClient = models.CharField(blank=False, max_length=13, unique=True)
	primssAgreed = models.DecimalField(max_digits=15, decimal_places=2) 
	domicilie = models.CharField(blank=True, max_length=80) 
	legalRepresentative = models.CharField(blank=True, max_length=80) 
	numeroActa = models.CharField(blank=True, max_length=80) 
	dateConstitution = models.DateField() 
	noNotario = models.CharField(blank=True, max_length=80) 
	nameNotario = models.CharField(blank=True, max_length=80) 
	residenciaActa = models.CharField(blank=True, max_length=80) 
	noRppActa = models.CharField(blank=True, max_length=80) 
	numeroPoder = models.CharField(blank=True, max_length=80) 
	datePower = models.DateField() 
	noNotarioPoder = models.CharField(blank=True, max_length=80) 
	nameNotarioPoder = models.CharField(blank=True, max_length=80) 
	residenciaPoder = models.CharField(blank=True, max_length=80) 
	noRppPoder = models.CharField(blank=True, max_length=80)
	isActive = models.BooleanField(default=True) 


	class Meta:
		verbose_name = "Cliente"
		verbose_name_plural = "Clientes"
	
	def __unicode__(self):
		return '%s' %(self.rfc)


class FileModel(models.Model):
	STATUS_NOMINA = (
		(0, 'REVISADA'),
		(1, 'DISPERSADA'),
		(2, 'PAGADA'),
		) 
	
	archivo = models.FileField(upload_to='archivos/')
	createDate = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(choices=STATUS_NOMINA)
	cliente = models.CharField(blank=False, max_length=13)
	startPayroll = models.DateField() 
	endPayroll = models.DateField()
	datePayroll = models.DateField()

	class Meta:
		verbose_name = 'Archivo'
		verbose_name_plural ='Archivos'

	def __unicode__(self):
		return '%s' %(self.id)

class PayeeIdModel(models.Model):

	STATUS_NOMINA = (
		(0, 'REVISADA'),
		(1, 'DISPERSADA'),
		(2, 'PAGADA'),
		) 

	createDate = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(choices=STATUS_NOMINA)
	cliente = models.CharField(blank=False, max_length=13)
	# startPayroll = models.DateField() 
	# endPayroll = models.DateField()
	# datePayroll = models.DateField()

	# creationDate = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Nomina Cliente"
		verbose_name_plural = "Nomina Clientes"

	def __unicode__(self):
		return '%s'%(self.cliente);
  
# class ClientPermitsModel(models.Model):

# 	TYPE_PERMITS = (
# 		(0, 'administrador'),
# 		(1, 'master'),
# 		(2, 'ejecutivo'),
# 		(3, 'tesoreria'),
# 		(4, 'facturacion'),
# 		(5, 'cliente'),
# 		)

# 	cliente = models.ForeignKey(ClienteModel)
# 	permitsType = models.IntegerField(choices=TYPE_PERMITS)

# 	class Meta:
# 		verbose_name = "Permiso Cliente"
# 		verbose_name_plural = "Permiso Clientes"

# 	def __unicode__(self):
# 		return "{} - {}".format(self.cliente, self.TYPE_PERMITS[self.permitsType][1])

class PermitsModel(models.Model):

	TYPE_PERMITS = (
	(0, 'administrador'),
	(1, 'master'),
	(2, 'ejecutivo'),
	(3, 'tesoreria'),
	(4, 'facturacion'),
	(5, 'cliente'))
	
	
	cliente = models.ManyToManyField(ClienteModel)
	permiso = models.SmallIntegerField(choices=TYPE_PERMITS)
	user = models.ForeignKey(UserModel, on_delete = models.CASCADE )
	class Meta:
		verbose_name = "Permiso"
		verbose_name_plural = "Permisos"

	def __unicode__(self):
		return '%s'%(self.user)



    