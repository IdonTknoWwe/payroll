from django import forms 
from .models import EmployeeModel
from apps.employee.models import PaymentEmployeeSchemaModel
from betterforms.multiform import MultiForm

class EmployeeForm(forms.ModelForm): 
    class Meta: 
        model = EmployeeModel 
        exclude = ('paymentSchema', ) 

class Employee2Form(forms.ModelForm):
	class Meta:
		model = PaymentEmployeeSchemaModel
		exclude = ('employee',)

class EmployeeMultiForm(MultiForm):
	form_classes = {
		'empleado':EmployeeForm,
		'PaymentEmployee': Employee2Form,
	}