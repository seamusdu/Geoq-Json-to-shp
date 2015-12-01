import urllib2
import urllib


values={
         "code" : "310000",
         "region":'grid',
         "extent":[13438319.355,3408204.284,13569976.288,3546846.231],# 查询范围，必选
         "inSR":3857,
         "radius":250,
         "condition":{"pop":[0,4057]} #筛选条件, 人口栅格
         }
requestData=urllib.urlencode(values)
url=ur'http://ip/rest/services/filterservice/regionfilter' #修改IP地址
req = urllib2.Request(url,requestData)
response = urllib2.urlopen(req)  
the_page = response.read()


import json
import arcpy

ddata = json.loads(the_page)
# Obtain the geometry array
ddata1 = ddata['result']['features']

# Define a function to create polygons
def extract_geometry(ddata1):
    point = arcpy.Point()
    array = arcpy.Array()
    featureList = []
    
    for i in range(len(ddata1)):
        j = ddata1[i]
        z = j['geometry']['rings'][0][0:4]
        
        #For each coordinate pair, set the x,y properties and add to the array object.
        for coordPair in z:
            point.X = coordPair[0]
            point.Y = coordPair[1]
            array.add(point)
        array.add(array.getObject(0))
        polygon = arcpy.Polygon(array)
        array.removeAll()
        
        #Append to the list of polygon objects
        featureList.append(polygon)
        
    arcpy.CopyFeatures_management(featureList, "e:/") #保存地址

extract_geometry(ddata1)

