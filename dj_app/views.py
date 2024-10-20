from django.shortcuts import render
from django.http import JsonResponse
from .scripts.urlToResponse import mainf

def custom_page(request):
    return render(request, 'custom_page.html')

import markdown

def process_input(request):
    if request.method == 'POST':
        input_text = request.POST.get('textInput', '')  # Get the input text
        result = mainf(input_text)  # Call your function

        # Convert Markdown to HTML
        html_result = markdown.markdown(result)

        # Return as a JsonResponse, making sure the HTML is returned safely
        return JsonResponse({'output': html_result})