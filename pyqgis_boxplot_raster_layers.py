# References
# https://courses.spatialthoughts.com/pyqgis-masterclass.html
# https://docs.qgis.org/3.34/en/docs/pyqgis_developer_cookbook/cheat_sheet.html
# Before running the script, QGIS must have some loaded raster layers.

import matplotlib.pyplot as plt

## Allow the user to select which raster to analyse. Drop-down menu.
raster_dict = {}
for layer in QgsProject.instance().mapLayers().values():
    if isinstance(layer, QgsRasterLayer):
        raster_dict.update({layer.name(): layer.dataProvider().dataSourceUri()}) # dictionary with the name and path of the raster layers

rasterToolbar = iface.addToolBar('Raster Selector')
label = QLabel('Select raster layer: ', parent = rasterToolbar)

rasterSelector = QComboBox(parent = rasterToolbar)
for i in range(len(raster_dict)):
    rasterSelector.addItem(list(raster_dict.keys())[i])
rasterSelector.setCurrentIndex(-1)

button = QPushButton('Boxplot!', parent = rasterToolbar)

rasterToolbar.addWidget(label)
rasterToolbar.addWidget(rasterSelector)
rasterToolbar.addWidget(button)

def raster_stats(raster_name):
    raster_name = rasterSelector.currentText()
    
    if raster_name == '':
        iface.messageBar().pushCritical('Alert', 'Please select a raster layer.')
        raise Exception('Error: No raster layer selected in the comboBox.')
    else:
        iface.messageBar().pushInfo('Selected Raster', raster_name)
    
    ## Verifies if a layer and geometry is selected
    ## If yes, it is used in the process. Otherwise, it uses the map extent.
    layer = iface.activeLayer()
    
    if isinstance(layer, QgsVectorLayer):
        num_geom_selected = len(layer.selectedFeatures())
    else:
        num_geom_selected = 0

    if layer == None or num_geom_selected == 0:
        me_str = iface.mapCanvas().extent().asPolygon()
        limit = QgsGeometry.fromWkt('POLYGON((' + me_str + '))') #QgsGeometry
        iface.messageBar().pushInfo('Active Layer', 'Map extent selected as active layer.')
    else:
        f = layer.selectedFeatures()[0]
        limit = f.geometry() # QgsGeometry
        iface.messageBar().pushInfo('Active Layer', 'First selected geometry from active layer used.')
    
    ## Creatae a memory layer to use later as limit...
    limit_layer = QgsVectorLayer('Polygon?crs=epsg:4326', 'limit_layer', 'memory')
    dpr = limit_layer.dataProvider()
    plg = QgsFeature()
    plg.setGeometry(limit)
    dpr.addFeatures([plg])
    limit_layer.updateExtents()
    #QgsProject.instance().addMapLayers([limit_layer]) # If you want to add this layer to the project, uncomment this line.
    
    # Calling processing algorithms.
    input = limit_layer # A shapefile
    input_raster = raster_dict[raster_name] # A raster file
    
    # Raster summary.
    #data_info = {'INPUT': input,'INPUT_RASTER': input_raster,'RASTER_BAND':1,'COLUMN_PREFIX':'_','STATISTICS':[2,3,4,5,6],'OUTPUT':'TEMPORARY_OUTPUT'}
    
    #summary = processing.run("native:zonalstatisticsfb", data_info)
    #QgsProject.instance().addMapLayer(summary['OUTPUT'])
    
    # Clip raster
    rst_clip = processing.run("gdal:cliprasterbymasklayer", {'INPUT': input_raster, 'MASK':input, 'SOURCE_CRS':None, 'TARGET_CRS':None, 'TARGET_EXTENT':None, 'NODATA':None, 'ALPHA_BAND':False, 'CROP_TO_CUTLINE':True, 'KEEP_RESOLUTION':False, 'SET_RESOLUTION':False, 'X_RESOLUTION':None, 'Y_RESOLUTION':None, 'MULTITHREADING':False, 'OPTIONS':'', 'DATA_TYPE':0, 'EXTRA':'', 'OUTPUT':'TEMPORARY_OUTPUT'})
    
    # Convert pixels values to points with values
    px_values = processing.run("native:pixelstopoints", {'INPUT_RASTER': rst_clip['OUTPUT'], 'RASTER_BAND':1, 'FIELD_NAME': 'VALUE', 'OUTPUT':'TEMPORARY_OUTPUT'})
    #QgsProject.instance().addMapLayer(px_values['OUTPUT']) # If you want to add this layer to the project, uncomment this line.
    
    ## Generating the boxplot
    px_layer = px_values['OUTPUT'].getFeatures()
    
    nm_feat = px_values['OUTPUT'].featureCount()
    points_limit = 1000
    if nm_feat > points_limit:
        mbox = QMessageBox()
        mbox.setText('There are more than ' + str(points_limit) + ' points on the layer. This might get things slower. Do you want to continue?')
        mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        mbox_result = mbox.exec()
        
        if mbox_result == QMessageBox.Ok:
            pass
        elif mbox_result == QMessageBox.Cancel:
            return
        else:
            pass
    
    rst_data = []
    for i in px_layer:
        data = i.attributes()
        rst_data.append(data[0])
        
    #https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.boxplot.html
    fig, ax = plt.subplots(figsize=(6,6))
    bplot = ax.boxplot(rst_data)
    plt.show()
        
#rasterSelector.currentTextChanged.connect(raster_stats)
button.clicked.connect(raster_stats)
