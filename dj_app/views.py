from django.shortcuts import render

def custom_page(request):
    return render(request, 'custom_page.html')