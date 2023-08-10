import csv

def get_distinct_column_values(csv_filename, column_index):
    distinct_values = set()
    with open(csv_filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) > column_index:
                distinct_values.add(row[column_index])
    return list(distinct_values)


def find_max_concurrent_sessions(csv_filename, account_name_index):
    # List to store start and end times as events
    account_names = get_distinct_column_values(csv_filename, account_name_index)
    print(account_names)

    
    for name in account_names:
        with open(csv_filename, 'r') as session_data:
            _session_data = csv.reader(session_data)
            events = []
            print(events)
            for row in _session_data:
                if row[0] == name:
                    events.append((row[1], 1))  # 1 indicates session start
                    events.append((row[2], -1))  # -1 indicates session end

            events.sort()  # Sort the events based on time
            print(events)
            max_concurrent_sessions = 0
            current_concurrent_sessions = 0

            for _, event_type in events:
                current_concurrent_sessions += event_type
                max_concurrent_sessions = max(max_concurrent_sessions, current_concurrent_sessions)

            with open('result.csv', 'a') as result_filename:
                result_filename_writer = csv.writer(result_filename)
                result_filename_writer.writerow([name,max_concurrent_sessions])


find_max_concurrent_sessions('input.csv', 0)
