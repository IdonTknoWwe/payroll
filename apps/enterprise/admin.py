from django.contrib import admin

# Register your models here.
from .models import EnterpriseModel
# Register your models here.
@admin.register(EnterpriseModel)
class EnterpriseAdmin(admin.ModelAdmin):
	list_display = ('name', 'rfc','isActive',)