import win32api
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
        file_obj = request.FILES['file']

        if serializer.is_valid():
            serializer.save()

        printer = win32print.GetDefaultPrinter();

        if printer:
            win32api.ShellExecute(0, "print", file_obj.name, '/d:"%s"' % printer, ".", 0)
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
