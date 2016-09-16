# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 14:17:20 2016

FULLY AUTOMATED GIS-BASED INDIVIDUAL TREE CROWN DELINEATION BASED ON CURVATURE VALUES FROM A LIDAR DERIVED CANOPY HEIGHT MODEL IN A CONIFEROUS PLANTATION
@author: R. J. L. Argamosa a,* E.C. Paringit a, K.R. Quinton b, F. A. M. Tandoc a, R. A. G Faelga a, C. A. G. Ibañez a, M. A. V. Posilero a, G. P. Zaragosa a

The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences, Volume XLI-B8, 2016 XXIII ISPRS Congress, 12–19 July 2016, Prague, Czech Republic

The following texts show the code written in Python language that utilizes several arcpy functions to delineate tree crowns as stated in this paper. 
The script can only be executed outside the ArcGIS software and requires that the CHM and the arcpy script is contained in the same folder.
"""

import arcpy, os, shutil
from arcpy.sa import *
import string
from arcpy import env
import arcpy.cartography as CA 
env.overwriteOutput = True
env.workspace=os.getcwd() 
ws=env.workspace 
listchm=arcpy.ListRasters()
class folder:
    def __init__(self):
        self.folder=['fs','rc','rtp','thie','slope','curv','inter','aggre','smooth',' clip']
    def cf(self): 
        self.folder.sort() 
        for i in self.folder:
            if not os.path.exists(ws+'\\'+i): 
                os.makedirs(ws+'\\'+i)

f=folder() 
f.cf()
class crown:
    def __init__(self):
        self.chm=listchm[0] 
        self.pt=ws+'\\'+'rtp'+'\\'+'rtp.shp' 
        self.fs=ws+'\\'+'fs'+'\\'+'fs.tif' 
        self.rc=ws+'\\'+'rc'+'\\'+'rastercalc.tif' 
        self.thie=ws+'\\'+'thie'+'\\'+'thie.shp' 
        self.slope=ws+'\\'+'slope'+'\\'+'slope.tif' 
        self.curv=ws+'\\'+'curv'+'\\'+'curv.tif' 
        self.prof=ws+'\\'+'curv'+'\\'+'prof.tif' 
        self.prof1=ws+'\\'+'rtp'+'\\'+'prof_pt1.shp' 
        self.rtpprof=ws+'\\'+'rtp'+'\\'+'prof_pt.shp' 
        self.clip=ws+'\\'+'clip'+'\\'+'clip.shp' 
        self.int=ws+'\\'+'inter'+'\\'+'int.shp' 
        self.table=ws+'\\'+'inter'+'\\'+'freq' 
        self.diss=ws+'\\'+'inter'+'\\'+'int_diss.shp' 
        self.aggre=ws+'\\'+'aggre'+'\\' 
        self.smooth=ws+'\\'+'smooth'+'\\' 
        self.name='final_crown.shp' 
        self.add=ws+'\\'+'smooth' 
        self.ext=ws+'\\'+'fs'+'\\'+'extract.tif' 
        self.size="3 meters" 
        self.value="VALUE>=5"
        self.xy_tol='2 meters' 
    def inchm(self):
        print 'generating the local maxima' 
        if len(listchm)>1:
            print 'must only be one raster inside the working directory'
            os.system('pause') 
        else:
            pass 
        spc=3
        arcpy.CheckOutExtension('Spatial')
        sql=self.value
        ext1=ExtractByAttributes(self.chm, sql)
        ext1.save(self.ext)
        fs1=FocalStatistics(self.ext, NbrRectangle(spc, spc,"CELL"),"MAXIMUM", "NODATA") 
        fs1.save(self.fs)
        
        rascalc=Con(Raster(self.ext)==Raster(self.fs),Raster(self.ext))
        rascalc.save(self.rc) 
        arcpy.CheckInExtension('Spatial') 
        arcpy.RasterToPoint_conversion(self.rc, self.pt, '#') 
        arcpy.Integrate_management(self.pt,self.xy_tol)
    def curv_pts(self):
        print 'generating negative profile curvature' 
        arcpy.CreateThiessenPolygons_analysis(self.pt, self.thie,"ALL")
        arcpy.CheckOutExtension('3D')
        arcpy.Slope_3d(self.ext,self.slope, "DEGREE",1) 
        arcpy.Curvature_3d (self.slope,self.curv, 1, self.prof,"#") 
        arcpy.CheckInExtension('3D') 
        arcpy.RasterToPoint_conversion(self.prof, self.prof1, '#')
        arcpy.Select_analysis(self.prof1,self.rtpprof,where_clause="""" GRID_CODE" < 0""")
        arcpy.Clip_analysis(self.rtpprof,self.thie,self.clip)
        arcpy.Intersect_analysis([self.thie,self.clip],self.int, "ALL","","INPUT")
        arcpy.Dissolve_management(self.int,self.diss, 'FID_thie','#', "MULTI_PART","DISSOLVE_LINES")
    def smooth1(self):
        print 'smoothing polygons'
        fc3=self.diss
        field3="FID_thie" 
        cursor3=arcpy.SearchCursor(fc3) 
        x=0
        for row3 in cursor3:
            x+=1
            row3.getValue(field3) 
            arcpy.MakeFeatureLayer_management(fc3, "lyr") 
            arcpy.SelectLayerByAttribute_management("lyr","NEW_SELECTION","FID_thie="+str(row3.getValue(field3)))
 
            itername=string.zfill(x,5)+'.shp'
            print str(x)+' '+'crowns created!' 
            arcpy.AggregatePoints_cartography('lyr', self.aggre+itername,self.size) 
            CA.SmoothPolygon(self.aggre+itername, self.smooth+itername, "PAEK", 3) 
            
    def append(self):
        print 'appending shapefiles'
        utm=arcpy.SpatialReference("WGS 1984 UTM Zone 51N")
        arcpy.CreateFeatureclass_management(ws, "POLYGON", "#", "DISABLED","DISABLED", utm) 
        env.workspace=self.add 
        listindv=arcpy.ListFeatureClasses() 
        arcpy.Append_management(listindv,"NO_TEST","#","#") 
        print 'Done!'
c=crown() 
c.inchm() 
c.curv_pts() 
c.smooth1() 
c.append()