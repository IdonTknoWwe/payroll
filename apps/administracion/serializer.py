from .models import *
from rest_framework import serializers



class PaymentSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSchemeModel
        fields = '__all__'