import unittest
from tests.conftest import *


class TestCloudmis(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_device_info(self):
        result = dg_sdk.Cloudmis.device_info("fdadfasdfsdfsdfs", "test")
        assert result["resp_code"] == "10000000"
