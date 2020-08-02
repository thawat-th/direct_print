# ./direct_print/api/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('welcome', views.welcome),
    path('printers', views.printers),
    path('printers/default', views.printers_default),
    path('print', views.print_data),
    path('print/binary', views.printers),
    path('print/url', views.printers),
]