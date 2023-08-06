import unittest
from tests.conftest import *


class TestRequestTools(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_request_post_v2(self):
        params = {
            "trade_type": "A_NATIVE",
            "trans_amt": "0.01",
            "goods_desc": "goods_desc"
        }
        result = dg_sdk.DGTools.request_post(url="https://api.huifu.com/v2/trade/payment/jspay",
                                             request_params=params)
        assert result["resp_code"] == "00000100"

    def test_request_post_v2_2(self):
        params = {
            "trade_type": "A_NATIVE",
            "trans_amt": "0.01",
            "goods_desc": "goods_desc"
        }
        result = dg_sdk.DGTools.request_post(url="/v2/trade/payment/jspay",
                                             request_params=params)
        assert result["resp_code"] == "00000100"

    def test_request_post_v1(self):
        # dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(private_key_v1, public_key_v1, sys_id_v1, product_id_v1,
        #                                               huifu_id_v1)
        request_params = {
            "huifu_id": huifu_id,
            "trade_type": "A_NATIVE",
            "trans_amt": "0.01",
            "goods_desc": "goods_desc",
            "notify_url": "virgo://http://www.xxx.com/getResp"
        }

        result = dg_sdk.DGTools.request_post("https://spin.cloudpnr.com/top/trans/pullPayInfo",
                                             request_params)
        assert result["resp_code"] == "10000000"

    def test_request_post_v1_2(self):
        # dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(private_key_v1, public_key_v1, sys_id_v1, product_id_v1,
        #                                               huifu_id_v1)
        required_params = {
            "product_id": product_id
        }

        result = dg_sdk.DGTools.request_post("/ssproxy/queryMerchInfo",
                                             required_params)
        assert result["sub_resp_code"] == "00000000"
