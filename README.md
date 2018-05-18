# FUNKTION:
	
Dieses Tool konvertiert ein Shapfile mit einer EPSG Projektion zu 
einem .geojson Format im World Geodetic System WGS84 / EPSG:4326.
Letzteres ist das gängige Format mit Längen- Breitenkoordinaten und kann zB.
von Google Maps gelesen werden.

Wenn der EPSG Code unbekannt ist, aber eine .prj Datei vorliegt, kann er auf
der folgenden Website ermittelt werden:
http://prj2epsg.org/search

Ansonten erkennt die Website http://mygeodata.cloud/converter aus den .shp, .dbf 
und .shx Dateien die Projektion und EPSG Code (nicht immer fehlerfrei).

Bisher verwendete Codes:
- EPSG:31467 -> DHDN / 3-degree Gauss-Kruger zone 3 
- EPSG:32632 -> WGS 84 / UTM zone 32N
- default:EPSG:4326 -> WGS 84  World

# VERWENDUNG:
	
	python converter.py <inputFile> <outputFile> [EPSG Projektions Code]

Es kann <file>.shp oder auch nur <file> (ohne Dateiendung) verwendet werden.
Die .shp und .dbf (und mehr) Dateien mit selbem Namen im selben Verzeichnis
werden mit gelesen.

# INSTALLATION:
	
Benötigt wird: 

	pyshp
	pyproj

Zu installieren mit:

	pip install pyshp
	pip install pyproj

# TROUBLESHOOTING:
	
Zur Installation von pyproj wird unter Windows Visual C++14 benötigt. Dies
lässt sich umgehen indem man eine Windows Binary runterläd und diese direkt
installiert.

Quelle: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyproj

Dann: 

    pip install pyproj‑1.9.5.1‑cp36‑cp36m‑win_amd64.whl

Beachte:
Das cp** steht für die Python version. Also cp36 für Python 3.6 usw.


# PROBLEME / ERWEITERUNGEN:
	
- Umlaute in Attributsnamen können momentan nicht gelesen werden.
- Der Projektionscode wird noch nicht automatisch erkannt.


### Guter .geojson viewer:
	geojsonviewer.nsspot.net