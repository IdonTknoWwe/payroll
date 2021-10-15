#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms  
from .models import UserModel 
 
class UserModelForm(forms.ModelForm): 

	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta: 
		model = UserModel 
		fields = ('email', 'username', 'first_name', 'last_name',)

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('Las contraseñas no coinciden')
			return password2

	def save(self, commit=True):
		user = super(UserModelForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user