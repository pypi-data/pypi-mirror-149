import json
import unittest

import dg_sdk
from tests.conftest import *


class TestQuickAndHoldPay(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_apply(self):
        result = dg_sdk.QuickAndHoldPay.apply("0.02", "test", "test",
                                              notify_url,
                                              risk_check_data,
                                              terminal_device_data,
                                              extend_pay_data)
        assert result["resp_code"] == "22000001"

    def test_bind_card(self):
        card_info = dg_sdk.Card("6225751103859172", "李四", "13133332222")
        cert_info = dg_sdk.Cert("00", "310475110386223510", "0", "20210401", "20310401")

        result = dg_sdk.QuickAndHoldPay.bind_card("123123123123132",
                                                  "20220401",
                                                  card_info,
                                                  cert_info,
                                                  out_cust_id="6666000103633622")
        assert result["resp_code"] == "00000003"

    def test_bind_card_confirm(self):
        card_info = dg_sdk.Card("6225751103859172", "李四", "13133332222")
        cert_info = dg_sdk.Cert("00", "310475110386223510", "0", "20210401", "20310401")

        result = dg_sdk.QuickAndHoldPay.bind_card_confirm("123123123123132",
                                                          "20220401",
                                                          "out_cust_id",
                                                          card_info,
                                                          cert_info,
                                                          trans_id=org_req_seq_id,
                                                          verify_code="123456")
        assert result["resp_code"] == "00000110"

    def test_unbind(self):
        result = dg_sdk.QuickAndHoldPay.un_bind("123123123123132",
                                                "20220401")
        assert result["resp_code"] == "00000110"

    def test_confirm(self):
        result = dg_sdk.QuickAndHoldPay.confirm("121212",
                                                "20220401",
                                                "123123123123132",
                                                "goods_desc",
                                                "notify_url")
        assert result["resp_code"] == "23000004"

    def test_sms_code(self):
        result = dg_sdk.QuickAndHoldPay.sms_code("121212",
                                                 "123123123123132",
                                                 "20220401")
        assert result["sub_resp_code"] == "20003"

    def test_page(self):
        result = dg_sdk.QuickAndHoldPay.page("10.11",
                                             "http://www.baidu.com",
                                             terminal_device_data,
                                             extend_pay_data,
                                             risk_check_data)
        assert result

    @pytest.mark.skip(reason="没找到文档")
    def test_with_hold_pay(self):
        result = dg_sdk.QuickAndHoldPay.with_hold_pay("10.11",
                                                      "card_band_id",
                                                      "goods_desc",
                                                      "user_huifu_id",
                                                      risk_check_data)
        assert result["resp_code"] == "20003"

    def test_customer_reg(self):
        result = dg_sdk.QuickAndHoldPay.customer_reg("詹上",
                                                     "00",
                                                     "310481198804222210",
                                                     "0",
                                                     "20210101",
                                                     "20231010",
                                                     "13122223333",
                                                     "dfasdfsdfs")
        assert result["resp_code"] == "00000003"
