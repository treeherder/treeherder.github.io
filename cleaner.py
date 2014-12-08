from pykml import parser
from decimal import Decimal
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import ATOM_ElementMaker as ATOM
from lxml import etree, objectify
file_object =  open("wifi.kml", "r")
file_string = file_object.read()
tree_root = parser.fromstring(file_string)
#setup .kml template for clean file
#focus on fidelity

new_root = KML.kml(
        KML.Document(
            KML.name(tree_root.Document.name.text+"--clean--" )
            )
        )
for folder_idx in xrange(len(tree_root.Document.Folder)-1): #telly folders
  fldr = KML.Folder(KML.name(tree_root.Document.Folder[folder_idx].name.text))
  #print len(tree_root.Document.Folder[folder_idx].Placemark)  #debugging
  for place_mark_idx in xrange(len(tree_root.Document.Folder[folder_idx].Placemark)-1):#iterate over places
    (lng, lat) = (tree_root.Document.Folder[folder_idx].Placemark[place_mark_idx].Point.coordinates.text.split(","))
    if (Decimal(lat) > 0): #convert to useful numbers and filter bad results
      pm = KML.Placemark(
         KML.name(tree_root.Document.Folder[folder_idx].Placemark[place_mark_idx].name.text),
         KML.Point(
         KML.coordinates(tree_root.Document.Folder[folder_idx].Placemark[place_mark_idx].Point.coordinates.text)
           )
         )
    fldr.append(pm)
  #print fldr.name.text
  #for plmk in xrange(len(fldr.Placemark)):
   #print fldr.Placemark[plmk].Point.coordinates.text
  new_root.append(fldr)

print etree.tostring(new_root, pretty_print=True)
