#!/bin/bash

# specify the output filename and path
output_file="./combined-LTCUSDT.csv"


# get a list of all CSV files in the directory
csv_files=$(ls ./LTCUSDT-*.csv)

# create the header row for the output file
header="id,price,qty,quote_qty,time,is_buyer_maker,is_best_match"

# write the header row to the output file
echo $header > $output_file

# loop through all CSV files (excluding the header row) and append them to the output file
for csv in $csv_files
do
  tail -n +2 $csv | sed '/^$/d' >> $output_file
done

echo "CSV files combined successfully!"