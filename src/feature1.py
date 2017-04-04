import base_feature
import collections
import csv
import read_server_log

class FindMostActive(base_feature.BaseFeature):

    def __init__(self, input_data, output_file, k=10):
        super(FindMostActive, self).__init__(input_data, output_file)
        self.hosts_to_hits = collections.Counter()
        self.k = k

    def _data_to_string(self, line):
        return line[0]+","+str(line[1])

    def _process_input(self):
        for log_line in self.server_log:
            self.hosts_to_hits[log_line.host] = self.hosts_to_hits.get(log_line.host, 0) + 1

    def parse(self):
        self._process_input()
        output = self._filter_top_k(self.hosts_to_hits, self.k)
        output.sort(key=lambda x: x[0]) # resolve ties by putting hosts in lexicographic order
        output.sort(key=lambda x: x[1], reverse=True) # re-sort by frequency, descending
        self._write_output(output, self._data_to_string)
        