# dj_app/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .scripts.urlToResponse import mainf

@csrf_exempt  # Disable CSRF protection for this view
def process_input(request):
    if request.method == 'POST':
        input_text = request.POST.get('textInput', '')  # Get the input text from the request
        result = mainf(input_text)  # Call the mainf function
        return JsonResponse({'output': result})  # Return the result as JSON
    return JsonResponse({'error': 'Invalid request method'}, status=400)
