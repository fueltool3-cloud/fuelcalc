from django.shortcuts import render
from .forms import FuelCalculatorForm
from .services import calculate_fuel

def fuel_calculator(request):
    """
    Main view: display form and handle calculation.
    
    GET: Render blank/default form
    POST: Validate input, calculate fuel, render form with results
    """
    result = None
    error = None

    if request.method == 'POST':
        form = FuelCalculatorForm(request.POST)
        
        if form.is_valid():
            try:
                # Extract validated data
                trip_distance = form.cleaned_data['trip_distance']
                truck_class = form.cleaned_data['truck_class']
                load_status = form.cleaned_data['load_status']
                is_loaded = (load_status == 'loaded')
                buffer_pct = form.cleaned_data['buffer_percentage']
                intended_fuel = form.cleaned_data.get('intended_fuel') or None

                # Call business logic
                result = calculate_fuel(
                    trip_distance_km=trip_distance,
                    truck_class=truck_class,
                    is_loaded=is_loaded,
                    buffer_percentage=buffer_pct,
                    intended_fuel_liters=intended_fuel
                )
                
            except ValueError as e:
                error = f"Calculation error: {str(e)}"
    else:
        form = FuelCalculatorForm()

    context = {
        'form': form,
        'result': result,
        'error': error,
    }
    return render(request, 'calculator/fuel_form.html', context)