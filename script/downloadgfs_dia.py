import ftplib
from ftplib import FTP
import arcpy
import time
import os
import sys
from datetime import datetime
import tempfile
import types


##tiempo inicio
ti = time.strftime("%c")

message_count = arcpy.GetMessageCount()

mess = ti+ " Inicia"
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

#captura parametros
fecha = arcpy.GetParameter(0) or "01/03/2016"
dout = arcpy.GetParameter(1) or os.getcwd()  
ftpdir = arcpy.GetParameter(2) or "nomads.ncdc.noaa.gov"
dirdown = arcpy.GetParameter(3) or "/GFS/analysis_only"
comodin = arcpy.GetParameter(4) or "gfsanl_4"
comodin = str(comodin)
excluir = arcpy.GetParameter(5) or ".inv"
excluir = str(excluir)


#validar fecha
fechastr = ""
if isinstance(fecha,datetime):
    fechastr = fecha.strftime("%d/%m/%Y")
else:
    fechastr = str(fecha)

#Validar directorio 
doutstr = ""
if isinstance(dout,arcpy.Parameter):
    doutstr = str(dout.valueAsText())
else:
    doutstr = str(dout)
    

mess = "Parámetros de entrada"
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess
mess = "Fecha: "+fechastr
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess
mess = "Directorio Salida: "+doutstr
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess
mess = "FTP de descarga: "+ ftpdir
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess
mess = "Carpeta FTP: "+dirdown
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess
mess = "Comodín: "+comodin
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess
mess = "Excluir: "+excluir
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

##convertir fecha

fechaformat = datetime.strptime(fechastr, '%d/%m/%Y')

dd = fechaformat.strftime('%d')
mess = "Día: "+dd
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

mm = fechaformat .strftime('%m')
mess = "Mes: "+ mm
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

yy = fechaformat.strftime('%Y')
mess = "Año: "+ yy
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

#carpeta salida
dirout = doutstr #"C:\\Users\\cromero\\Documents\\tesis\\python\\datosgfs"
dirmain = dirdown
ftpuri = ftpdir

#año - mes - dia descargar
ano = yy
mes = mm
dia = dd

#cadena de carpetas
sub1 = ano+mes
sub2 = ano+mes+dia
subt = "/"+ sub1 +"/"+sub2

#crea los directorios de descarga
#carpeta para descargar
dirtime = time.strftime("%d%m%Y%H%M%S")

dir1 = os.path.join(dirout, dirtime)
mess = "creando directorio base para descarga de datos ... "+dir1
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess
if not os.path.exists(dir1):
    os.makedirs(dir1)

dir2 = os.path.join(dir1, sub1)
mess = "creando directorio mes para descarga de datos ... "+dir2
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess
if not os.path.exists(dir2):
    os.makedirs(dir2)

dir3 = os.path.join(dir2, sub2)
mess = "creando directorio día para descarga de datos ... "+dir3
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess
if not os.path.exists(dir3):
    os.makedirs(dir3)

#ingreso al ftp y directorio principal
try:
    ftps = FTP(ftpuri)
    ftps.login()
    ftps.cwd(dirmain)
except (ftplib.all_errors), msg:
    mess = "[-] ha ocurrido un error ingresando al ftp: " +  str(msg) + " Revise si la ruta existe en el FTP "+dirmain
    arcpy.AddMessage(mess)
    print(arcpy.GetMessage(message_count - 1))
    print mess
    sys.exit(0)

##
####acceso subdirectorio
try:
    ftps.cwd(sub1)
    ftps.cwd(sub2)
except (ftplib.all_errors), msg:
    mess = "[-] ha ocurrido un error accediendo a los subdirectorios: " + str(msg) + "Revise si la ruta existe" + subt + "en el FTP"
    arcpy.AddMessage(mess)
    print(arcpy.GetMessage(message_count - 1))
    print mess
    ftps.quit()
    sys.exit(0)
    
filelist=ftps.nlst()
#print filelist

ndfiles = 0 
numfiles = len(filelist)

mess = "total archivos para la descarga "+str(numfiles)
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

try:
    for file in filelist:
        ndfiles = int(ndfiles) + 1
        

        comodin.replace(" ", "")
        if comodin not in str(file) and comodin!="":
            mess = "No se descargará... "+str(ndfiles)+"/"+str(numfiles)+" "+file+" nombre no coincide con el comodín "+comodin
            arcpy.AddMessage(mess)
            print(arcpy.GetMessage(message_count - 1))
            print mess
            continue

        excluir.replace(" ", "")
        if excluir in str(file) and excluir!="":
            mess = "No se descargará... "+str(ndfiles)+"/"+str(numfiles)+" "+file+" nombre coincide con cadena excluida "+excluir
            arcpy.AddMessage(mess)
            print(arcpy.GetMessage(message_count - 1))
            print mess
            continue

        mess = "descargando... "+str(ndfiles)+"/"+str(numfiles)+" "+file
        arcpy.AddMessage(mess)
        print(arcpy.GetMessage(message_count - 1))
        print mess

        ##se agrega continue para continuar con el ciclo y no descargar mienttras se prueba
        #continue

        
        ftps.retrbinary("RETR " + file, open(os.path.join(dir3, file),"wb").write)

        #se agrega break mientras se hace debug
        #así descargará un solo grib dato.
        #break
except (ftplib.all_errors), msg:
     mess = "Error: el archivo no puede ser descargado " + file + " - " + str(msg)
     arcpy.AddMessage(mess)
     print(arcpy.GetMessage(message_count - 1))
     print mess
     ftps.quit()
     sys.exit(0)

arcpy.SetParameter(6, dir1)

##cerrar conexion y tiempo
ftps.quit()
tf = time.strftime("%c")

mess = "tus datos se encuentran descargado en en "+dir1
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

mess = tf +' Fin'
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

