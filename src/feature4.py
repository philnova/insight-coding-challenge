import base_feature
from datetime import datetime,timedelta

class FindBlockedIPs(base_feature.BaseFeature):

    def __init__(self, input_data, output_file, failed_attempts = 3, window_seconds = 20, block_minutes = 5, failure_codes=["401"]):
        super(FindBlockedIPs, self).__init__(input_data, output_file)
        self.failed_attempts = failed_attempts
        self.block_minutes = block_minutes
        self.window_seconds = window_seconds
        self.failure_codes = failure_codes
        self.blocked_logs = []
        self.server_log.sort(key=lambda x: x.host) # stable sort so should preserve time information

    def _data_to_string(self, data):
        return data.convert_to_string() # use the method provided in read_server_log

    def _look_ahead_for_failures(self, target_host, start_idx, current_idx, remaining_failed_attempts, time_cutoff):
        for idx in xrange(current_idx, self.server_log_len):
            if self.server_log[idx].timestamp > time_cutoff or self.server_log[idx].host != target_host:
                return start_idx # we cannot conclude anything about skipping ahead
            elif self.server_log[idx].response_code in self.failure_codes:
                remaining_failed_attempts -= 1
                if remaining_failed_attempts == 0:
                    return self._block_incoming_attempts(target_host, idx + 1, self.server_log[idx].timestamp + timedelta(minutes = self.block_minutes))
                else:
                    return self._look_ahead_for_failures(target_host, start_idx, idx + 1, remaining_failed_attempts, time_cutoff)
            else:
                return idx # successful login; we are done looking at this window
        return start_idx

    def _block_incoming_attempts(self, target_host, start_idx, time_cutoff):
        for idx in xrange(start_idx, self.server_log_len):
            if self.server_log[idx].timestamp > time_cutoff or self.server_log[idx].host != target_host:
                return idx 
            self.blocked_logs.append(self.server_log[idx])
        return start_idx

    def _scan_for_first_failed_login(self):
        idx = 0
        while idx < self.server_log_len:
            log = self.server_log[idx]
            if log.response_code in self.failure_codes:
                idx = self._look_ahead_for_failures(log.host, idx + 1, idx + 1, self.failed_attempts - 1, log.timestamp + timedelta(seconds = self.window_seconds))
            else:
                idx += 1

    def parse(self):
        self._scan_for_first_failed_login()
        self._write_output(self.blocked_logs, self._data_to_string)
        