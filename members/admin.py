# members/admin.py

from django.contrib import admin
from .models import GroundwaterPDF
from django.contrib import messages
from .pdf_processor_file import process_pdf_file  # we’ll write this

@admin.register(GroundwaterPDF)
class GroundwaterPDFAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_at', 'file')
    actions = ['process_pdf']

    def process_pdf(self, request, queryset):
        for obj in queryset:
            result = process_pdf_file(obj.file.path)
            messages.success(request, f"{result} entries processed from {obj.file.name}")
    process_pdf.short_description = "🧪 Process selected PDF(s)"
