import arcpy
import os
import subprocess
import os.path
from arcpy import env
from arcpy.sa import *
from subprocess import call

arcpy.env.overwriteOutput = 1
arcpy.CheckOutExtension("Spatial")

dirpath = os.path.dirname(os.path.realpath(__file__))
srutawgrib2 = dirpath+"\\wgrib2\\Windows_7\\wgrib2.exe"
ext = ".grib2"
##tiempo inicio
ti = time.strftime("%c")

message_count = arcpy.GetMessageCount()
mess = ti+ " Inicia"
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

inPath = arcpy.GetParameter(0) or "C:\\windanalyst\\data\\gfs\\201808" 
ouPath = arcpy.GetParameter(1) or inPath
match = arcpy.GetParameter(2) or "10 m above ground"
delete = arcpy.GetParameter(3) or True
Sistema_de_coordenadas_de_salida = arcpy.GetParameterAsText(4)
Transformacion_geografica = ""
if Sistema_de_coordenadas_de_salida == '#' or not Sistema_de_coordenadas_de_salida:
    Sistema_de_coordenadas_de_salida = "GEOGCS['GCS_Coordinate_System_imported_from_GRIB_file',DATUM['D_unknown',SPHEROID['Sphere',6371229.0,0.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 11258999068426.2;-100000 10000;-100000 10000;8.99289281755252E-09;0.001;0.001;IsHighPrecision"
    Sistema_de_coordenadas_de_salida2 =Sistema_de_coordenadas_de_salida
else:
    Sistema_de_coordenadas_de_salida2 = str(Sistema_de_coordenadas_de_salida)
zone = arcpy.GetParameterAsText(5)
if zone == '#' or not zone:
    zone =  "C:\\windanalyst\\data\\zone.gdb\\palmira" # provide a default value if unspecified

bbox = arcpy.GetParameterAsText(6)
if bbox == '#' or not bbox:
    bbox = "-8517538.459500 414133.688800 -8457878.461800 383239.996000" # provide a default value if unspecified


vel = arcpy.GetParameter(7) or True


exc = arcpy.GetParameterAsText(8)
if exc  == '#' or not exc :
    exc  = "C:\windanalyst\script\exclude.txt" # provide a default value if unspecified


text_file = open(exc, "r")
exclude = text_file.read().split(',')


inPath2 = inPath
if hasattr(inPath, 'value'):
    inPath2 = inPath.value

match2 = match
if hasattr(match, 'value'):
    match2 = match.value

ouPath2 = ouPath
if hasattr(ouPath, 'value'):
    ouPath2 = ouPath.value

mess = "Ruta de entrada: "+inPath2
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

mess = "Ruta de Salida: "+ouPath2 
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

mess = "Match: "+match2 
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

mess = "Borrar Datos de entrada: "+str(delete)
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

mess = "Zona: "+str(zone)
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

mess = "SRS Salida: "+str(Sistema_de_coordenadas_de_salida2)
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

mess = "BBOX: "+str(bbox)
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess


mess = "Calcular Velocidad: "+str(vel)
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess


dirs  = os.listdir( inPath2 )
baseName = os.path.basename(inPath2)
fpath = os.path.join( ouPath2, baseName+"_DATA.gdb" )
fpats = os.path.join( ouPath2, baseName+"_STATS.gdb" )

fpathv = os.path.join( ouPath2, baseName+"_DATA_V.gdb" )
fpatsv = os.path.join( ouPath2, baseName+"_STATS_V.gdb" )
    

if arcpy.Exists(fpath):
    arcpy.Delete_management(fpath)
    arcpy.Delete_management(fpats)

#crear FGDB Salida datos
arcpy.CreateFileGDB_management(ouPath2, baseName+"_DATA")
arcpy.CreateFileGDB_management(ouPath2, baseName+"_STATS")

if vel == True:
    if arcpy.Exists(fpathv):
        arcpy.Delete_management(fpathv)
        arcpy.Delete_management(fpatsv)
    arcpy.CreateFileGDB_management(ouPath2, baseName+"_DATA_V")
    arcpy.CreateFileGDB_management(ouPath2, baseName+"_STATS_V")
    

mess = "FGDB creada en "+ ouPath2 +" con nombre "+os.path.basename(inPath2)+"_DATA.gdb y "+os.path.basename(inPath2)+"STATS_.gdb"
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

mosaiTName = "A"+os.path.basename(inPath2)
mMosaic = os.path.join( fpath, mosaiTName )
arcpy.CreateMosaicDataset_management(in_workspace=fpath, in_mosaicdataset_name=mosaiTName, coordinate_system=Sistema_de_coordenadas_de_salida, num_bands="", pixel_type="", product_definition="NONE", product_band_definitions="")
mess = "Mosaic Dataset SRS de origen: "+str(mMosaic )
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

mosaiTNameV = "A"+os.path.basename(inPath2)
if vel == True:
    
    mMosaicV = os.path.join( fpathv, mosaiTName )
    arcpy.CreateMosaicDataset_management(in_workspace=fpathv, in_mosaicdataset_name=mosaiTNameV, coordinate_system=Sistema_de_coordenadas_de_salida, num_bands="", pixel_type="", product_definition="NONE", product_band_definitions="")
    mess = "Mosaic Dataset SRS de origen: "+str(mMosaic )
    arcpy.AddMessage(mess)
    print(arcpy.GetMessage(message_count - 1))
    print mess
    

procesados = []
procesadoT = []
procesadvv = []
procesadoV = []

mean = []
median = []
majority = []
mosaics = []
mosaicsV = []

for file in dirs:

    if file == os.path.basename(inPath2)+".gdb":
        continue
    if any(file in s for s in exclude):
    #if file in exclude:
        mess = "No se procesara "+ file
        arcpy.AddMessage(mess)
        print(arcpy.GetMessage(message_count - 1))
        print mess
        continue

    mess = "Carpeta: "+file
    arcpy.AddMessage(mess)
    print(arcpy.GetMessage(message_count - 1))
    print mess

    jpath = os.path.join( inPath2, file )
    mess = "Ruta de extraccion actual: "+jpath 
    arcpy.AddMessage(mess)
    print(arcpy.GetMessage(message_count - 1))
    print mess
    
    arcpy.env.workspace = jpath
    arcpy.env.scratchWorkspace = jpath

    mosaicName = "R"+file
    rMosaic = os.path.join( fpath, mosaicName )
    arcpy.CreateMosaicDataset_management(in_workspace=fpath, in_mosaicdataset_name=mosaicName, coordinate_system=Sistema_de_coordenadas_de_salida, num_bands="", pixel_type="", product_definition="NONE", product_band_definitions="")
    mess = "Mosaic Dataset SRS de origen: "+str(rMosaic )
    arcpy.AddMessage(mess)
    print(arcpy.GetMessage(message_count - 1))
    print mess

    if vel == True:
        mosaicNameV = "R"+file
        rMosaicV = os.path.join( fpathv, mosaicName )
        arcpy.CreateMosaicDataset_management(in_workspace=fpathv, in_mosaicdataset_name=mosaicNameV, coordinate_system=Sistema_de_coordenadas_de_salida, num_bands="", pixel_type="", product_definition="NONE", product_band_definitions="")
        mess = "Mosaic Dataset SRS de origen: "+str(rMosaicV )
        arcpy.AddMessage(mess)
        print(arcpy.GetMessage(message_count - 1))
        print mess


    rasters = arcpy.ListRasters("*",'*')
    noFile = []
    
    for hdf in rasters:
        ver = False
        if hdf in exclude:
            continue

        if any(hdf in s for s in exclude):
        #if file in exclude:
            mess = "No se procesara "+ hdf
            arcpy.AddMessage(mess)
            print(arcpy.GetMessage(message_count - 1))
            print mess
            continue
        for g in exclude:
            
            print hdf
            print g
            print str(hdf).find(g)
            if g in hdf:
                mess = "No se procesara "+ hdf
                arcpy.AddMessage(mess)
                print(arcpy.GetMessage(message_count - 1))
                print mess
                ver = True
        if ver == True:
            continue
                

        try:
            desc = arcpy.Describe (hdf)
        except:
            noFile.append(hdf)
            continue
        sfile = os.path.join(desc.path,desc.file)
        dfile = os.path.join(ouPath2,desc.baseName)
        mfile = os.path.join(fpath,desc.baseName)
        mfilv = os.path.join(fpathv,desc.baseName)


        mess = "Procesando "+desc.catalogPath+ " - "+desc.dataType+ " - " +desc.baseName
        arcpy.AddMessage(mess)
        print(arcpy.GetMessage(message_count - 1))
        print mess

        if vel == True:

            arcpy.env.workspace = fpathv
            arcpy.env.scratchWorkspace = fpathv
            
            gwind = dfile+"_WIND"+ext
            callWind = srutawgrib2+ " "+sfile+" -wind_speed "+gwind +" -match \""+match2+"\""
            mess = "Extrayendo velocidad viento "+callWind
            arcpy.AddMessage(mess)
            print(arcpy.GetMessage(message_count - 1))
            print mess
            os.system(callWind)

            mess = "Recortando zona velocidad viento "
            arcpy.AddMessage(mess)
            print(arcpy.GetMessage(message_count - 1))
            print mess
            
            outClipV = os.path.join(fpathv,mfilv+"_WIND")
            #print outClipV, fpathv, mfile
            arcpy.Clip_management(gwind, bbox, outClipV, zone, "-1,797693e+308", "NONE", "NO_MAINTAIN_EXTENT")
          
            mess = "Agregando Raster proyectado velocidad viento "+ str(gwind)+ " a mosaico "+str(rMosaicV)
            arcpy.AddMessage(mess)
            print(arcpy.GetMessage(message_count - 1))
            print mess
            arcpy.AddRastersToMosaicDataset_management(in_mosaic_dataset=rMosaicV, raster_type="Raster Dataset", input_path=outClipV, update_cellsize_ranges="UPDATE_CELL_SIZES", update_boundary="UPDATE_BOUNDARY", update_overviews="NO_OVERVIEWS", maximum_pyramid_levels="", maximum_cell_size="0", minimum_dimension="1500", spatial_reference="", filter="#", sub_folder="SUBFOLDERS", duplicate_items_action="ALLOW_DUPLICATES", build_pyramids="NO_PYRAMIDS", calculate_statistics="NO_STATISTICS", build_thumbnails="NO_THUMBNAILS", operation_description="#", force_spatial_reference="NO_FORCE_SPATIAL_REFERENCE", estimate_statistics="NO_STATISTICS", aux_inputs="")

            if delete == True:
                os.remove(gwind)

            #print outClipV
            #sys.exit(0)
            
        arcpy.env.workspace = fpath
        arcpy.env.scratchWorkspace = fpath
        
        gwdir = dfile+"_WDIR"+ext
        callWdir = srutawgrib2+ " "+sfile+" -wind_dir "+gwdir+" -match \""+match2+"\""
        mess = "Extrayendo direccion viento "+callWdir
        arcpy.AddMessage(mess)
        print(arcpy.GetMessage(message_count - 1))
        print mess
        os.system(callWdir)

        mess = "Recortando zona direccion viento "
        arcpy.AddMessage(mess)
        print(arcpy.GetMessage(message_count - 1))
        print mess
        outClipD = os.path.join(fpath,mfile+"_WDIR")
        arcpy.Clip_management(in_raster=gwdir, rectangle=bbox, out_raster=outClipD, in_template_dataset=zone, nodata_value="-1.797693e+308", clipping_geometry="NONE", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
        
        mess = "Agregando Raster Direccion viento "+ str(gwdir)+ " a mosaico "+str(rMosaic) 
        arcpy.AddMessage(mess)
        print(arcpy.GetMessage(message_count - 1))
        print mess
        arcpy.AddRastersToMosaicDataset_management(in_mosaic_dataset=rMosaic, raster_type="Raster Dataset", input_path=outClipD, update_cellsize_ranges="UPDATE_CELL_SIZES", update_boundary="UPDATE_BOUNDARY", update_overviews="NO_OVERVIEWS", maximum_pyramid_levels="", maximum_cell_size="0", minimum_dimension="1500", spatial_reference="", filter="#", sub_folder="SUBFOLDERS", duplicate_items_action="ALLOW_DUPLICATES", build_pyramids="NO_PYRAMIDS", calculate_statistics="NO_STATISTICS", build_thumbnails="NO_THUMBNAILS", operation_description="#", force_spatial_reference="NO_FORCE_SPATIAL_REFERENCE", estimate_statistics="NO_STATISTICS", aux_inputs="")
        

        if delete == True:
            os.remove(gwdir)

        procesadoT.append(outClipD)
        procesados.append(hdf)
        if vel ==  True:
            procesadoV.append(outClipV)
        ##break

    
    
    mosaics.append( rMosaic)
    if vel == True:
        mosaicsV.append( rMosaicV)
    mess = "Computando Estaditicas diarias"
    arcpy.AddMessage(mess)
    print(arcpy.GetMessage(message_count - 1))
    print mess

    jStat = os.path.join( fpats, "R"+file+"WDIR"+"_MAJORITY" )
    eStat = os.path.join( fpats, "R"+file+"WDIR"+"_MEDIAN" )
    mStat = os.path.join( fpats, "R"+file+"WDIR"+"_MEAN" )

    if vel == True:
        jStatv = os.path.join( fpatsv, "R"+file+"WIND"+"_MAJORITY" )
        eStatv = os.path.join( fpatsv, "R"+file+"WIND"+"_MEDIAN" )
        mStatv = os.path.join( fpatsv, "R"+file+"WIND"+"_MEAN" )

    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")

    # Execute CellStatistics and # Save the output 
    outCellStatisticsMaj = CellStatistics(procesadoT, "MAJORITY", "NODATA")
    outCellStatisticsMaj.save(jStat)

    outCellStatisticsMaj = CellStatistics(procesadoT, "MEDIAN", "NODATA")
    outCellStatisticsMaj.save(eStat)

    outCellStatisticsMaj = CellStatistics(procesadoT, "MEAN", "NODATA")
    outCellStatisticsMaj.save(mStat)

    if vel == True:
        # Execute CellStatistics and # Save the output
        outCellStatisticsMaj = CellStatistics(procesadoV, "MAJORITY", "NODATA")
        outCellStatisticsMaj.save(jStatv)

        outCellStatisticsMaj = CellStatistics(procesadoV, "MEDIAN", "NODATA")
        outCellStatisticsMaj.save(eStatv)

        outCellStatisticsMaj = CellStatistics(procesadoV, "MEAN", "NODATA")
        outCellStatisticsMaj.save(mStatv)
        


arcpy.env.workspace = fpath
arcpy.env.scratchWorkspace = fpath
mess = "Computando Estaditicas totales"
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

rasters = arcpy.ListRasters("*", "ALL")

jStat = os.path.join( fpats, "WDIR"+"_MAJORITY" )
eStat = os.path.join( fpats, "WDIR" +"_MEDIAN" )
mStat = os.path.join( fpats, "WDIR"+"_MEAN" )
xStat = os.path.join( fpats, "WDIR"+"_MAXIMUN" )
nStat = os.path.join( fpats, "WDIR"+"_MINIMUN" )
iStat = os.path.join( fpats, "WDIR"+"_MINORITY" )
rStat = os.path.join( fpats, "WDIR"+"_RANGE" )
sStat = os.path.join( fpats, "WDIR"+"_STD" )
uStat = os.path.join( fpats, "WDIR"+"_SUM" )
vStat = os.path.join( fpats, "WDIR"+"_VARIETY" )

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Execute CellStatistics and # Save the output 
outCellStatisticsMaj = CellStatistics(rasters, "MAJORITY", "NODATA")
outCellStatisticsMaj.save(jStat)

outCellStatisticsMaj = CellStatistics(rasters, "MEDIAN", "NODATA")
outCellStatisticsMaj.save(eStat)

outCellStatisticsMaj = CellStatistics(rasters, "MEAN", "NODATA")
outCellStatisticsMaj.save(mStat)

outCellStatisticsMaj = CellStatistics(rasters, "MAXIMUM", "NODATA")
outCellStatisticsMaj.save(xStat)

outCellStatisticsMaj = CellStatistics(rasters, "MINIMUM", "NODATA")
outCellStatisticsMaj.save(nStat)

outCellStatisticsMaj = CellStatistics(rasters, "MINORITY", "NODATA")
outCellStatisticsMaj.save(iStat)

outCellStatisticsMaj = CellStatistics(rasters, "RANGE", "NODATA")
outCellStatisticsMaj.save(rStat)

outCellStatisticsMaj = CellStatistics(rasters, "STD", "NODATA")
outCellStatisticsMaj.save(sStat)

outCellStatisticsMaj = CellStatistics(rasters, "SUM", "NODATA")
outCellStatisticsMaj.save(uStat)

outCellStatisticsMaj = CellStatistics(rasters, "VARIETY", "NODATA")
outCellStatisticsMaj.save(vStat)

if vel == True:
    arcpy.env.workspace = fpathv
    arcpy.env.scratchWorkspace = fpathv
    mess = "Computando Estaditicas totales de Velocidad"
    arcpy.AddMessage(mess)
    print(arcpy.GetMessage(message_count - 1))
    print mess

    rasters = arcpy.ListRasters("*", "ALL")

    jStatv = os.path.join( fpatsv, "WIND"+"_MAJORITY" )
    eStatv = os.path.join( fpatsv, "WIND" +"_MEDIAN" )
    mStatv = os.path.join( fpatsv, "WIND"+"_MEAN" )
    xStatv = os.path.join( fpatsv, "WIND"+"_MAXIMUN" )
    nStatv = os.path.join( fpatsv, "WIND"+"_MINIMUN" )
    iStatv = os.path.join( fpatsv, "WIND"+"_MINORITY" )
    rStatv = os.path.join( fpatsv, "WIND"+"_RANGE" )
    sStatv = os.path.join( fpatsv, "WIND"+"_STD" )
    uStatv = os.path.join( fpatsv, "WIND"+"_SUM" )
    vStatv = os.path.join( fpatsv, "WIND"+"_VARIETY" )

    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")

    # Execute CellStatistics and # Save the output 
    outCellStatisticsMaj = CellStatistics(rasters, "MAJORITY", "NODATA")
    outCellStatisticsMaj.save(jStatv)

    outCellStatisticsMaj = CellStatistics(rasters, "MEDIAN", "NODATA")
    outCellStatisticsMaj.save(eStatv)

    outCellStatisticsMaj = CellStatistics(rasters, "MEAN", "NODATA")
    outCellStatisticsMaj.save(mStatv)

    outCellStatisticsMaj = CellStatistics(rasters, "MAXIMUM", "NODATA")
    outCellStatisticsMaj.save(xStatv)

    outCellStatisticsMaj = CellStatistics(rasters, "MINIMUM", "NODATA")
    outCellStatisticsMaj.save(nStatv)

    outCellStatisticsMaj = CellStatistics(rasters, "MINORITY", "NODATA")
    outCellStatisticsMaj.save(iStatv)

    outCellStatisticsMaj = CellStatistics(rasters, "RANGE", "NODATA")
    outCellStatisticsMaj.save(rStatv)

    outCellStatisticsMaj = CellStatistics(rasters, "STD", "NODATA")
    outCellStatisticsMaj.save(sStatv)

    outCellStatisticsMaj = CellStatistics(rasters, "SUM", "NODATA")
    outCellStatisticsMaj.save(uStatv)

    outCellStatisticsMaj = CellStatistics(rasters, "VARIETY", "NODATA")
    outCellStatisticsMaj.save(vStatv)

##tiempo final
tf = time.strftime("%c")

message_count = arcpy.GetMessageCount()

mess = "Total Archivos Procesados" +str(len(procesados))+ " "+ str(procesados)
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

mess = tf+ " Finaliza"
arcpy.AddMessage(mess)
print(arcpy.GetMessage(message_count - 1))
print mess

