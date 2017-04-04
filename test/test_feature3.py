import collections
import pytest
import sys
import os.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../src/")
from feature3 import FindHighestTrafficWindows
from gen_test_data import gen_test_data

class TestFindHighestTrafficWindows:
    @pytest.fixture(autouse=True)
    def setup(self, tmpdir):
        self.tmpdir = tmpdir

    def test_empty_input(self):
        """Tests that FindHighestTrafficWindows outputs an empty file
        when the input is empty."""
        f_output_null = self.tmpdir.join("null_output.txt")
        input_null = []
        f3_null = FindHighestTrafficWindows(input_null, str(f_output_null), 0)
        f3_null.parse()
        assert f3_null.timezone == "+0000" # should be set to default value
        assert f3_null.time_to_requests == collections.Counter() 
        assert f_output_null.read() == ""

    def test_timezone(self):
        """Tests that FindHighestTrafficWindows reads timezone from
        the input."""
        f_output_single_entry = self.tmpdir.join("single_entry_output.txt")
        input_single_entry = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature3_single_entry.txt'))
        f3_single_entry = FindHighestTrafficWindows(input_single_entry, str(f_output_single_entry))
        f3_single_entry.parse()
        assert f3_single_entry.timezone == "-0400"

    def test_single_entry(self):
        """Tests that FindHighestTrafficWindows correctly identifies that the
        highest traffic window for a single entry begins with the entry."""
        f_output_single_entry = self.tmpdir.join("single_entry_output.txt")
        input_single_entry = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature3_single_entry.txt'))
        f3_single_entry = FindHighestTrafficWindows(input_single_entry, str(f_output_single_entry))
        f3_single_entry.parse()
        assert f_output_single_entry.read() == "01/Jul/1995:00:00:01 -0400,1\n"

    def test_in_between_values(self):
        """Tests that FindHighestTrafficWindows recognizes that highest
        traffic windows may begin between logged events."""
        f_output_multi_entry = self.tmpdir.join("multi_entry_output.txt")
        input_multi_entry = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature3_multi_entry.txt'))
        f3_multi_entry = FindHighestTrafficWindows(input_multi_entry, str(f_output_multi_entry))
        f3_multi_entry.parse()
        assert f_output_multi_entry.read() == "01/Jul/1995:00:00:01 -0400,2\n01/Jul/1995:00:00:02 -0400,1\n01/Jul/1995:00:00:03 -0400,1\n01/Jul/1995:00:00:04 -0400,1\n"

    def test_window_boundary(self):
        """Tests for off-by-one errors at the boundary of the sliding window: ensure that two events exactly 60 minutes
        apart are both included in the same window, but two events 60 minutes and 1 second apart are not included in the
        same window, and two events at the same clock time but separated by one day are also not included in the same
        time window."""
        f_output_boundary = self.tmpdir.join("boundary_output.txt")
        input_boundary = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature3_boundary.txt'))
        f3_boundary = FindHighestTrafficWindows(input_boundary, str(f_output_boundary), k=2)
        f3_boundary.parse()
        assert f_output_boundary.read() == "01/Jul/1995:00:00:03 -0400,2\n01/Jul/1995:00:00:04 -0400,2\n"

    def test_limited_to_k(self):
        """Tests that if there are more than k traffic windows, we only return
        the top k."""
        f_output_multi_entry = self.tmpdir.join("multi_entry_output.txt")
        input_multi_entry = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature3_multi_entry.txt'))
        f3_multi_entry = FindHighestTrafficWindows(input_multi_entry, str(f_output_multi_entry),k=2)
        f3_multi_entry.parse()
        assert f_output_multi_entry.read() == "01/Jul/1995:00:00:01 -0400,2\n01/Jul/1995:00:00:04 -0400,1\n"

    def test_dynamic_window(self):
        """Tests that we can configure the size of the sliding window."""
        f_output_window = self.tmpdir.join("boundary_output.txt")
        input_window = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature3_boundary.txt'))
        f3_window = FindHighestTrafficWindows(input_window, str(f_output_window),k=2,minutes_per_bucket=120)
        f3_window.parse()
        assert f_output_window.read() == "01/Jul/1995:00:00:03 -0400,3\n01/Jul/1995:00:00:04 -0400,2\n"
