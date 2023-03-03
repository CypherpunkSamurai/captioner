# A script to convert csv files to list
# 

import pandas
import argparse

parser = argparse.ArgumentParser(
    'csv_to_list',
    description='convert csv to list')
parser.add_argument('csv_file', help='csv file to convert')
parser.add_argument('txt_file', help='output file')

args = parser.parse_args()

df = pandas.read_csv(args.csv_file)
df[df.columns[0]].to_csv(args.txt_file, index=False, sep='\n')