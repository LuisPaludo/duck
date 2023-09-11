from django.contrib import admin
from .models import TouristAttraction, Location
# Register your models here.

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(TouristAttraction)
class TuristicPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','points')
    list_filter = [
        "location"
    ]
