import collections
import pytest
import sys
import os.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../src/")
from feature2 import FindMostIntensiveResources
from gen_test_data import gen_test_data

class TestFindMostIntensiveResources:
    @pytest.fixture(autouse=True)
    def setup(self, tmpdir):
        self.tmpdir = tmpdir

    def test_empty_input(self):
        """Tests that FindMostIntensiveResources outputs an empty file
        when the input is empty."""
        f_output_null = self.tmpdir.join("null_output.txt")
        input_null = []
        f2_null = FindMostIntensiveResources(input_null, str(f_output_null), 0)
        f2_null.parse()
        assert f2_null.resources_to_bandwidth == collections.Counter() 
        assert f_output_null.read() == ""

    def test_grouping(self):
        """Tests that an input file with 6 server logs from 3 unique resources
        is correctly grouped by FindMostIntensiveResources."""
        f_output_grouping = self.tmpdir.join("grouping_output.txt")
        input_grouping = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature2_grouping.txt'))
        f2_grouping = FindMostIntensiveResources(input_grouping, str(f_output_grouping), 3)
        f2_grouping.parse()
        assert f2_grouping.resources_to_bandwidth["/"] == 2048
        assert f2_grouping.resources_to_bandwidth["/coolstuff.gif"] == 256
        assert f2_grouping.resources_to_bandwidth["/lamestuff.gif"] == 112
        assert f_output_grouping.read() == '/\n/coolstuff.gif\n/lamestuff.gif\n'

    def test_breaking_ties(self):
        """Tests that FindMostIntensiveResources orders its output lexicographically when
        two resources have equal volume. In this case /coolstuff.gif and /lamestuff.gif both have
        total 2048, so /coolstuff.gif should come first as c < l."""
        f_output_ties = self.tmpdir.join("ties_output.txt")
        input_ties = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature2_tie.txt'))
        f2_ties = FindMostIntensiveResources(input_ties, str(f_output_ties), 3)
        f2_ties.parse()
        assert f2_ties.resources_to_bandwidth["/coolstuff.gif"] == 2048
        assert f2_ties.resources_to_bandwidth["/lamestuff.gif"] == 2048
        assert f_output_ties.read() == '/coolstuff.gif\n/lamestuff.gif\n'

    def test_k_larger_than_data(self):
        """Tests that FindMostIntensiveResources does not throw errors when the k most active
        resources requested is larger than the total number of unique resources."""
        f_output_large_k = self.tmpdir.join("large_k_output.txt")
        input_large_k = gen_test_data(str(os.path.dirname(__file__) + '/../test/feature2_grouping.txt'))
        f2_large_k = FindMostIntensiveResources(input_large_k, str(f_output_large_k), 10)
        f2_large_k.parse()
        assert f_output_large_k.read() == '/\n/coolstuff.gif\n/lamestuff.gif\n'
