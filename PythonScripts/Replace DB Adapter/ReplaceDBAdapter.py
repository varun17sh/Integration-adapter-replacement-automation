import os
import shutil
import re
import zipfile
from xml.dom import minidom
import Variables as c

namespaceOld = "http://xmlns.oracle.com/cloud/adapter/database"
namespaceNew = "http://xmlns.oracle.com/cloud/adapter/atpdatabase"
ics_project_attributes = ':atpdatabase'
dir_path = os.path.dirname(os.path.realpath(__file__)) 

### -------- Function to replace a particular string in file -------------
def changeString(filename, substringOld, substringNew):
    with open(filename, 'r+') as f:
        text = f.read()
        if substringOld in text :
            text = re.sub(substringOld, substringNew, text)
            f.seek(0)
            #print(text)
            f.write(text)
            f.truncate() 


### -------- Function to Extract zip into a target directory ------------
def extractIARFiles(path_to_zip_file):
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall('targetdir')

# ------------ Function to Delete DB adapter configuration file and replace with ATP -----------
def replaceDBAdapterWithATP():
    FileToBeRemoved = c.DATABASEADAPTERNAME + '.xml'
    os.remove(dir_path + '/targetdir/icspackage/appinstances/' + FileToBeRemoved)
    tail = os.path.split(c.ATPADAPTERLOCATION)
    shutil.copy(c.ATPADAPTERLOCATION, dir_path + '/targetdir/icspackage/appinstances/' + tail[1])

##------------- Function to Update project.xml ----------------------##
def updateProjectXML(zipName):
    filepath = dir_path + '/targetdir/icspackage/project/' + zipName.rpartition('.')[0] + '/PROJECT-INF/project.xml'
    #print(filepath)
    substring = '<code>' + c.DATABASEADAPTERNAME + '</code>'
    newstring = '<code>' + c.ATPADAPTERNAME + '</code>'

    changeString(filepath, substring, newstring)
    changeString(filepath, namespaceOld, namespaceNew)

def updateJCAFilesAndNamespaces(zipName):
    prjctdir = dir_path + '/targetdir/icspackage/project/' + zipName.rpartition('.')[0]
    changeString(prjctdir + '/ics_project_attributes.properties', ':database', ics_project_attributes) 
    for subdir, dirs, files in os.walk(prjctdir + '/resources'):
        for file in files:
            #print(os.path.join(subdir, file))
            if file.rpartition('.')[2] == 'jca':
                changeJCAFileProperties(os.path.join(subdir, file), c.ATPADAPTERJCAFILE)
            
            changeString(os.path.join(subdir, file), namespaceOld, namespaceNew)

def zipFileAndExport(zipName):
    shutil.make_archive(c.EXTRACTTODIRECTORY + '/' + zipName, 'zip', dir_path + '/targetdir') 
    shutil.rmtree(dir_path + '/targetdir')
    os.rename(c.EXTRACTTODIRECTORY + '/' + zipName + '.zip', c.EXTRACTTODIRECTORY + '/' + zipName)

def changeJCAFileProperties(jcaFilePath, ATPJCAFILE):
    ## ------ Check if jca file is for database adapter ----------------
    mydoc = minidom.parse(jcaFilePath)
    items = mydoc.getElementsByTagName('adapter-config')

    if items[0].attributes['adapter'].value == "database":
        ## ------ Change adapter type to atp --------------------
        items[0].attributes['adapter'].value = 'atpdatabase'   

        ## ------ Clone connection factory from ATP JCA file ------------------------------
        connectionStringATP = minidom.parse(ATPJCAFILE)
        atpAdapterConn = connectionStringATP.getElementsByTagName('connection-factory')[0]
        cloneNode = atpAdapterConn.cloneNode(deep=True)

        # Change current JCA file properties
        connFactNode = mydoc.getElementsByTagName('connection-factory')
        endPointNode = mydoc.getElementsByTagName('endpoint-interaction')

        # remove old connection-factory
        for i in connFactNode:  
            x = i.parentNode 
            x.removeChild( i )
        # remove endpoint 
        for i in endPointNode:
            x = i.parentNode
            x.removeChild(i)

        # remove on-prem and agent attribute from endpoint-interaction
        if endPointNode[0].hasAttribute('agent'):
            endPointNode[0].removeAttribute('agent')
        if endPointNode[0].hasAttribute('onpremise'):
            endPointNode[0].removeAttribute('onpremise')

        # add both connfactory and endpoint interaction back to xml
        mydoc.firstChild.appendChild(cloneNode)
        items[0].appendChild(endPointNode[0])

        # write the file
        f = open(jcaFilePath, "w")
        f.write(mydoc.getElementsByTagName('adapter-config')[0].toxml())
        f.close()

def main():
    for filename in os.listdir(c.ZIPDIRECTORY):
        if filename.endswith(".iar"):
            print(os.path.join(filename))
            extractIARFiles(os.path.join(c.ZIPDIRECTORY, filename))
            replaceDBAdapterWithATP()
            updateProjectXML(filename)
            updateJCAFilesAndNamespaces(filename)
            zipFileAndExport(filename)
        else:
            continue    

if __name__ == "__main__":
    main()
