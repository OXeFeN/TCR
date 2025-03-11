# core/views.py
from django.shortcuts import render

def home(request):
    """
    Zobrazí domovskou stránku.
    """
    return render(request, 'home.html')

def about(request):
    """
    Zobrazí stránku 'O klubu'.
    """
    return render(request, 'about.html')
