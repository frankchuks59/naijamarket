# chatbot/views.py
from django.shortcuts import render

def home(request):
    """AI Business Advisor chatbot"""
    return render(request, 'chatbot/home.html')