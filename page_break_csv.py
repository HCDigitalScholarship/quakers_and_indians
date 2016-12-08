import re
import os 
from lxml import etree
from bs4 import BeautifulSoup
import csv


def csv_page_break(xml_file, html_file):
      
      #formats the html page so that it is easier to read
      soup = BeautifulSoup(open(html_file, 'rb'), "html.parser")

      """
      collects all pb tags into a list where each pb tag is given a opening
      and closing tag
      """
      page_break_loc = soup.find_all('pb')
      
      """
      the next for loop re-formats the pb tags so that they look like
      the pb tags in the xml file.
            (1) new_pb = re.sub('\</pb>$', '',str(pb)) -- removes the closing
                  pb tag
            (2) new_pb = new_pb[:-1]+"/"+new_pb[-1] -- adds a backslash to the
                  end of the string in the pb tag
      """
      new_pb_list = []
      
      for pb in page_break_loc: 
            new_pb = re.sub('\</pb>$', '',str(pb))
            new_pb = new_pb[:-1]+"/"+new_pb[-1]
            new_pb_list.append(new_pb)

            
      """
      opens the xml file, first changes it to a elementtree object and then a
      string.
      """ 
      tree = etree.parse(open(xml_file))
      xml_string = etree.tostring(tree)

      """
       The code below finds each page break in the xml file and saves the content between
       each break into separate rows in a csv so that all contents within a page
       as indicated in the xml file is saved to a row in the csv.
             (1) pb_csv_list.append(os.path.basename(xml_file)) -- the first column in the
                 csv has the name of the file that is being read
             (2) pb_csv_list.append(os.path.basename(xml_file)+"_pg_"+ str(count)) -- the second
                 column has the current page that is being read within the xml file
             (3) pb_csv_list.append(xml_string[:xml_string.find(pbs)]) -- the third column has the
                 page content
      """
      with open("csv_for_"+os.path.basename(xml_file)+".csv", 'wb') as f:
            writer = csv.writer(f)
            count = 0
            csv_list =[]
            
            for pbs in new_pb_list:
                  pb_csv_list = []
                  pb_csv_list.append(os.path.basename(xml_file))
                  pb_csv_list.append(os.path.basename(xml_file)+"_pg_"+ str(count))
                  pb_csv_list.append(xml_string[:xml_string.find(pbs)])
                  csv_list.append(pb_csv_list)
                  
                  count+=1
                  xml_string = xml_string[xml_string.find(pbs)+len(pbs):]
           

            """
            gets the remaining content in the xml page and stores it in the csv with the
            same format
            """
            pb_csv_list = []
            pb_csv_list.append(os.path.basename(xml_file))
            pb_csv_list.append(os.path.basename(xml_file)+"_pg_"+ str(count))
            pb_csv_list.append(xml_string[:xml_string.find(pbs)])
            csv_list.append(pb_csv_list)
            
            writer.writerows(csv_list)
            
            os.remove(xml_file) #removes xml_file from directoy (can delete if you want to save this file)
            os.remove(html_file) #removes html_file from directoy (can delete if you want to save file)
           
      
