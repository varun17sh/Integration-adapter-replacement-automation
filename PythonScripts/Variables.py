#####################################################################################
#           Define these variables before running the script
#####################################################################################
# 
#     DATABASEADAPTERNAME    =    The identifier of the current database adapter
#     ATPADAPTERNAME         =    Identifier of the new ATP Adapter 
#     ATPADAPTERLOCATION     =    the path to the new ATP adapter config file (~.xml)
#     ATPADAPTERJCAFILE      =    Path to the JCA file for the new ATP adapter. Can be found in the new exported integration made with ATP adapter
#     ZIPDIRECTORY           =    Path to the directory where all the archive files(.iar) are placed. With the folder name as the last element in path e.g. e.g. D:/mydir/temp
#     EXTRACTTODIRECTORY     =    Path to the new directory where the script will place the updated archives. Should end with the folder name e.g. D:/mydir/temp
#
####################################################################################

DATABASEADAPTERNAME = 'TESTATPFROMDB'
ATPADAPTERNAME = 'ATPSHAREDINFRA'

ATPADAPTERLOCATION = 'D:/Integration archives/TESTATPSHARED_01.00.0000/icspackage/appinstances/ATPSHAREDINFRA.xml'
ATPADAPTERJCAFILE = 'D:/Integration archives/PythonScripts/TestATP_S_REQUEST.jca'

ZIPDIRECTORY = 'D:/Integration archives/PythonScripts/IARFILES'
EXTRACTTODIRECTORY = 'D:/Integration archives/PythonScripts/NewFolder'