import collections
import pytest
import os.path
from feature4 import FindBlockedIPs
from gen_test_data import gen_test_data

class TestFindBlockedIPs:
    @pytest.fixture(autouse=True)
    def setup(self, tmpdir):
        self.tmpdir = tmpdir

    def test_empty_input(self):
        pass
