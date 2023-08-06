import unittest
from tests.conftest import *


class TestOnlinePayment(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_web_page(self):
        result = dg_sdk.OnlinePayment.web_page(trans_amt="0.01",
                                               goods_desc="goods_desc",
                                               goods_short_name="商品",
                                               gw_chnnl_tp="01",
                                               biz_tp="100001",
                                               notify_url="https://notify_url")
        assert isinstance(result, str)

    def test_union_app_create(self):
        pay_card_type = "Z"
        result = dg_sdk.OnlinePayment.union_app_create(trans_amt="0.01",
                                                       risk_check_data=risk_check_data,
                                                       pay_card_type=pay_card_type)

        assert result["resp_code"] == "22000004"

    def test_wap_page(self):
        result = dg_sdk.OnlinePayment.wap_page(bank_card_no="9558801001107141605",
                                               trans_amt="1.00",
                                               front_url="http://www.xxx.com/getresp",
                                               notify_url="virgo://http://192.168.25.213:30030/sspc/onlineAsync",
                                               extend_pay_data=extend_pay_data,
                                               risk_check_data=risk_check_data,
                                               terminal_device_data=terminal_device_data)

        assert result["data"].get("resp_code") == "90000000"

    def test_query(self):
        pay_card_type = "Z"
        result = dg_sdk.OnlinePayment.union_app_create(trans_amt="0.01",
                                                       risk_check_data=risk_check_data,
                                                       pay_card_type=pay_card_type)

        result = dg_sdk.OnlinePayment.query(org_req_date=result["req_date"],
                                            org_req_seq_id=result["req_seq_id"])

        assert result["resp_code"] == "23000001"

    def test_refund(self):
        pay_card_type = "Z"
        result = dg_sdk.OnlinePayment.union_app_create(trans_amt="0.01",
                                                       risk_check_data=risk_check_data,
                                                       pay_card_type=pay_card_type)

        result = dg_sdk.OnlinePayment.refund(ord_amt="0.01", org_req_date=result["req_date"],
                                             risk_check_data=risk_check_data,
                                             notify_url=notify_url,
                                             org_req_seq_id=result["req_seq_id"])

        assert result["resp_code"] == "23000001"

    def test_refund_query(self):
        pay_card_type = "Z"
        result = dg_sdk.OnlinePayment.union_app_create(trans_amt="0.01",
                                                       risk_check_data=risk_check_data,
                                                       pay_card_type=pay_card_type)
        result = dg_sdk.OnlinePayment.refund(ord_amt="0.01",
                                             org_req_date=result["req_date"],
                                             risk_check_data=risk_check_data,
                                             notify_url=notify_url,
                                             org_req_seq_id=result["req_seq_id"])
        result = dg_sdk.OnlinePayment.refund_query(org_req_date=result["req_date"],
                                                   org_req_seq_id=result["req_seq_id"])
        assert result["resp_code"] == "23000001"

    def test_payer_query(self):
        result = dg_sdk.OnlinePayment.payer_query(org_req_date="20220401",
                                                  org_req_seq_id="122312312312312")
        assert result["resp_code"] == "23000001"

    def test_bank_list(self):
        result = dg_sdk.OnlinePayment.bank_list(gate_type="01",
                                                order_type="P")
        assert result["resp_code"] == "00000000"
