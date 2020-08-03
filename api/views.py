from pathlib import Path

import win32print
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Printer
from api.serializers import PrintFileSerializer


class PrintFileView(CreateAPIView):
    serializer_class = PrintFileSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        serializer = PrintFileSerializer(data=request.data)

        file = request.FILES['file']
        filename = file.name
        print(filename)
        print(file.content_type)
        print(file.size)

        rd = file.read()

        printer_name = win32print.GetDefaultPrinter()
        print(printer_name)

        print_defaults = {"DesiredAccess": win32print.PRINTER_ACCESS_USE}
        h = win32print.OpenPrinter(printer_name, print_defaults)
        hJob = win32print.StartDocPrinter(h, 1, (filename, None, "RAW"))
        win32print.StartPagePrinter(h)
        b = win32print.WritePrinter(h, rd)
        win32print.EndPagePrinter(h)
        win32print.EndDocPrinter(h)
        win32print.ClosePrinter(h)
        print(b)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrinterView(APIView):
    serializer_class = PrintFileSerializer

    def get(self, request):
        printers = Printer.objects.all()
        serializer = PrintFileSerializer(printers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PrintFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
