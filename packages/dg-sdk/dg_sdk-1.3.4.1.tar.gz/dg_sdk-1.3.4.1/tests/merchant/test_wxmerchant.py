import unittest
from tests.conftest import *


class TestHuabei(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_config(self):
        result = dg_sdk.WXMerchant.config(fee_type="01", wx_applet_app_id="ssdfadf")
        assert result["resp_code"] == "00000002"

    def test_query_config(self):
        result = dg_sdk.WXMerchant.query_config()
        assert result["resp_code"] == "00000000"

    def test_realname(self):
        result = dg_sdk.WXMerchant.realname(name="李四",
                                            mobile="13233332222",
                                            id_card_number="3104222233222222")
        assert result["resp_code"] == "00000000"

    def test_query_realname_state(self):
        result = dg_sdk.WXMerchant.query_realname_state()
        assert result["resp_code"] == "00000000"
