from django.contrib import admin
from .models import Prizes, PrizeCategory, UserRedeemedPrizes

# Register your models here.

@admin.register(Prizes)
class PrizesAdmin(admin.ModelAdmin):
    list_display = ('name', 'generated_by')

@admin.register(PrizeCategory)
class PrizeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(UserRedeemedPrizes)
class UserRedeemedPrizesAdmin(admin.ModelAdmin):
    list_display = ('__str__',)