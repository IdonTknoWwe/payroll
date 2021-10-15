from django import forms  
from .models import EnterpriseModel 
 
class EnterpriseForm(forms.ModelForm): 
    class Meta: 
        model = EnterpriseModel 
        fields = '__all__' 