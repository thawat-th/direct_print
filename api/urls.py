# ./direct_print/api/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('welcome', views.welcome),
    path('/v1/printers', views.printers),
    path('/v1/printers/default', views.printers_default),
    path('/v1/print', views.print_data),
    path('/v1/print/binary', views.printers),
    path('/v1/print/url', views.printers),
]