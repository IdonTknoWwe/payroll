from django.contrib import admin
from .models import EmployeeModel, PaymentEmployeeSchemaModel, DataPayrollModel

# Register your models here.

class PaymentEmployeeSchemaTabularInline(admin.TabularInline):
	model = PaymentEmployeeSchemaModel
	extra = 2
		
@admin.register(PaymentEmployeeSchemaModel)
class PaymentEmployeeSchemaAdmin(admin.ModelAdmin):
	list_display = ('typePayment','enterprise', 'empleado')

	def empleado(self, obj):
		return obj.employeemodel_set.all()[0]


@admin.register(EmployeeModel)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('apPaterno','apMaterno', 'name','rfc','cliente', 'calculation','payroll', 'isActive',)
	# inlines = (PaymentEmployeeSchemaTabularInline, )

@admin.register(DataPayrollModel)
class DataPayrollAdmin(admin.ModelAdmin):
	list_display = ('rfc','cliente',)