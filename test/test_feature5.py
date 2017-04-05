import pytest
import sys
import os.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../src/")
from datetime import datetime,timedelta
from feature5 import GetHostActivityLog
from gen_test_data import gen_test_data

class TestGetHostActivityLog:
    @pytest.fixture(autouse=True)
    def setup(self, tmpdir):
        self.tmpdir = tmpdir

    def test_empty_input(self):
        """Tests that GetHostActivityLog outputs an empty file
        when the input is empty."""
        f_output_null = self.tmpdir.join("null_output.txt")
        input_null = []
        f5_null = GetHostActivityLog(input_null, str(f_output_null), host_to_search="google.com")
        f5_null.parse()
        assert f5_null.bin_to_activity == {}
        assert f_output_null.read() == ""

    def test_input_data_sort(self):
        """Test that GetHostActivityLog sorts the input server logs
        by host and time."""
        f_output_sort = self.tmpdir.join("sort_output.txt")
        input_sort = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature4_sort.txt')) #reuse feature 4 input
        f5_sort = GetHostActivityLog(input_sort, str(f_output_sort), host_to_search="google.com")
        f5_sort.parse()
        # first confirm that hosts are sorted in lexicographic order
        assert f5_sort.server_log[0].host == "bing.com"
        assert f5_sort.server_log[1].host == "bing.com"
        assert f5_sort.server_log[2].host == "google.com"
        assert f5_sort.server_log[3].host == "google.com"

        # then confirm that events are ascending in time within a host
        assert f5_sort.server_log[0].bytes == 56
        assert f5_sort.server_log[1].bytes == 1024
        assert f5_sort.server_log[2].bytes == 256
        assert f5_sort.server_log[3].bytes == 1024

    def test_correct_assignment(self):
        """Test that GetHostActivityLog correctly bins incoming traffic and ignores
        other hosts."""
        f_output_assignment = self.tmpdir.join("assignment_output.txt")
        input_assignment = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature5_assignment.txt'))
        f5_assignment = GetHostActivityLog(input_assignment, str(f_output_assignment), host_to_search="199.72.81.55", minutes_per_bin=5)
        f5_assignment.parse()
        assert f_output_assignment.read() == "01/Jul/1995:00:00:01,6\n01/Jul/1995:00:05:01,1\n01/Jul/1995:00:10:01,5\n"

    def test_handles_gaps(self):
        """Test that GetHostActivityLog outputs a 0 next to any gaps, rather than simply
        skipping them."""
        f_output_gaps = self.tmpdir.join("gaps_output.txt")
        input_gaps = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature5_gaps.txt'))
        f5_gaps = GetHostActivityLog(input_gaps, str(f_output_gaps), host_to_search="199.72.81.55", minutes_per_bin=5)
        f5_gaps.parse()
        assert f_output_gaps.read() == "01/Jul/1995:00:00:01,6\n01/Jul/1995:00:05:01,1\n01/Jul/1995:00:10:01,5\n01/Jul/1995:00:15:01,0\n01/Jul/1995:00:20:01,1\n"
