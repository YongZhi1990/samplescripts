import csv
import hashlib
import pandas as pd

csv_file = pd.read_csv('number - Sheet1.csv')

md5_hash = []

for row in csv_file['number']:
    md5_hash.append(hashlib.md5(str(row).encode('utf-8')).hexdigest())

csv_file['md5-hash'] = md5_hash

csv_file.to_csv('output.csv', index=False)
