import csv
import read_server_log

class FileInputReader(object):
    def __init__(self, input_file):
        self.input_file = input_file
        self.data = []

    def read(self):
        with open(self.input_file, 'rb') as f_input:
            csv_input = csv.reader(f_input, delimiter=' ')
            for row in csv_input:
                log_line = read_server_log.ServerLog(row)
                self.data.append(log_line)
