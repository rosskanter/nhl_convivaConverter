#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# convivaConverter.py v2 - Re-formats BAMTECH Conviva Data for Amazon quicksight
# Written by Ross Kanter 2018


import csv, os, glob, re, shutil, sys
import numpy as np
import pandas as pd



os.chdir('./ConvivaData/')

# Loop through every CSV file in the current working directory.
for csvFilename in os.listdir('.'):
    if not csvFilename.endswith('.csv'):
        continue # skip non-csv files

    print('Slicing ' + csvFilename + '...')
    # Read the CSV file skipping unnecessary rows
    csvRows = []
    with open(csvFilename) as csvFileObj:
        readerObj = csv.reader(csvFileObj)
        for row in readerObj:
            if readerObj.line_num <= 11 or len(row) < 2:
                continue # skip first 12 rows
            csvRows.append(row)
            
                
       

        # Organize into 3 separate lists representing sections of data on conviva export
        table_1 = []
        for row in csvRows[:289]:
            if row:
                table_1.append(row)

        table_2 = []
        for row in csvRows[289:578]:
            if row:
                table_2.append(row)

        table_3 = []
        for row in csvRows[578:]:
            if row:
                table_3.append(row)

# Make 3 pd data frames for each list and remove the extra time columns
    df_1 = pd.DataFrame(table_1)
    df_2 = pd.DataFrame(table_2).drop(0, axis=1)
    df_3 = pd.DataFrame(table_3).drop(0, axis=1)
    print('Merging Files into QuicksightReady file')

# Combine the three data frames by column, removing excess date characters from time, and write the columns to a new CSV
    combined_csv = pd.concat([df_1, df_2, df_3], ignore_index = True, axis = 1)
    combined_csv = combined_csv.replace('\w\w\w\s\d\d\s\d\d\d\d', '', regex=True)
    combined_csv.to_csv("./QuicksightReady.csv", index=False, header=False)
    os.rename("./QuicksightReady.csv", "Quicksight_" + csvFilename)


    
   
