import unittest

import dg_sdk
from tests.conftest import *


class TestSettlement(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(private_key, public_key, sys_id, product_id, huifu_id)

        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_create(self):
        result = dg_sdk.Settlement.create(cash_amt="0.01",
                                          token_no="121231312",
                                          into_acct_date_type="D1")

        assert result["resp_code"] == "22000005"

    def test_query(self):
        result = dg_sdk.Settlement.query("20211123", org_req_seq_id="dsfasdfs")

        assert result["resp_code"] == "23000001"
