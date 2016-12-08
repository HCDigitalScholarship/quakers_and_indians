import os
import re
import shutil
from lxml import etree
from html5lib.sanitizer import HTMLSanitizerMixin
from bs4 import BeautifulSoup



    
xml_file =  input( "Please insert path to XML file that you would like to convert to HTML:  ") 

"""
1 -- etree.parse(xml_file)
reads the xml file that is given as input and changes it into an ElementTree object.
This ElementTree object is an object that treats the XML file as a tree object
with oarent and child nodes. 

2 -- etree.tostring(tree)
transforms the elementtree object to a python string object. 

"""
tree = etree.parse(xml_file)  
xml_string = etree.tostring(tree)

"""
3 -- new_xml_string = xml_string[xml_string.index("</teiHeader>")+12:]
Removes all TEI-specific heading context before and including the </teiHeader>
closing tag.

4 -- new_xml_string = new_xml_string.replace("</TEI>", "")
Removes </TEI> closing tag (the opening tage was removed by the line above since
it was before the </teiHeader> closing tag.

"""
new_xml_string = xml_string[xml_string.index("</teiHeader>")+12:]
new_xml_string = new_xml_string.replace("</TEI>", "")

"""  
The four lines below take the string new_xml_string and save it to a file
with the name 'converted'+[the file name of the original xml file that was given
as input].

The string new_xml_string is a string of the original xml file without some of
the TEI specific tags that appear at the beginning and end of the original xml
file.

"""
converted_file = os.path.basename(xml_file)
text_file = open("converted_" + converted_file, "w")
text_file.write(new_xml_string)
text_file.close()

#########################################################################

"""
This section of the code first gets the path of the file created above and then
changes the file to a elementtree object.

After turning the file into an elementtree the function changeXMLtag and the
smaller for loops below, takes the xml tags in the file and changes its
format so that it resembles an html tag.

  changeXMLtag
  
  (1) for tagName in root.iter(str_tagname) -- gets all xml tags that have the same
  tag name as the input {str_tagname}
  (2) if len(tagName.items()) != 0 -- checks to see if a tag has any attributes
      if the tag hass attributes, then
      (3) tagName.attrib["key"] = "#"+ tagName.attrib["key"] -- takes the key
      attribute of the tag and adds an hash to the front of its value
  (4)-(5) for key in tagName.keys():
            tagName.attrib["href"] = tagName.attrib.pop(key) --

          changes the key attribute to a herf attribute
  (6) tagName.attrib['class'] = tagName.tag -- adds the class attribute to the
      tag and sets it to the tag name
  (7) tagName.tag = "a" -- changes the tag name to an anchor tag


"""
xml_toChange = str(os.path.realpath("converted_" + converted_file))
new_tree = etree.parse(xml_toChange)
root = new_tree.getroot()

def changeXMLtag(str_tagname):
  for tagName in root.iter(str_tagname):
    if len(tagName.attrib) != 0:
      tagName.attrib["key"] = "#"+ tagName.items()[0][1]
    for key in tagName.keys():
      tagName.attrib["href"] = tagName.attrib.pop(key)
    tagName.attrib['class'] = tagName.tag
    tagName.tag = "a"

tags_to_change = ["persName", "placeName", "orgName", "geogName"] 
for tags in tags_to_change:
    changeXMLtag(tags)
    
"""
The for loops below

  (1) takes the date xml tag and changes it to an anchor tag
  (2) takes the title xml tag and changes it to a h1 tag
  (3) takes the row xml tag and changes it to the appropriate html
      table row tag
  
"""
for date in root.iter("date"):
    date.tag = "a"

for title in root.iter("title"):
    title.tag = "h1"

for row in root.iter("row"):
    row.tag = "tr"
    
"""
The for loops below

  (1) takes the line break xml tag, changes it to the appropriate html line
      break tag and then clears the attribute of the tag
  (2) takes the cell xml tag, changes it to the appropriate html table cell
      tag and then clears the attribute of the tag
"""
for line_break in root.iter("lb"):
    line_break.tag = "br"
    line_break.attrib.clear()
    
for cell in root.iter("cell"):
    cell.tag = "td"
    cell.attrib.clear()
    
"""
The for loop below takes the xml page break tag and deletes all attributes that
is not a n (page number) attribute.
"""
for page_break in root.iter("pb"):
    for attr in page_break.attrib:
        if attr != 'n':
            del page_break.attrib[attr]

#########################################################################
            
new_tree.write(xml_toChange) #updates the changes made above in the file 
another_tree = etree.parse(xml_toChange) #parses xml file 

list_of_xml_tags = [elem.tag for elem in root.iter() if elem is not root] #gets all tags in the xml file 

for tag in list_of_xml_tags:#takes out all tags that are not approporiate html tags from the xml file except for the root, body tag and pg tag
    if tag not in HTMLSanitizerMixin.acceptable_elements and tag != "body" and tag != "pb" :
        etree.strip_tags(another_tree, tag) 
        

another_tree.write(xml_toChange)#saves the changes made to the file xml_toChange

#adds html header to xml_toChange and writes to new file, which is essentially now a html file
with open(xml_toChange, 'rb') as f, open('new_'+ converted_file,  'wb') as g:
    g.write('<!DOCTYPE html><html>{}</html>'.format(f.read()))
    
#deletes the file saved as 'converted'+converted_file from directoy because
#it is not needed anymore (can remove if you want to save this file)
os.remove(xml_toChange)

#makes a copy of the recently created file and saves as html file
xml_file = os.path.realpath('new_'+ converted_file)
html_file = xml_file[:len(xml_file)-3]+"html"
shutil.copy2(xml_file,html_file)

from page_break_csv import csv_page_break

#saves the contents of a html file to a csv where each cell is
#comprised of the content within a page break in the xml file
csv_page_break(xml_file, html_file)




