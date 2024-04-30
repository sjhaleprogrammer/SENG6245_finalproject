from django.shortcuts import render
from datetime import date
from .models import AISummary

def index(request):
    
    data = AISummary.objects.filter(created_at= date.today() )
    
    return render(request, 'index.html', {'processed_data': data[0].text})
