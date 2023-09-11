from django.contrib import admin
from .models import History, CustomUser

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date')
    list_filter = [
        "user"
    ]
    search_fields = ('user__username',)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','is_partner')
    list_filter = [
        "is_partner"
    ]
    search_fields = ('username',)
