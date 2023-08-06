import unittest
from tests.conftest import *


class TestAcctPayment(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_acct_payment_create(self):
        split_branch = "{\"acct_infos\":[{\"div_amt\":\"0.01\",\"huifu_id\":\"6666000018344461\"}]}"

        result = dg_sdk.AcctPayment.create("0.01", split_branch, risk_check_data, out_huifu_id="6666000108854952")
        assert result["resp_code"] == "22000002"

    def test_acct_payment_query(self):
        result = dg_sdk.AcctPayment.query("20211123", org_req_seq_id="testsstest")
        assert result["resp_code"] == "23000001"

    def test_acct_payment_refund(self):
        result = dg_sdk.AcctPayment.refund("0.01", "20211123", org_req_seq_id="dsfasdfs")
        assert result["resp_code"] == "23000001"

    def test_acct_refund_query(self):
        result = dg_sdk.AcctPayment.refund_query("20211123", org_req_seq_id="dsfasdfs")
        assert result["resp_code"] == "23000001"

    def test_balance_query(self):
        result = dg_sdk.AcctPayment.balance_query()
        assert result["resp_code"] == "00000000"
