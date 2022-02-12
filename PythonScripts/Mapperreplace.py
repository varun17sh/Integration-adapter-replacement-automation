import os 
import re
from xml.dom import minidom
import Variables as c

dir_path = os.path.dirname(os.path.realpath(__file__))

filepath = 'D:/Integration archives/PythonScripts/InsertIntoTable_REQUEST.jca'

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

changeJCAFileProperties(filepath, c.ATPADAPTERJCAFILE)