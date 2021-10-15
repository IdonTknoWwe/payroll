from django.contrib import admin
from .models import ClienteModel, FileModel, PayeeIdModel, PermitsModel
# Register your models here.


# class PermitsTabularInline(admin.TabularInline):
# 	model = PermitsModel
# 	extra = 2
		
# @admin.register(PermitsModel)
# class PermitsAdmin(admin.ModelAdmin):
# 	list_display = ('UserModel','cliente',)

# 	def cliente(self, obj):
# 		print obj, 'obj'
# 		return obj.cliente.all()[0].cliente.rfcClient

@admin.register(ClienteModel)
class ClientAdmin(admin.ModelAdmin):
	list_display = ('name', 'rfcClient','isActive',)

@admin.register(FileModel)
class FileAdmin(admin.ModelAdmin):
	list_display = ('createDate','cliente', 'status', 'startPayroll', 'endPayroll','datePayroll','archivo',)

@admin.register(PayeeIdModel)
class PayeeIdAdmin(admin.ModelAdmin):
	list_display = ('createDate','status','cliente',)

@admin.register(PermitsModel)
class PermitsAdmin(admin.ModelAdmin):
	list_display = ('user',)

# @admin.register(ClientPermitsModel)
# class ClientPermitsAdmin(admin.ModelAdmin):
# 	list_display = ('cliente','permitsType',)