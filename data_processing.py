#not tested yet
import csv
import hashlib
import pandas as pd
import csv
import datetime
import os
import pytz
import re
import mysql.connector
from mysql.connector import Error


class TimeOps:

    def convert_string_to_datetime_type:
        #2023-02-01T14:03:43.000+00:00
        date_string = "2023-03-27 10:30:00"
        date_format = "%Y-%m-%d %H:%M:%S"
        datetime_object = datetime.datetime.strptime(date_string, date_format)
        print(datetime_object)

    def convert_epoch_time_to_string:
        epoch_time = 1616963236   # Replace with your epoch time
        date_string = datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S')
        date_obj = datetime.datetime.fromtimestamp(epoch_time)
        print(date_string)
        print(date_obj)

    def date_format_timezone(hours, mins):
        # Define the datetime string and the timezone it's in
        dt_string = '2022-04-01 12:00:00' #if your datetime string does not fit this format try using regex to replace it
        #2023-02-01T14:03:43.000+00:00
        #get rid of the T and everything after and including the .
        #text = '2023-02-01T14:03:43.000+00:00'
        #pattern = r'(.*T.*)\..*'
        #match = re.match(pattern, text)
        #if match:
        #    datetime = match.group(1)
        #    print(datetime)
        #else:
        #    print('No match found')
        from_tz = pytz.timezone('US/Pacific')

        # Convert the string to a datetime object with timezone information
        dt = datetime.datetime.strptime(dt_string, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_tz)

        # Convert the datetime object to a different timezone
        to_tz = pytz.timezone('Asia/Tokyo')
        converted_dt = dt.astimezone(to_tz)

        # Print the converted datetime object
        print(converted_dt)

    def date_trunc(hours, mins):
        #convert to string
        #truncate string using regex
        pass

def import_csv_to_sql(filepath):
    
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database'
        )

        # Create a new cursor object
        cursor = connection.cursor()

        # Specify the path to your CSV file
        csv_file = '/path/to/csv/file.csv'

        # Open the CSV file and read the contents
        with open(csv_file, 'r') as file:
            csv_data = file.read()

        # Execute the MySQL LOAD DATA statement
        query = """
            LOAD DATA INFILE '{}'
            INTO TABLE your_table_name
            FIELDS TERMINATED BY ','
            ENCLOSED BY '"'
            LINES TERMINATED BY '\n'
            IGNORE 1 ROWS
        """.format(csv_file)
        cursor.execute(query)

        # Commit the changes to the database
        connection.commit()

        print('CSV data successfully imported into MySQL')

    except Error as e:
        print('Error:', e)

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print('Database connection closed')

def md5_column(filepath, column_name):
    csv_file = pd.read_csv(filepath)

    md5_hash = []

    for row in csv_file[str(column_name)]:
        md5_hash.append(hashlib.md5(str(row).encode('utf-8')).hexdigest())

    csv_file['md5-hash'] = md5_hash
    csv_file.to_csv('output.csv', index=False)


def find_duplicates_in_column(filepath, column_name):
    df = pd.read_csv(filepath)

    seen = {}
    dupes = []
    unique = []

    for row in df.index:
        if df.loc[row, str(column_name)] not in seen:
            seen[df.loc[row, str(column_name)]] = 1
            unique.append((row, df.loc[x, str(column_name)])
        else:
            if seen[df.loc[row, str(column_name)]] == 1 or seen[df.loc[row, str(column_name)]] > 1:
                dupes.append((row, df.loc[row, str(column_name)]))
                seen[df.loc[row, str(column_name)]] += 1

    with open('processed_csv_unique', 'a') as unique_csv, open('process_csv_duplicates', 'a') as duplicate_csv:
        unique_csv_writer = csv.writer(unique_csv, delimiter=',')
        duplicate_csv_writer = csv.writer(duplicate_csv, delimiter=',')

        for data in unique:
            unique_csv_writer.writerow([data])

        for dupe in dupes:
            duplicate_csv_writer.writerow([dupe])


def group_by_sum(filepath, group_by_column_names, sum_column):

    with open(filepath, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        results = {}

        for row in reader:
            sum_column_value = float(row[sum_column])
            data = []
            
            for column in group_by_column_names:
                data.append(row[column])

            key = tuple(data)

            if data in result:
                result[key] += sum_column_value
            else
                result[key] = sum_column_value

    with open('process_csv_group_by_sum', 'a') as process_csv_group_by_sum:
        process_csv_group_by_sum_writer = csv.writer(process_csv_group_by_sum, delimiter=',')
        headers = group_by_column_names.append(f"Sum of {sum_colum}")
        process_csv_group_by_sum_writer.writerow(headers)

        for keytuple, value in result.items():
            row_data = []
            for index in range(len(keytuple)):
                row_data.append(keytuple[range])
            row_data.append(value)

        process_csv_group_by_sum_writer.writerow(row_data)


def count(filepath, group_by_column_names):

    with open(filepath, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        results = {}

        for row in reader:
            data = []
            
            for column in group_by_column_names:
                data.append(row[column])

            key = tuple(data)

            if data in result:
                result[key] += 1
            else
                result[key] = 1

    with open('process_csv_group_by_sum', 'a') as process_csv_group_by_sum:
        process_csv_group_by_sum_writer = csv.writer(process_csv_group_by_sum, delimiter=',')
        headers = group_by_column_names.append(f"Sum of {sum_colum}")
        process_csv_group_by_sum_writer.writerow(headers)

        for keytuple, value in result.items():
            row_data = []
            for index in range(len(keytuple)):
                row_data.append(keytuple[range])
            row_data.append(value)

        process_csv_group_by_sum_writer.writerow(row_data)

def count_distinct(filepath, group_by_column_names, count_distinct_column):

    with open(filepath, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        results = {}
        seen = {}

        for row in reader:
            data = []
            
            for column in group_by_column_names:
                data.append(row[column])

            key = tuple(data)

            if seen[count_distinct_column] == 1 or seen[count_distinct_column] > 1:
                seen[count_distinct_column] +=1
            if seen[count_distinct_column] not in seen:
                seen[count_distinct_column] = 1
                result[key] += 1
        
    with open('process_csv_group_by_count_distinct', 'a') as process_csv_group_by_count_distinct:
        process_csv_group_by_count_distnct_writer = csv.writer(process_csv_group_by_count_distinct, delimiter=',')
        headers = group_by_column_names.append(f"count of distinct {count_distinct_column}")
        process_csv_group_by_sum_writer.writerow(headers)

        for keytuple, value in result.items():
            write_row_data = []
            for index in range(len(keytuple)):
                write_row_data.append(keytuple[range])
            write_row_data.append(value)

        process_csv_group_by_sum_writer.writerow(write_row_data)




