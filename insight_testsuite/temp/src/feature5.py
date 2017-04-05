import base_feature
from datetime import datetime,timedelta

class GetHostActivityLog(base_feature.BaseFeature):

    def __init__(self, input_data, output_file, host_to_search, minutes_per_bin=5):
        super(GetHostActivityLog, self).__init__(input_data, output_file)
        self.host_to_search = host_to_search
        self.minutes_per_bin = minutes_per_bin
        self.bin_to_activity = {}
        self.server_log.sort(key=lambda x: x.host)

    def _data_to_string(self, data):
        return data[0].strftime('%d/%b/%Y:%H:%M:%S')+","+str(data[1])

    def _find_activity_bounds_from_host(self):
        print self.host_to_search
        first, last = None, None
        for idx, log in enumerate(self.server_log):
            if first is not None and log.host != self.host_to_search:
                last = idx - 1 # this should be the first host after the target host
                return first, last
            elif first is None and log.host == self.host_to_search:
                first = idx
        if first is not None and last is None:
            last = self.server_log_len - 1
        return first, last

    def _bin_activity(self, first, last):
        start_time = self.server_log[first].timestamp
        current_bin = 0
        cutoff = start_time + timedelta(minutes = self.minutes_per_bin)
        for idx in xrange(first, last + 1):
            if self.server_log[idx].timestamp <= cutoff:
                current_bin += 1
            else:
                self.bin_to_activity[start_time] = current_bin
                current_bin = 1
                start_time = cutoff
                cutoff += timedelta(minutes = self.minutes_per_bin)
        self.bin_to_activity[start_time] = current_bin

    def parse(self):
        first, last = self._find_activity_bounds_from_host()
        print first, last
        if first is not None:
            # conditional ensures that host was actually found
            self._bin_activity(first, last)
        output = [(k, v) for k, v in self.bin_to_activity.items()]
        output.sort(key=lambda x: x[0]) # sort by time ascending
        self._write_output(output, self._data_to_string)
