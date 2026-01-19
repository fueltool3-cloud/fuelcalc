from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TruckClass(models.Model):
    """
    Represents a truck class with its fuel consumption characteristics.
    
    Attributes:
        name: Truck class identifier (e.g., "Small Van", "3-Axle Truck")
        base_km_per_liter: Base fuel efficiency when empty (km/L)
        loaded_multiplier: Factor to reduce efficiency when loaded (1.0 = no reduction)
        is_active: Soft delete flag; only active classes appear in forms
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="e.g., 'Small Van', '2-Axle Truck', '3-Axle Truck'"
    )
    base_km_per_liter = models.FloatField(
        validators=[MinValueValidator(1.0)],
        help_text="Fuel efficiency when empty (km/L)"
    )
    loaded_multiplier = models.FloatField(
        default=0.85,
        validators=[MinValueValidator(0.5), MaxValueValidator(1.0)],
        help_text="Multiplier applied to base km/L when loaded (e.g., 0.85 = 15% reduction)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive classes don't appear in selection forms"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Truck Classes"

    def __str__(self):
        return self.name

    def get_effective_km_per_liter(self, is_loaded):
        """
        Calculate effective fuel efficiency for given load status.
        
        Args:
            is_loaded (bool): True if truck is loaded, False if empty
            
        Returns:
            float: Effective km/L for this truck class
        """
        if is_loaded:
            return self.base_km_per_liter * self.loaded_multiplier
        return self.base_km_per_liter