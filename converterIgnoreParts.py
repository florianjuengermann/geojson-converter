import sys
import shapefile
from pyproj import Proj, transform

if len(sys.argv) == 1:
	print("No input file provided. Usage:\n python converter.py <inputFile> <outputFile> [projection EPSG code] [encoding]")
	print("You can use 'file.shp' or just 'file' the converter will read the .shp .dbf files and so on.")
	print("Default EPSG code is 4326 (no conversion). Default encoding is cp437.")
	exit()
inFile = sys.argv[1].replace(".shp", "").replace(".dbf", "")

if len(sys.argv) == 2:
	print("No output file provided, using "+ inFile + "_output.geojson")
	outFileS = inFile +"_output.geojson"
else:
	outFileS = sys.argv[2]

if len(sys.argv) <= 3:
	proj = 4326 # Word reference frame WGS84
else:
	proj = int(sys.argv[3])

if len(sys.argv) <= 4:
	ENCODING = "cp437"#"utf-8"
else:
	ENCODING = sys.argv[4]



print("Using projection: EPSG:"+ str(proj))
print("Using encoding:", ENCODING)


sf = shapefile.Reader(inFile, encoding=ENCODING)
outFile = open(outFileS, "w+")

shapes = sf.shapes()
# check if shapes are polgons
for shape in shapes:
	if not shape.shapeType == shapefile.POLYGON:
		print("ERROR: Shape" + str(shape) + " is not POLYGON")

# attribute names
fields = sf.fields[1:] 
field_names = [field[0] for field in fields]

#projections
inProj = Proj(init=('epsg:'+str(proj)))  
outProj = Proj(init='epsg:4326') # Word reference frame WGS84

outFile.write("{\n\"type\": \"FeatureCollection\",\n\"crs\": { \"type\": \"name\", \"properties\":")
outFile.write(" { \"name\": \"urn:ogc:def:crs:OGC:1.3:CRS84\" } },\n\"features\": [\n")


shapesCount = len(sf.shapeRecords())
#shapesCount = 1

for s in range(shapesCount):
	feature = sf.shapeRecords()[s]
	print("Reading shape " + str(s+1) + " / " +str(shapesCount))
	rec = feature.record
	shape = feature.shape

	# ---------- PARAMS ------------------
	if len(rec) != len(field_names):
		print("ERROR: mismatch in feature lenghts for shape", str(feature.record))
	else:
		outFile.write("{ \"type\": \"Feature\", \"properties\": { ")
		#print(type(rec[5]))
		for i in range(len(rec)):
			outFile.write("\"" + field_names[i] + "\": ")
			
			#handeling umlaute
			if isinstance(rec[i], bytes):
				rec[i] = rec[i].decode(ENCODING, "replace")
				if "\ufffd" in rec[i]:
					rec[i] = rec[i].replace("\ufffd", "?")
					print("Unkown character in string '"+ str(rec[i])+"'. Try using a different encoding.")

			if not isinstance(rec[i], (int, float, complex)):
				outFile.write("\"" + str(rec[i]) + "\"")
			else:
				outFile.write(str(rec[i]))

			if i != len(rec) - 1:
				outFile.write(", ")

	
	# ------------ GEOMETRY ----------------

		outFile.write(" }, \"geometry\": { \"type\": \"Polygon\", \"coordinates\": [ ")

		# NOT CHECK FOR PARTS, can be used to convert a array of line segments to a polygon

		outFile.write("[ ")
		startIndex = 0
		
		endIndex = len(shape.points)
		
		startX, startY = transform(inProj,outProj,shape.points[startIndex][0], shape.points[startIndex][1])

		# add all points for this part
		for i in range(startIndex, endIndex):
			coords = shape.points[i]
			x,y = transform(inProj,outProj,coords[0],coords[1])
			outFile.write("[ " + str(x) + ", " + str(y) + " ]")

			if i != endIndex - 1:
				outFile.write(", ")

		# check if polygon is closed
		lastX, lastY = transform(inProj,outProj,shape.points[endIndex-1][0], shape.points[endIndex-1][1])
		if lastX != startX or lastY != startY:
			print("ERROR: shape start and endpoint does not match! Inserting point...")
			outFile.write(", [ " + str(startX) + ", " + str(startY) + " ]")

		outFile.write(" ]")

		outFile.write(" ] } }")

		if s != shapesCount - 1:
			outFile.write(",\n")


outFile.write("\n]\n}")
outFile.close()
print("Finished!")