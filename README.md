# windanalyst
ArcGIS Tools to make wind Maps and analyze data


#### Download and Install
Download unzip and rename in C:\windanalyst

All the example data to process the tools are on C:\windanalyst\data

Open ArcCatalog and go to the folder C:\windanalyst\script
Expand the Toolbox WindAnalystGFS.tbx

Now you can see all tools!.



#### Tools Descriptions

* **Beta difference**: Compute the Angle Beta between Wind Velocity and DEM-Aspect.
* **Classify Slope Aspect**: Generates a Slope-Aspect classification on based parameters.
* **Create Wind Rose**: Create a set of constants azimuth rasters N, NE, E, SE, S, SW, W, NW.
* **Download GFS data by day**: Download GFS data by day from given NOAA FTP.
* **Download GFS data by month**: Download GFS data by month from given NOAA FTP.
* **Process GFS Wind Data From Downloaded Folder**: Extract Wind data from downloaded GRIB files and compute statistics.
* **Raster Batch Project**: Project a set of rasters.
* **Select Beta Angle by Wind Rose**: Given a Wind Rose and Aspect compute the angle Beta.
* **Select Slope Aspect**: Create Slope and Aspect from given DEM.

#### Tools Parameters

**1. Select Slope Aspect**


![alt text](https://github.com/crablasph/windanalyst/blob/master/images/1_slope_zone.png)

* **DEM**: Input raster DEM.
* **Output GDB**: Output Geodatabse for Slope and Aspect.
* **slope zone**: Output Slope.
* **aspect zone**: Output Aspect.


**2. Create Wind Rose**


![alt text](https://github.com/crablasph/windanalyst/blob/master/images/2_create_wind_rose.png)

* **Output**: Output Workspace for the data.
* **Cell size**: A size cell value to generate the constants raster.
* **Extent**: Bounding Box for the constants rasters.

**3. Select Beta Angle by Wind Rose**


![alt text](https://github.com/crablasph/windanalyst/blob/master/images/3_select_beta_angle_wr.png)

* **Output**: Output Workspace for the data.
* **Max angle**: Maximun angle for classification.
* **Aspect**: Aspect Raster.

**4. Classify Slope Aspect**


![alt text](https://github.com/crablasph/windanalyst/blob/master/images/4_c_slope_aspect.png)

* **Slope Input**: Slope Raster for classfification.
* **Aspect Input**: Aspect Raster for classfification.
* **Output GDB**: Geodatabase for Output data.
* **Slope Classify**: Slope output for classification.
* **Aspect Selected**: Aspect output for classification.
* **Reclass field**: Field to reclassify.
* **Reclassification**: Table to old-new values.

**5. Download GFS data by day**


![alt text](https://github.com/crablasph/windanalyst/blob/master/images/5_dday.png)

* **Download Day**: Date to download.
* **Output Folder**: Output folder for downloaded data.
* **FTP**: FTP string URL.
* **FTP Folder**: Sub- folder on FTP site.
* **WildCard**: if this string is on file name the script will proceed to download the file.
* **Exclude**: if this string is on file name the script will not proceed to download the file.


**6. Download GFS data by month**


![alt text](https://github.com/crablasph/windanalyst/blob/master/images/6_dmon.png)

* **Download Day of the Month**: Date to download.
* **Output Folder**: Output folder for downloaded data.
* **FTP**: FTP string URL.
* **FTP Folder**: Sub- folder on FTP site.
* **WildCard**: if this string is on file name the script will proceed to download the file.
* **Exclude**: if this string is on file name the script will not proceed to download the file.

**7. Process GFS Wind Data From Downloaded Folder**


![alt text](https://github.com/crablasph/windanalyst/blob/master/images/7_stats.png)

* **Input Folder**: Downloaded folder to process.
* **Output Folder**: Folder for the output data.
* **Match**: Match string variable for wgrib2 extraction. See more https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/.
* **Delete source**: Boolean. If true the GRIB extracted files will be deleted.
* **Output SRS**: Spatial reference system for the output mosaic datasets.
* **Zone**: Zone to clip the data.
* **BBOX**: Extent to clip the data.
* **Vel**: Boolean. If true the velocity will be processed.
* **Exclude**: Strings to be excluded on the file. The hours to exclude on the process on a file.

**8. Beta difference**


![alt text](https://github.com/crablasph/windanalyst/blob/master/images/8_beta_diff.png)

* **Aspect**: Aspect Raster.
* **Map Algebra**: Formula.
* **BETA**: BETA raster output.

**9. Raster Batch Project**


![alt text](https://github.com/crablasph/windanalyst/blob/master/images/9_r_batch_prj.png)



