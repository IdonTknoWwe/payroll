from  __future__ import unicode_literals
from django.db import models
from apps.employee.models import EmployeeModel 
from django.db import models

class PaymentSchemeModel(models.Model):
    TYPE_ACTION=(
        (0,'CANTIDAD'),
        (1,'PORCENTAJE'),
    )
    playSheet = models.IntegerField()
    cash = models.DecimalField(blank=False, max_digits=9, decimal_places=2)
    assimilated = models.DecimalField(blank=False, max_digits=9, decimal_places=2)
    pantryVouchers= models.DecimalField(blank=False, max_digits=9, decimal_places=2)
    thirds = models.DecimalField(blank=False, max_digits=9, decimal_places=2)
    family = models.DecimalField(blank=False, max_digits=9, decimal_places=2)
    quantity = models.DecimalField(blank=False, max_digits=9, decimal_places=2)
    percent = models.IntegerField()
    action = models.SmallIntegerField(choices=TYPE_ACTION)
    identifier = models.CharField(blank=False, max_length=10, unique=True)


    class Meta:
        verbose_name = 'Esquema'
        verbose_name_plural = 'Esquemas' 

    def __unicode__(self):
        return '%s' %(self.identifier)


class IsrModel (models.Model):
    lowerLimit = models.DecimalField(max_digits=9, decimal_places=2)
    upperLimit = models.DecimalField(max_digits=12, decimal_places=2)
    fixedFee = models.DecimalField(max_digits=9, decimal_places=2)
    percentage = models.DecimalField(max_digits=9, decimal_places=2)

    
    class Meta:
        verbose_name = 'Isr'
        verbose_name_plural = 'Isrs'
    
    def __unicode__(self):
        return '%s' %(self.lowerLimit)


class SubsidoModel(models.Model):
    minimum =  models.DecimalField(max_digits=9, decimal_places=2)
    maximum = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.DecimalField(max_digits=9, decimal_places=2)


    class Meta:
        verbose_name =  'Subsidio'
        verbose_name_plural =  'Subsidios'

    def __unicode__(self):
        return '%s' %(self.minimum)


class SocialBurdenModel(models.Model):
    TYPE_BOUQUET = (
        (1,'ENFERMEDADES Y MATERNIDAD'),
        (2, 'INVALIDEZY VIDA'),
        (3, 'RETIRO'),
        (4, 'CESANTIA EN EDAD AVANZADA Y VEJEZ'),
        (5, 'GUARDERIA Y PRESTACIONES SOCIALES'),
        (6, 'RIESGO DE TRABAJO'),
        (7, 'APORTACION AL INFONAVIT')
    )

    bouquet = models.SmallIntegerField(choices=TYPE_BOUQUET)
    percentageEmployee = models.DecimalField(blank=False, max_digits=5, decimal_places=2)
    percentageClient = models.DecimalField(blank=False, max_digits=5, decimal_places=2)
    days =  models.DecimalField(blank=False, max_digits=5, decimal_places=2)
    identifier = models.SmallIntegerField(unique=True)


    class Meta:
        verbose_name= 'Carga Social'
        verbose_name_plural = 'Cargas Sociales'

    def __unicode__(self):
        return '%s' %(self.identifier)
