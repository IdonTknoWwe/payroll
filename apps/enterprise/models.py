from __future__ import unicode_literals

from django.db import models

# Create your models here.

class EnterpriseModel(models.Model):
	name = models.CharField(blank=False, max_length=80)
	accountBancomer = models.CharField(blank=True, max_length=20)
	clabeBancomer = models.CharField(blank=True, max_length=20)
	accountSantander = models.CharField(blank=True, max_length=20)
	clabeSantander = models.CharField(blank=True, max_length=20)
	primss = models.DecimalField(max_digits=15, decimal_places=2)
	rfc = models.CharField(blank=False, max_length=13, unique=True)
	legalRepresentative = models.CharField(blank=True, max_length=255)
	recordNumber = models.CharField(blank=True, max_length=255)
	dateConstitution = models.DateField()
	noNotarioActa = models.CharField(blank=True, max_length=255)
	nameNotarioActa = models.CharField(blank=True, max_length=255)
	residenciaActa = models.CharField(blank=True, max_length=255)
	noRppActa = models.CharField(blank=True, max_length=255)
	numeroPoder = models.CharField(blank=True, max_length=255)
	datePower = models.DateField()
	noNotarioPoder = models.CharField(blank=True, max_length=255)
	nameNotarioPoder = models.CharField(blank=True, max_length=255)
	residenciaPoder = models.CharField(blank=True, max_length=255)
	noRppPoder = models.CharField(blank=True, max_length=255)
	isActive = models.BooleanField(default=True) 

	class Meta:
		verbose_name = "Empresa"
		verbose_name_plural = "Empresas"

	def __unicode__(self):
		return '%s' %(self.rfc)