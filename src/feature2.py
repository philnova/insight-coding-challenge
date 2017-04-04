import base_feature
import collections
import csv
import read_server_log

class FindMostIntensiveResources(base_feature.BaseFeature):

    def __init__(self, input_data, output_file, k=10):
        super(FindMostIntensiveResources, self).__init__(input_data, output_file)
        self.resources_to_bandwidth = collections.Counter()
        self.k = k

    def _data_to_string(self, line):
        return line[0]

    def _process_input(self):
        for log_line in self.server_log:
            self.resources_to_bandwidth[log_line.resource] = self.resources_to_bandwidth.get(log_line.resource, 0) + log_line.bytes

    def parse(self):
        self._process_input()
        output = self._filter_top_k(self.resources_to_bandwidth, self.k)
        output.sort(key=lambda x: x[0]) # resolve ties by putting hosts in lexicographic order
        output.sort(key=lambda x: x[1], reverse=True) # re-sort by frequency, descending
        self._write_output(output, self._data_to_string)
        