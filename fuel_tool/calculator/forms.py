from django import forms
from django.core.exceptions import ValidationError
from .models import TruckClass

class FuelCalculatorForm(forms.Form):
    """
    Form for capturing trip parameters and calculating fuel recommendation.
    Validates all inputs at form level before passing to business logic.
    """
    LOAD_CHOICES = [
        ('empty', 'Empty'),
        ('loaded', 'Loaded'),
    ]

    trip_distance = forms.FloatField(
        min_value=0.01,
        max_value=1000,
        label='Trip Distance (km)',
        widget=forms.NumberInput(attrs={
            'placeholder': 'e.g., 150',
            'step': '0.1',
            'class': 'form-input',
        }),
        help_text='Must be between 0 and 1000 km'
    )

    truck_class = forms.ModelChoiceField(
        queryset=TruckClass.objects.filter(is_active=True),
        label='Truck Class',
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='-- Select a truck class --'
    )

    load_status = forms.ChoiceField(
        choices=LOAD_CHOICES,
        label='Load Status',
        widget=forms.RadioSelect(attrs={'class': 'form-radio'}),
        initial='empty'
    )

    buffer_percentage = forms.FloatField(
        min_value=5,
        max_value=25,
        initial=12,
        label='Safety Buffer (%)',
        widget=forms.NumberInput(attrs={
            'placeholder': '12',
            'step': '1',
            'class': 'form-input',
        }),
        help_text='Default 12% (range 5–25%)'
    )

    intended_fuel = forms.FloatField(
        min_value=0,
        required=False,
        label='Intended Fuel to Issue (litres) — Optional',
        widget=forms.NumberInput(attrs={
            'placeholder': 'e.g., 100 (leave blank to skip)',
            'step': '0.1',
            'class': 'form-input',
        }),
        help_text='Leave blank to skip warning check'
    )

    def clean(self):
        """
        Cross-field validation: ensure intended_fuel (if provided) is reasonable.
        """
        cleaned_data = super().clean()
        intended = cleaned_data.get('intended_fuel')
        
        # If intended_fuel was provided (not empty string or None), validate it
        if intended is not None and intended > 0:
            if intended < 5:
                raise ValidationError(
                    'Intended fuel should be at least 5 litres for a valid trip.'
                )
            if intended > 300:
                raise ValidationError(
                    'Intended fuel exceeds reasonable maximum (300 litres). Check your input.'
                )
        
        return cleaned_data