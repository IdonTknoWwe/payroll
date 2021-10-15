from django import forms
from .models import ClienteModel, FileModel
from django.core.validators import RegexValidator

class ClientForm(forms.ModelForm):
	
	class Meta:
		model = ClienteModel
		fields = '__all__'
		
class FileForm(forms.ModelForm):
	class Meta:
		model = FileModel
		fields = '__all__'