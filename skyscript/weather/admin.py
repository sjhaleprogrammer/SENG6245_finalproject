from django.contrib import admin
from .models import Weather, AISummary

admin.site.register(Weather)
admin.site.register(AISummary)

