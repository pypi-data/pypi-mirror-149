import unittest
from tests.conftest import *


class TestInstallment(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_sign(self):
        creadit_card = dg_sdk.CreditCardInfo("13144442222", "6225751103859173", "张三", "310481198804223510", "01")
        result = dg_sdk.Installment.sign(trans_amt="0.01",
                                         front_url="https://notify_url",
                                         credit_card=creadit_card,
                                         request_type="1",
                                         terminal_device_data=terminal_device_data)
        assert result["resp_code"] == "90000000"

    def test_payment_apply(self):
        creadit_card = dg_sdk.CreditCardInfo("13144442222", "6225751103859173", "张三", "310481198804223510", "01")

        result = dg_sdk.Installment.payment_apply("100.00",
                                                  creadit_card,
                                                  "goods_descc",
                                                  "3",
                                                  notify_url,
                                                  terminal_device_data,
                                                  risk_check_data,
                                                  extend_pay_data)
        assert result["data"]["resp_code"] == "22000004"

    def test_payment_confirm(self):
        result = dg_sdk.Installment.payment_confirm("goods",
                                                    "cvv2",
                                                    '20220401',
                                                    'org_req_seq_id',
                                                    '20260801',
                                                    '890')
        assert result["data"]["resp_code"] == "10000000"

    # def test_payment(self):
    #     creadit_card = dg_sdk.CreditCardInfo("13144442222", "6225751103859173", "张三", "310481198804223510", "01")
    #
    #     result = dg_sdk.Installment.payment(trans_amt="0.01",
    #                                         credit_card=creadit_card,
    #                                         instalments_num="3",
    #                                         notify_url=notify_url,
    #                                         terminal_device_data=terminal_device_data)
    #
    #     assert result["resp_code"] == "23000001"

    def test_query(self):
        result = dg_sdk.Installment.query(org_req_date="20220401",org_req_seq_id="12123131232131")

        assert result["resp_code"] == "23000001"

    def test_refund(self):
        result = dg_sdk.Installment.refund(ord_amt="0.01",
                                           risk_check_data=risk_check_data,
                                           terminal_device_data=terminal_device_data,
                                           notify_url=notify_url,
                                           org_req_date="20220401",
                                           org_req_seq_id="12123131232131")

        assert result["resp_code"] == "23000001"
