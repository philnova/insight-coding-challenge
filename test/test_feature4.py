import collections
import pytest
import sys
import os.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../src/")
from datetime import datetime,timedelta
from feature4 import FindBlockedIPs
from gen_test_data import gen_test_data

class TestFindBlockedIPs:
    @pytest.fixture(autouse=True)
    def setup(self, tmpdir):
        self.tmpdir = tmpdir

    def test_empty_input(self):
        """Tests that FindBlockedIPs outputs an empty file
        when the input is empty."""
        f_output_null = self.tmpdir.join("null_output.txt")
        input_null = []
        f4_null = FindBlockedIPs(input_null, str(f_output_null))
        f4_null.parse()
        assert f4_null.blocked_logs == []
        assert f_output_null.read() == ""

    def test_input_data_sort(self):
        """Test that FindBlockedIPs sorts the input server logs
        by host and time."""
        f_output_sort = self.tmpdir.join("sort_output.txt")
        input_sort = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature4_sort.txt'))
        f4_sort = FindBlockedIPs(input_sort, str(f_output_sort))
        f4_sort.parse()
        # first confirm that hosts are sorted in lexicographic order
        assert f4_sort.server_log[0].host == "bing.com"
        assert f4_sort.server_log[1].host == "bing.com"
        assert f4_sort.server_log[2].host == "google.com"
        assert f4_sort.server_log[3].host == "google.com"

        # then confirm that events are ascending in time within a host
        assert f4_sort.server_log[0].bytes == 56
        assert f4_sort.server_log[1].bytes == 1024
        assert f4_sort.server_log[2].bytes == 256
        assert f4_sort.server_log[3].bytes == 1024

    def test_blocked_requests_not_reconsidered(self):
        """Test that FindBlockedIPs does not start a new block
        window if there are three failed login attempts within
        a time period that is already blocked."""
        f_output_not_reconsider = self.tmpdir.join("not_reconsider_output.txt")
        input_not_reconsider = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature4_block_not_reconsider.txt'))
        f4_not_reconsider = FindBlockedIPs(input_not_reconsider, str(f_output_not_reconsider))
        f4_not_reconsider.parse()
        assert len(f4_not_reconsider.blocked_logs) == 3

        # test that last request is not blocked
        # final request falls outside the block window established by the first three unsuccessful requests
        # but would fall within the block window of the unsuccessful requests that were blocked
        assert f4_not_reconsider.blocked_logs[2].timestamp == datetime.strptime("01/Jul/1995:00:04:05",'%d/%b/%Y:%H:%M:%S')

    def test_failed_requests_are_reconsidered(self):
        """Test that FindBlockedIPs reconsiders a failed login attempt
        that does *not* lead to a block if it might be the beginning of
        a later window of failed login attempts."""
        f_output_reconsider = self.tmpdir.join("reconsider_output.txt")
        input_reconsider = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature4_fail_reconsider.txt'))
        f4_reconsider = FindBlockedIPs(input_reconsider, str(f_output_reconsider))
        f4_reconsider.parse()
        assert len(f4_reconsider.blocked_logs) == 1
        assert f4_reconsider.blocked_logs[0].timestamp == datetime.strptime("01/Jul/1995:00:04:05",'%d/%b/%Y:%H:%M:%S')

    def test_additional_unsuccessful_logins_are_blocked(self):
        """Test that FindBlockedIPs begins blocking incoming requests as soon as
        the threshhold for failed requests is met, and that additional incoming failed
        requests are blocked."""
        f_output_immediate = self.tmpdir.join("immediate_output.txt")
        input_immediate = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature4_immediate.txt'))
        f4_immediate = FindBlockedIPs(input_immediate, str(f_output_immediate))
        f4_immediate.parse()
        assert len(f4_immediate.blocked_logs) == 2

    def test_successful_login_reset(self):
        """Test that FindBlockedIPs resets its counter if there
        is a successful login request after a failed login request."""
        f_output_reset = self.tmpdir.join("reset_output.txt")
        input_reset = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature4_reset.txt'))
        f4_reset = FindBlockedIPs(input_reset, str(f_output_reset))
        f4_reset.parse()
        assert len(f4_reset.blocked_logs) == 0

    def test_failed_logins_depend_on_host(self):
        """Test that failed logins from multiple hosts do not lead
        to a block."""
        f_output_multiple_hosts = self.tmpdir.join("multiple_hosts_output.txt")
        input_multiple_hosts = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature4_multiple_hosts.txt'))
        f4_multiple_hosts = FindBlockedIPs(input_multiple_hosts, str(f_output_multiple_hosts))
        f4_multiple_hosts.parse()
        assert len(f4_multiple_hosts.blocked_logs) == 0

    def test_failed_attempts_counter(self):
        """Test that the counter of failed attempts that lead to a block
        can be configured."""
        f_output_configure_fail = self.tmpdir.join("configure_fail_output.txt")
        input_configure_fail = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature4_configure_fail.txt'))
        f4_configure_fail = FindBlockedIPs(input_configure_fail, str(f_output_configure_fail), failed_attempts=2)
        f4_configure_fail.parse()
        assert len(f4_configure_fail.blocked_logs) == 4

    def test_window_seconds(self):
        """Test that the size of the window to look for failed login attempts 
        can be configured."""
        f_output_configure_window = self.tmpdir.join("configure_window_output.txt")
        input_configure_window = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature4_configure_window.txt'))
        f4_configure_window = FindBlockedIPs(input_configure_window, str(f_output_configure_window), window_seconds=30)
        f4_configure_window.parse()
        assert len(f4_configure_window.blocked_logs) == 1

    def test_block_window_minutes(self):
        """Test that the size of the block period can be configured."""
        f_output_configure_block = self.tmpdir.join("configure_block_output.txt")
        input_configure_block = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature4_configure_block.txt'))
        f4_configure_block = FindBlockedIPs(input_configure_block, str(f_output_configure_block), block_minutes=30)
        f4_configure_block.parse()
        assert len(f4_configure_block.blocked_logs) == 2
