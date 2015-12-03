import xml.etree.ElementTree as ET
import os 
from lxml import etree
import lxml.etree as ET
from html5lib.sanitizer import HTMLSanitizerMixin

xml_file =  input( "Please insert path to XML file that you would like to convert to HTML:  ") 
tree = etree.parse(xml_file)
xml_string = etree.tostring(tree)


new_xml_string = xml_string[xml_string.index("</teiHeader>")+12:]
new_xml_string = new_xml_string.replace("</TEI>", "")

converted_file = os.path.basename(xml_file)
text_file = open("converted_" + converted_file, "w")
text_file.write(new_xml_string)
text_file.close()



       
xml_toChange =  input( "Please insert path to converted_xml_file.xml:  ") #path to converted_xml_file.xml  

new_tree = ET.parse(xml_toChange)
root = new_tree.getroot()

for persName in root.iter("persName"):
    if  len(persName.items()) != 0:
        persName.attrib["key"] = "#"+persName.items()[0][1]
    for key in persName.keys():
        persName.attrib["href"] = persName.attrib.pop(key)
    persName.attrib['class'] = persName.tag
    persName.tag = "a"
    
for placeName in root.iter("placeName"):
    if  len(placeName.items()) != 0:
        placeName.attrib["key"] = "#"+placeName.items()[0][1]
    for key in placeName.keys():
        placeName.attrib["href"] = placeName.attrib.pop(key)
    placeName.attrib['class'] = placeName.tag
    placeName.tag = "a"

for orgName in root.iter("orgName"):
    if  len(orgName.items()) != 0:
        orgName.attrib["key"] = "#"+orgName.items()[0][1]
    for key in orgName.keys():
        orgName.attrib["href"] = orgName.attrib.pop(key)
    orgName.attrib['class'] = orgName.tag
    orgName.tag = "a"

for geogName in root.iter("geogName"):
    if  len(geogName.items()) != 0:
        geogName.attrib["key"] = "#"+geogName.items()[0][1]
    for key in geogName.keys():
        geogName.attrib['href'] = geogName.attrib.pop(key)
    geogName.attrib['class'] = geogName.tag
    geogName.tag = "a"

for date in root.iter("date"):
    date.tag = "a"
    
for line_break in root.iter("lb"):
    line_break.tag = "br"
    line_break.attrib.clear()
    
for title in root.iter("title"):
    title.tag = "h1"

for row in root.iter("row"):
    row.tag = "tr"

for cell in root.iter("cell"):
    cell.tag = "td"
    cell.attrib.clear()
    
new_tree.write(xml_toChange)


another_tree = etree.parse(xml_toChange)
xml_string = etree.tostring(another_tree)


list_of_xml_tags = [elem.tag for elem in root.iter() if elem is not root]

for tag in list_of_xml_tags:
    if tag not in HTMLSanitizerMixin.acceptable_elements and tag != "body" and tag != "pb" :
        etree.strip_tags(another_tree, tag)
        

another_tree.write(xml_toChange)

#insert <!DOCTYPE html>
#insert html opening and closing tag

with open(xml_toChange, 'rb') as f, open('new_'+ converted_file, 'wb') as g:
    g.write('<!DOCTYPE html><html>{}</html>'.format(f.read()))




