#!/bin/bash

source /curate/env.sh

rm -f $metadata_json
rm -f $success_file
rm -f $error_file

mkdir -p $metadata_dir
mkdir -p $log_dir

python /curate/parseCsvToJson.py $input_dir $metadata_json &> $tmp_file
if [[ "$?" -eq 0 ]]
  then 
    touch $success_file
    echo  "Successfully finished csv parsing"
    echo "success" > $success_file
    chmod 777 $success_file
    chmod 777 $metadata_json
  else 
    touch $error_file
    echo  "Failed csv parsing"
    cat $tmp_file >> $error_file
    chmod 777 $error_file
fi

rm -f $tmp_file