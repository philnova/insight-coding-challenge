import base_feature
import csv
import collections
from datetime import datetime,timedelta
import read_server_log

class FindHighestTrafficWindows(base_feature.BaseFeature):

    def __init__(self, input_data, output_file, k=10, minutes_per_bucket=60):
        super(FindHighestTrafficWindows, self).__init__(input_data, output_file)
        self.time_to_requests = collections.Counter()
        #self.time_of_hits = []
        self.timezone = self.get_timezone()
        self.k = k
        self.minutes_per_bucket = minutes_per_bucket

    def get_timezone(self):
        try:
            return self.server_log[0].timezone # this assumes time zones on all logs are the same
        except:
            return "+0000"

    def _data_to_string(self, line):
        timestring, hit_count = line[0].strftime('%d/%b/%Y:%H:%M:%S'), str(line[1])
        return timestring+' '+self.timezone+','+hit_count
                
    def _sum_sliding_window(self):
        left_cutoff = self.server_log[0].timestamp
        hits_in_this_bucket = 1
        l, r = 0, 0
        max_time = self.server_log[-1].timestamp
        # Keep two pointers: l and r
        # At each tick of the loop, advance cutoff by one second
        # Then, advance l and r until they are both within the new window
        # 
        # This approach is O(max(total time in server logs in seconds, total number of logs)
        # which is linear time
        while left_cutoff <= max_time:
            while self.server_log[l].timestamp < left_cutoff:
                l += 1
                hits_in_this_bucket -= 1
            right_cutoff = left_cutoff + timedelta(minutes = self.minutes_per_bucket)
            while True:
                r += 1
                hits_in_this_bucket += 1
                if r >= self.server_log_len or self.server_log[r].timestamp > right_cutoff:
                    r -= 1
                    hits_in_this_bucket -= 1
                    break
            self.time_to_requests[left_cutoff] = hits_in_this_bucket
            left_cutoff += timedelta(seconds = 1)

    def parse(self):
        self._sum_sliding_window()
        output = self._filter_top_k(self.time_to_requests, self.k)
        output.sort(key=lambda x: x[0]) # resolve ties by putting hosts in lexicographic order
        output.sort(key=lambda x: x[1], reverse=True) # re-sort by frequency, descending
        self._write_output(output, self._data_to_string)
        