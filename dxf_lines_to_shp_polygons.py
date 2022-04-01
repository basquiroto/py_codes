import os
from qgis import processing

# Convert DWG files to DXF with ODA File Converter and save them in path
path = "C:/Users/ferna/Desktop/teste/"
crs = QgsCoordinateReferenceSystem("EPSG:31982")

list_files = os.listdir(path)
list_final = []
err_layers = []

for i in list_files:
    name = i[:-4]
    file = i + "|layername=entities|geometrytype=LineStringZ"
    layer = QgsVectorLayer(path+file, name, 'ogr')
    layer.setCrs(crs)

    # Save selected features
    processing.run("qgis:selectbyexpression", {'INPUT': layer,'EXPRESSION':'"Layer" = \'LIMIT\' or  "Layer" = \'LIMITS\''})
    #layer.selectByExpression(u'"Layer" = \'LIMITS\'') # This works, but I wasn't able save it as temporary output
    
    if layer.wkbType() != 2 and layer.wkbType() != 1002: # 2: LineString, 1002: LineStringZ
        err_layers.append(i)
        continue
    
    layer2 = processing.run('qgis:saveselectedfeatures', {"INPUT": layer, "OUTPUT": "TEMPORARY_OUTPUT"})["OUTPUT"]
    
# uncomment if using layer.selectByExpression() instead of processing.run("qgis:selectbyexpression"
#    limit_ln = name + "_line.gpkg"
#    QgsVectorFileWriter.writeAsVectorFormat(layer, path+limit_ln,
#                                            'utf-8', layer.crs(),
#                                            "GPKG", onlySelected=True)
#    layer2 = QgsVectorLayer(path+limit_ln, name  + '_ln', 'ogr')

    # Convert to polygon
    limits = processing.run("qgis:linestopolygons", {'INPUT': layer2, 'OUTPUT':'TEMPORARY_OUTPUT'})["OUTPUT"]
    
    if len(limits) == 0:
        print('It was not possible to convert file: ' + i)
        err_layers.append(i)
        continue
        
    list_final.append(limits)
    del(layer2)

limits_final = processing.run("qgis:mergevectorlayers", {"LAYERS": list_final, "OUTPUT": path+"limits_Agg.gpkg"})["OUTPUT"]

limits_agg = QgsVectorLayer(limits_final, "Limits United", 'ogr')
QgsProject.instance().addMapLayer(limits_agg)

print('Files not loaded: ', err_layers)
