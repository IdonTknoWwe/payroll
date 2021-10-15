from django.contrib import admin
from .models import PaymentSchemeModel, IsrModel, SubsidoModel, SocialBurdenModel
# Register your models here.


@admin.register(PaymentSchemeModel)
class PaymentAdmin(admin.ModelAdmin):
	list_display = ('playSheet', 'cash', 'assimilated', 'pantryVouchers', 'thirds', 'family', 
	'quantity','percent', 'action','identifier',)

@admin.register(IsrModel)
class IsrAdmin(admin.ModelAdmin):
	list_display = ('lowerLimit','upperLimit','fixedFee','percentage',)

@admin.register(SubsidoModel)
class SubsidioAdmin(admin.ModelAdmin):
	list_display = ('minimum','maximum','quantity',)


@admin.register(SocialBurdenModel)
class SocialBurdenAdmin(admin.ModelAdmin):
	list_display = ('identifier', 'bouquet', 'percentageEmployee', 'percentageClient', 'days')