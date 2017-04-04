import collections
import pytest
import sys
import os.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../src/")
from feature1 import FindMostActive
from gen_test_data import gen_test_data

class TestFindMostActive:
    @pytest.fixture(autouse=True)
    def setup(self, tmpdir):
        self.tmpdir = tmpdir

    def test_empty_input(self):
        """Tests that FindMostActive outputs an empty file
        when the input is empty."""
        f_output_null = self.tmpdir.join("null_output.txt")
        input_null = []
        f1_null = FindMostActive(input_null, str(f_output_null), 0)
        f1_null.parse()
        assert f1_null.hosts_to_hits == collections.Counter() 
        assert f_output_null.read() == ""

    def test_grouping(self):
        """Tests that an input file with 6 server logs from 3 unique hosts
        is correctly grouped by FindMostActive."""
        f_output_grouping = self.tmpdir.join("grouping_output.txt")
        input_grouping = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature1_grouping.txt'))
        f1_grouping = FindMostActive(input_grouping, str(f_output_grouping), 3)
        f1_grouping.parse()
        assert f1_grouping.hosts_to_hits["google.com"] == 3
        assert f1_grouping.hosts_to_hits["bing.com"] == 2
        assert f1_grouping.hosts_to_hits["askjeeves.com"] == 1
        assert f_output_grouping.read() == 'google.com,3\nbing.com,2\naskjeeves.com,1\n'

    def test_breaking_ties(self):
        """Tests that FindMostActive orders its output lexicographically when
        two hosts have equal traffic. In this case bing.com and google.com both have
        three hits, so bing.com should come first in the output file as b < g."""
        f_output_ties = self.tmpdir.join("ties_output.txt")
        input_ties = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature1_tie.txt'))
        f1_ties = FindMostActive(input_ties, str(f_output_ties), 3)
        f1_ties.parse()
        assert f1_ties.hosts_to_hits["google.com"] == 3
        assert f1_ties.hosts_to_hits["bing.com"] == 3
        assert f_output_ties.read() == 'bing.com,3\ngoogle.com,3\n'

    def test_k_larger_than_data(self):
        """Tests that FindMostActive does not throw errors when the k most active
        hosts requested is larger than the total number of unique hosts."""
        f_output_large_k = self.tmpdir.join("large_k_output.txt")
        input_large_k = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature1_grouping.txt'))
        f1_large_k = FindMostActive(input_large_k, str(f_output_large_k), 10)
        f1_large_k.parse()
        assert f_output_large_k.read() == 'google.com,3\nbing.com,2\naskjeeves.com,1\n'
