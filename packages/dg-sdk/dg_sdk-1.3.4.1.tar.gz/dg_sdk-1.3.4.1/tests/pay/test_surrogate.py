import unittest
import dg_sdk
from tests.conftest import *


class TestSurrogate(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(private_key, public_key, sys_id, product_id, huifu_id)
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_create(self):
        bank_card_info = dg_sdk.BankCard("张三", "6225098778909876", "00201", "01", "00121", "000213")

        result = dg_sdk.Surrogate.create(cash_amt="0.01",
                                         bank_card_info=bank_card_info,
                                         into_acct_date_type="D1",
                                         purpose_desc="puropose")

        assert result["resp_code"] == "10000000"

    def test_query(self):
        result = dg_sdk.Surrogate.query("20211123", org_req_seq_id="dsfasdfs")

        assert result["resp_code"] == "23000001"
