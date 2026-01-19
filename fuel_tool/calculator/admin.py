from django.contrib import admin
from .models import TruckClass

@admin.register(TruckClass)
class TruckClassAdmin(admin.ModelAdmin):
    """
    Admin interface for managing truck classes.
    Operations staff can add/edit truck definitions here.
    """
    list_display = ('name', 'base_km_per_liter', 'loaded_multiplier', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    
    fieldsets = (
        ('Truck Information', {
            'fields': ('name', 'is_active'),
        }),
        ('Fuel Efficiency', {
            'fields': ('base_km_per_liter', 'loaded_multiplier'),
            'description': (
                'base_km_per_liter: Empty truck efficiency (km/L).<br>'
                'loaded_multiplier: Reduction factor when loaded (0.85 = 15% reduction).'
            ),
        }),
    )