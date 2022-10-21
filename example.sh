#!/bin/bash

source /curate/env.sh

rm -f $dm_json
rm -f $error_file
rm -f $success_file



#############################################
#       Check file existance
#############################################

# check files : CONTCAR
if [ ! -f $contcar_file ]; then
   echo "CONTCAR file does not exist" >> $error_file
   exit -1
fi

# check files : INCAR
if [ ! -f $incar_file ]; then
   echo "INCAR file does not exist" >> $error_file
   exit -1
fi

# check files : OUTCAR or vasprun.xml
if [ ! -f $outcar_file ] && [ ! -f $xml_file ]; then
   echo "OUTCAR or vasprun.xml file does not exist" >> $error_file
   exit -1
fi


#############################################
#       Annotate basic Metadata
#############################################
basic_json=$root_dir/basic.json
$root_dir/annotate.sh $basic_json
if [ $? -ne 0 ]; then
   echo "============================" >> $error_file
   echo "Basic Metadata Annoation failure " >> $error_file
   echo "============================" >> $error_file
   cat $tmp_file >> $error_file
   exit -1
fi

#############################################
#       Dos
#############################################
#if [ -f $xml_file ]; then
#   $root_dir/dos_plot.py $input_dir $dos_file &> $tmp_file
#   if [ -z $dos_file ]; then
#       echo "============================" >> $error_file
#       echo "Dos diagram creation failure." >> $error_file
#       echo "============================" >> $error_file
#       cat $tmp_file >> $error_file
#       exit -1
#   fi
#fi



#############################################
#       Annotate battery Metadata
#############################################
battery_json=$root_dir/battery.json
$root_dir/battery.py $uploaded_dir $battery_json &> $tmp_file
if [ ! -f $battery_json ]; then
   echo "============================" >> $error_file
   echo "Battery Metadata Extraction Failure." >> $error_file
   echo "============================" >> $error_file
   cat $tmp_file >> $error_file
   exit -1
fi


#############################################
#       Integrate Metadata
#############################################
$root_dir/integ2.py $basic_json $battery_json $dm_json &> $tmp_file
if [ ! -f $dm_json ]; then
   echo "============================" >> $error_file
   echo "Metadata Integration Failure." >> $error_file
   echo "============================" >> $error_file
   cat $tmp_file >> $error_file
   exit -1
fi

#############################################
#      Finalize
#############################################
rm -f $basic_json
rm -f $battery_json
rm -f $tmp_file

echo  "Successfully finished VASP Annotation"
echo "success" > $success_file
