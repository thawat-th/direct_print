import base64

import win32print
from django.http import JsonResponse
from rest_framework.decorators import api_view

# from api.forms import DocumentForm
# from api.models import Document
from api.serializers import DocumentSerializer


@api_view(["GET"])
def welcome(request):
    content = {
        "message": "Welcome to the Direct print"
    }
    return JsonResponse(content)


@api_view(["GET"])
def printers(request):
    list = win32print.EnumPrinters(win32print.PRINTER_ENUM_NAME, None, 1)
    return JsonResponse(list, safe=False)


@api_view(["GET"])
def printers_default(request):
    printer = win32print.GetDefaultPrinter()
    return JsonResponse(printer, safe=False)


@api_view(["POST"])
def print_data(request):
    raw = request.POST.get("data")
    data = base64.b64decode(raw, None, True)
    if data:
        print_job(data)
    return JsonResponse("", safe=False)


@api_view(["POST"])
def print_binary(request, pk=None):
    serializer = DocumentSerializer(instance=None, data=request.data)

    # form = DocumentForm(request.POST, request.FILES)
    # if form.is_valid():
    #     newdoc = Document(docfile=request.FILES['docfile'])
    #     newdoc.save()
    return None


def print_job(data):
    printer = win32print.GetDefaultPrinter()
    if printer:
        print("Print job!")
        op = win32print.OpenPrinter(printer)
        win32print.StartDocPrinter(op, 1, ("Printing", None, "RAW"))
        win32print.StartPagePrinter(op)
        win32print.WritePrinter(op, data)
        win32print.EndPagePrinter(op)
        win32print.EndDocPrinter(op)
        win32print.ClosePrinter(op)
    else:
        print("Printer not found!")


