<<COMMENT
This script will unzip the .iar connection file and replace the DB adapter with ATP 
    Notes:
    1. The DB adapter and the ATP adapter connection files are in the same directory
    2. This script doesn't replace mappers

COMMENT

#--------------
# Unzips all .iar files in the directory and put in a new directory with the same .iar file name
for iar in *.iar
do
  dirname=`echo $iar | sed 's/\.iar$//'`
  echo dirname
  if mkdir "$dirname"
  then
    if cd "$dirname"
    then
      unzip ../"$iar"
      cd ..
      # rm -f $zip # Uncomment to delete the original zip file
    else
      echo "Could not unpack $iar - cd failed"
    fi
  else
    echo "Could not unpack $iar - mkdir failed"
  fi
done

#----------------
# Remove db adapter config file and replace with ATP adapter congif file

# *** TO DO ***
# Replace "DB_adapter_file" with your DB adapter connection file directory name (same as .iar file name)
# Replace "TESTATPFROMDB.xml" with your DB adapter adapter configuration .xml file name
# Replace "ATP_adapter" with your ATP adapter connection file directory name (same as .iar file name)
# Replace "ATPSHAREDINFRA.xml" with your ATP adapter adapter configuration .xml file name

rm ./DB_adapter_file/icspackage/appinstances/TESTATPFROMDB.xml
cp -r ./ATP_adapter/icspackage/appinstances/ATPSHAREDINFRA.xml ./DB_adapter_file/icspackage/appinstances/ATPSHAREDINFRA.xml

#-----------------
# Replace DB adapter code "TestATPFromDB" with - ATP adapter code "ATPSharedInfra" in DB adapter project.xml

# *** TO DO ***
# Replace "TestATPFromDB" with your DB adapter code name
# Replace "ATPSharedInfra" with your ATP adapter code name (same as .iar file name)
# Replace "DB_adapter_file" with your DB adapter connection file directory name (same as .iar file name)
# Replace "TESTATPFROMDB_01.00.0000" with your DB adapter connection file directory name (same as .iar file name)

sed -i '' 's/<code>TestATPFromDB/<code>ATPSharedInfra/g' DB_adapter_file/icspackage/project/TESTATPFROMDB_01.00.0000/PROJECT-INF/project.xml

