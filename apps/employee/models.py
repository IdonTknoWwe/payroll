from __future__ import unicode_literals
from django.db import models
from apps.enterprise.models import EnterpriseModel
from apps.cliente.models import ClienteModel


class PaymentEmployeeSchemaModel(models.Model):
    TYPE_SCHEMAS = (
        (1, 'NOMINA'),
        (2, 'EFECTIVO'),
        (3, 'ASIMILADOS'),
        (4, 'VALES DE DESPENSA'),
        (5, 'TERCEROS'),
        (6, 'FAMILIARES'),
    )

    typePayment = models.SmallIntegerField(choices=TYPE_SCHEMAS)
    enterprise = models.ForeignKey(EnterpriseModel,on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Empleado Empresa'
        verbose_name_plural = 'Empleado Empresas'

    def __unicode__(self):
        return '%s' % (self.enterprise)


class EmployeeModel (models.Model):
    TYPE_SEXO = (
        (0, 'MASCULINO'),
        (1, 'FEMENINO'),
    )

    TYPE_CALCULATION = (
        (0, 'BRUTO'),
        (1, 'NETO'),
        (2, 'INTEGRO'),
    )
    TYPE_PAYROLL = (
        (1, 'DIARIA'),
        (7, 'SEMANAL'),
        (14, 'CATORCENAL'),
        (15, 'QUINCENAL'),
        (30, 'MENSUAL'),
    )
    TYPE_DISTRIBUTE = (
        (1, 'EFECTIVO'),
        (2, 'ASIMILADOS'),
        (3, 'TERCEROS'),
        (4, 'FAMILIARES')
    )

    keyNoi = models.IntegerField()
    apPaterno = models.CharField(blank=False, max_length=80)
    apMaterno = models.CharField(blank=False, max_length=80)
    name = models.CharField(blank=False, max_length=80)
    bankname = models.CharField(blank=True, max_length=255)
    countname = models.IntegerField()
    interbankKey = models.IntegerField()
    dateAntiquity = models.DateField()
    realMonthlySalary = models.DecimalField(max_digits=15, decimal_places=2)
    lastDateImss = models.DateField()
    registeredSalary = models.DecimalField(max_digits=15, decimal_places=2)
    realSalary = models.DecimalField(max_digits=15, decimal_places=2)
    creditInfonavit = models.DecimalField(max_digits=15, decimal_places=2)
    creditFonacot = models.DecimalField(max_digits=15, decimal_places=2)
    gratification = models.DecimalField(max_digits=15, decimal_places=2)
    discounts = models.DecimalField(max_digits=15, decimal_places=2)
    remainder = models.DecimalField(max_digits=15, decimal_places=2)
    alimony = models.DecimalField(max_digits=15, decimal_places=2)
    gender = models.SmallIntegerField(choices=TYPE_SEXO)
    rfc = models.CharField(blank=True, max_length=13, unique=True)
    curp = models.CharField(blank=True, max_length=20)
    domicilie = models.CharField(blank=True, max_length=255)
    workstation = models.CharField(blank=True, max_length=255)
    workday = models.IntegerField()
    timetable = models.CharField(blank=True, max_length=255)
    restday = models.CharField(blank=True, max_length=255)
    calculation = models.SmallIntegerField(choices=TYPE_CALCULATION)
    distribute = models.SmallIntegerField(choices=TYPE_DISTRIBUTE)
    isActive = models.BooleanField(default=True)
    paymentSchema = models.ManyToManyField(PaymentEmployeeSchemaModel)
    scheme = models.ForeignKey('administracion.PaymentSchemeModel', on_delete=models.CASCADE)
    cliente = models.ForeignKey(ClienteModel, on_delete=models.CASCADE)
    payroll = models.SmallIntegerField(choices=TYPE_PAYROLL)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __unicode__(self):
        return '%s' % (self.rfc)


class DataPayrollModel(models.Model):

    apPaterno = models.CharField(blank=False, max_length=80)
    apMaterno = models.CharField(blank=False, max_length=80)
    name = models.CharField(blank=False, max_length=80)
    rfc = models.CharField(blank=False, max_length=15)
    monthlySalary = models.DecimalField(
        blank=False, max_digits=12, decimal_places=2)
    calculation = models.CharField(blank=False, max_length=10)
    salaryImss = models.DecimalField(
        blank=False, max_digits=12, decimal_places=2)
    faults = models.DecimalField(blank=False, max_digits=12, decimal_places=2)
    isr = models.DecimalField(blank=False, max_digits=12, decimal_places=2)
    imss = models.DecimalField(blank=False, max_digits=12, decimal_places=2)
    discounts = models.DecimalField(
        blank=False, max_digits=12, decimal_places=2)
    creditInfonavit = models.DecimalField(
        blank=False, max_digits=12, decimal_places=2)
    creditFonacot = models.DecimalField(
        blank=False, max_digits=12, decimal_places=2)
    alimony = models.DecimalField(blank=False, max_digits=12, decimal_places=2)
    others = models.DecimalField(blank=False, max_digits=12, decimal_places=2)
    savingsAccount = models.DecimalField(
        blank=False, max_digits=12, decimal_places=2)
    medicalExpenses = models.DecimalField(
        blank=False, max_digits=12, decimal_places=2)
    loans = models.DecimalField(blank=False, max_digits=12, decimal_places=2)
    stateTax = models.DecimalField(blank=False, max_digits=5, decimal_places=2)
    socialBurden = models.DecimalField(
        blank=False, max_digits=12, decimal_places=2)
    gratification = models.DecimalField(
        blank=False, max_digits=12, decimal_places=2)
    paySalary = models.DecimalField(
        blank=False, max_digits=12, decimal_places=2)
    bagToDeal = models.DecimalField(
        blank=False, max_digits=12, decimal_places=2)
    cash = models.DecimalField(blank=False, max_digits=12, decimal_places=2)
    assimilated = models.DecimalField(
        blank=False, max_digits=12, decimal_places=2)
    thirdParties = models.DecimalField(
        blank=False, max_digits=12, decimal_places=2)
    pantryVouchers = models.DecimalField(
        blank=False, max_digits=12, decimal_places=2)
    family = models.DecimalField(blank=False, max_digits=12, decimal_places=2)
    surplus = models.DecimalField(blank=False, max_digits=12, decimal_places=2)
    netReceived = models.DecimalField(
        blank=False, max_digits=12, decimal_places=2)
    daysPayroll = models.SmallIntegerField()
    identifier = models.IntegerField()
    statusPayroll = models.SmallIntegerField()
    cliente = models.CharField(blank=False, max_length=15)
    businessRoster = models.CharField(blank=False, max_length=15)
    businessCash = models.CharField(blank=False, max_length=15)
    businessAssimilated = models.CharField(blank=False, max_length=15)
    businessTthirdParties = models.CharField(blank=False, max_length=15)
    businessPantryVouchers = models.CharField(blank=False, max_length=15)
    businessFamily = models.CharField(blank=False, max_length=15)

    class Meta:
        verbose_name = "Nomina Empleado"
        verbose_name_plural = "Nomina Empleados"

    def __unicode__(self):
        return '%s' % (self.rfc)
