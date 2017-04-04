import csv
import read_server_log

def read(input_file):
    with open(input_file, 'rb') as f_input:
        csv_input = csv.reader(f_input, delimiter=' ')
        data = []
        for row in csv_input:
            log_line = read_server_log.ServerLog(row)
            data.append(log_line)
    return data
