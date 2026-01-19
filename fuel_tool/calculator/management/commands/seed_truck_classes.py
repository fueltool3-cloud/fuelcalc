from django.core.management.base import BaseCommand
from calculator.models import TruckClass

class Command(BaseCommand):
    help = "Seed common Nigerian truck classes with fuel efficiency data"

    def handle(self, *args, **options):
        truck_classes = [
            {
                "name": "Mini Pickup / Small Van",
                "base_km_per_liter": 12.0,
                "loaded_multiplier": 0.90,
            },
            {
                "name": "Pickup Truck (Toyota Hilux Class)",
                "base_km_per_liter": 12.0,
                "loaded_multiplier": 0.85,
            },
            {
                "name": "Medium Truck (Isuzu ELF / Dyna / Canter)",
                "base_km_per_liter": 9.0,
                "loaded_multiplier": 0.80,
            },
            {
                "name": "2-Axle Truck",
                "base_km_per_liter": 5.0,
                "loaded_multiplier": 0.85,
            },
            {
                "name": "3-Axle Truck / Heavy Duty",
                "base_km_per_liter": 4.0,
                "loaded_multiplier": 0.75,
            },
        ]

        created_count = 0

        for data in truck_classes:
            obj, created = TruckClass.objects.get_or_create(
                name=data["name"],
                defaults={
                    "base_km_per_liter": data["base_km_per_liter"],
                    "loaded_multiplier": data["loaded_multiplier"],
                    "is_active": True,
                }
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Truck class seeding complete. {created_count} new records added."
            )
        )
