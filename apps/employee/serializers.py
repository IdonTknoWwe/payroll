from .models import *
from rest_framework import serializers



class PaymentEmployeeSchemaSerializer (serializers.ModelSerializer):
    class Meta:
        model = PaymentEmployeeSchemaModel
        fields =  '__all__'


class EmployeeSerializer (serializers.ModelSerializer):
    class Meta:
        model = EmployeeModel
        fields = '__all__'


class DataPayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPayrollModel
        fields = '__all__'