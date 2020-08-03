from django.db import models


class Printer(models.Model):
    printer_name = models.TextField


class Print(models.Model):
    file = models.FileField()
