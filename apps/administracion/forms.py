from django import forms 
from .models import PaymentSchemeModel

class PaymentSchemeForm(forms.ModelForm):
    class Meta:
        model = PaymentSchemeModel
        fields = '__all__'
        