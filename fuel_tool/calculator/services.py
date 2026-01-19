"""
Business logic for fuel allocation calculations.
Isolated from views/forms to enable reuse and testing.
"""

from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class FuelRecommendation:
    """
    Immutable result of a fuel allocation calculation.
    Attributes:
        effective_km_per_liter: Fuel efficiency after load adjustment
        base_fuel_liters: Fuel required for distance at effective efficiency
        min_fuel_liters: Minimum recommended (base)
        max_fuel_liters: Maximum recommended (base + buffer)
        buffer_percentage: Safety buffer applied
        warning_message: Alert if intended_fuel exceeds max (None if no warning)
    """
    effective_km_per_liter: float
    base_fuel_liters: float
    min_fuel_liters: float
    max_fuel_liters: float
    buffer_percentage: float
    warning_message: Optional[str] = None

    def __str__(self):
        """Human-readable summary."""
        result = (
            f"Effective Efficiency: {self.effective_km_per_liter:.2f} km/L\n"
            f"Base Fuel Required: {self.base_fuel_liters:.2f} L\n"
            f"Recommended Range: {self.min_fuel_liters:.2f} – {self.max_fuel_liters:.2f} L\n"
            f"Buffer Applied: {self.buffer_percentage}%"
        )
        if self.warning_message:
            result += f"\n⚠️  {self.warning_message}"
        return result


def calculate_fuel(
    trip_distance_km: float,
    truck_class,
    is_loaded: bool,
    buffer_percentage: float,
    intended_fuel_liters: Optional[float] = None
) -> FuelRecommendation:
    """
    Calculate recommended fuel range for a delivery trip.
    
    Args:
        trip_distance_km: Distance in km (validated > 0)
        truck_class: TruckClass model instance
        is_loaded: Boolean; True if truck is loaded
        buffer_percentage: Safety buffer %; validated 5–25
        intended_fuel_liters: Optional; user's planned fuel amount
        
    Returns:
        FuelRecommendation with calculation results and optional warning
        
    Raises:
        ValueError: If inputs are invalid (shouldn't happen if form validation works)
    """
    
    # Validate critical inputs
    if trip_distance_km <= 0:
        raise ValueError("Trip distance must be positive.")
    if buffer_percentage < 5 or buffer_percentage > 25:
        raise ValueError("Buffer percentage must be 5–25%.")
    if truck_class is None:
        raise ValueError("Truck class is required.")
    
    # Step 1: Lookup effective fuel efficiency for this truck and load
    effective_km_per_liter = truck_class.get_effective_km_per_liter(is_loaded)
    
    # Step 2: Calculate base fuel (distance / efficiency)
    base_fuel_liters = trip_distance_km / effective_km_per_liter
    
    # Step 3: Apply safety buffer
    buffer_fuel_liters = base_fuel_liters * (buffer_percentage / 100.0)
    max_fuel_liters = base_fuel_liters + buffer_fuel_liters
    
    # Step 4: Check for warning if intended fuel provided
    warning_message = None
    if intended_fuel_liters is not None and intended_fuel_liters > 0:
        if intended_fuel_liters > max_fuel_liters:
            excess = intended_fuel_liters - max_fuel_liters
            warning_message = (
                f"Intended fuel ({intended_fuel_liters:.2f} L) exceeds recommended max "
                f"({max_fuel_liters:.2f} L) by {excess:.2f} L. Review this decision."
            )
    
    return FuelRecommendation(
        effective_km_per_liter=effective_km_per_liter,
        base_fuel_liters=base_fuel_liters,
        min_fuel_liters=base_fuel_liters,
        max_fuel_liters=max_fuel_liters,
        buffer_percentage=buffer_percentage,
        warning_message=warning_message
    )