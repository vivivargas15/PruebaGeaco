from django.shortcuts import render
from django.http import HttpResponse
from . import models
import pandas as pd
import xlsxwriter 
import zipfile
import aspose.words as aw
from docxtpl import DocxTemplate
from .models import Document
import datetime

# Create your views here.

def uploadFile(request):
    if request.method == "POST":
        
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]
        Item= request.POST["Item"]

        # Saving the information in the database
        document = models.Document(
    		title = fileTitle,
            uploadedFile = uploadedFile,
            item=Item
        )
        document.save()

    documents = models.Document.objects.all()

    return render(request, "uploadfile/upload-file.html", context = {
        "files": documents
    })


# no borrar esta
 
def downloadFileExcel(request):
    #se quiere proponer : seleccionar de la base de datos url de upload del objeto k
    #query=models.Document.objects.all()
    #ruta = query.uploadedFile()
    #file= pd.read_json(f'media/{ruta}')
    file= pd.read_json('media/Uploaded Files/datos.json')
    archivos=[]
    for index, fila in file.iterrows():
        wb= xlsxwriter.Workbook(f"uploadfile/excel/doc_generado{index}.xlsx")
        hoja=wb.add_worksheet()
        
        hoja.write(2,2,f"Se remite a Sr(a) {fila['nombre']} la disposición de presentarse en la entidad {fila['entidad']} con su vehículo de placa {fila['placa']}")
        wb.close()
        archivos.append(f"doc_generado{index}.xlsx")

    with zipfile.ZipFile('uploadfile/excel/descarga.zip', 'w') as fzip:
        for archivo in archivos:
            fzip.write(f"uploadfile/excel/{archivo}")

    excel=zipfile.ZipFile(f"uploadfile/excel/descarga.zip", mode="r")
    response= HttpResponse(excel, content_type= 'application/zip')
    response['Content-Disposition']= 'attachment ; filename="descarga.zip"'

    return response

#no borrar

def downloadFileTxt(request):
    #file= pd.read_excel('media/Uploaded Files/datos.xlsx')
    #file= pd.read_csv('media/Uploaded Files/datos.csv')

    file= pd.read_json('C:/Users/COMPUDIDA/Desktop/geaco/uploadfile/datos.json')
    archivos=[]
    for index, fila in file.iterrows():
        doc = open(f"uploadfile/txt/doc_generado{index}.txt","w") 
        doc.write(f"Se remite a Sr(a) {fila['nombre']} la disposición de presentarse en la entidad {fila['entidad']} con su vehículo de placa {fila['placa']}")
        archivos.append(f"doc_generado{index}.txt")

    with zipfile.ZipFile('uploadfile/txt/descarga.zip', 'w') as fzip:
        for archivo in archivos:
            fzip.write(f"uploadfile/txt/{archivo}")
            

           
    txt=zipfile.ZipFile(f"uploadfile/txt/descarga.zip", mode="r")
    response= HttpResponse(txt, content_type= 'application/zip')
    response['Content-Disposition']= 'attachment ; filename="descarga.zip"'

    return response

#no borrar - error linea 98
def downloadFileWord(request):
    doc= DocxTemplate("uploadfile/plantillaword.docx")
    archivos=[]
    file= pd.read_json('C:/Users/COMPUDIDA/Desktop/geaco/uploadfile/datos.json')
    for index, fila in file.iterrows():
        context= {
        'nombre':fila['nombre'],
        'entidad': fila['entidad'],
        'placa': fila['placa']
        }

        doc.render(context)
        doc.save(f"uploadfile/word/doc_generado{index}.docx")
        archivos.append(f"doc_generado{index}.txt")

    with zipfile.ZipFile('uploadfile/word/descarga.zip', 'w') as fzip:
        for archivo in archivos:
            fzip.write(f"uploadfile/word/{archivo}")

    word=zipfile.ZipFile(f"uploadfile/word/descarga.zip", mode="r")
    response= HttpResponse(word, content_type= 'application/zip')
    response['Content-Disposition']= 'attachment ; filename="descarga.zip"'

    return response


def GestionTareas(request):
    fechas=Document.objects.all()

    return render(request,"uploadfile/tarea.html", {'fechas':fechas} )


def GestionTareas(request):
    fechas=Document.objects.all()
      
    return render(request,"uploadfile/tarea.html", {'fechas':fechas} )

