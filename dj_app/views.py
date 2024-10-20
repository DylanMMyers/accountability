from django.shortcuts import render
from django.http import JsonResponse
from .scripts.urlToResponse import mainf

def custom_page(request):
    return render(request, 'custom_page.html')

def process_input(request):
    if request.method == 'POST':
        input_text = request.POST.get('textInput', '')  # Get the input text from the request
        result = mainf(input_text)  # Call the mainf function
        return JsonResponse({'output': result})  # Return the result as JSON
    return JsonResponse({'error': 'Invalid request method'}, status=400)