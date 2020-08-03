# ./direct_print/api/urls.py

from django.urls import path

from .views import PrintFileView, PrinterView

urlpatterns = [
    path(r'v1/print', PrintFileView.as_view(), name='Print'),
    path(r'v1/printers', PrinterView.as_view(), name='Printer'),
]
