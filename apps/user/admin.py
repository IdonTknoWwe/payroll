from django.contrib import admin

from apps.user.models import UserModel, PermissionUser

# Register your models here.
@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
	list_display = ('username','email', 'is_active', 'is_staff', 'password')

@admin.register(PermissionUser)
class PermissionUser(admin.ModelAdmin):
	list_display = ('permission','description',)