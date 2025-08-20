# %%
import csv 
import pandas as pd
import pathlib
import os

# %%
oshwa_data = "./Data/Raw/oshwa/oshwa_raw.csv"
cleaned_data = 'oshwa_clean.csv'

# %%
allowed_domains = ["github.com", "gitlab.com", "zenodo", "osf.io"]

with open(oshwa_data, 'r', newline='') as infile, \
     open(cleaned_data, 'w', newline='') as outfile:
    
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow(header)

    link_column_index = header.index("documentationUrl") #need to change based on the platform

    for row in reader:
        link = row[link_column_index]

        if any(domain in link for domain in allowed_domains):
            writer.writerow(row)



