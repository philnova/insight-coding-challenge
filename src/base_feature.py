import csv
import read_server_log

class BaseFeature(object):

    def __init__(self, server_log, output_file):
        self.server_log = server_log
        self.output_file = output_file
        self.server_log_len = len(server_log)

    def _filter_top_k(self, data, k):
        """Accepts a collections.Counter object data and a limit k.
        Returns the k largest elements in data using heapsort."""
        return data.most_common(k)

    def _write_output(self, output_data, data_to_string=str):
        """Generic function to write data from an iterable
        object into the output_file specified at construction.
        Accepts as an argument output_data, an iterable, and
        a method data_to_string, which converts each
        item in the iterable into a string representation."""
        with open(self.output_file, 'w') as f_output:
            for item in output_data:
                f_output.write(data_to_string(item)+"\n")
