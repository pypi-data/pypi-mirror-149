import json
import unittest
from tests.conftest import *


class TestDelaytrans(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_confirm(self):
        result = dg_sdk.Delaytrans.confirm(org_req_date=org_req_date,org_req_seq_id=org_req_seq_id)
        assert result["resp_code"] == "23000001"

    def test_confirm_query(self):
        result = dg_sdk.Delaytrans.confirm_query(org_req_date=org_req_date,org_req_seq_id=org_req_seq_id)
        assert result["resp_code"] == "23000001"


    def test_confirm_refund(self):
        result = dg_sdk.Delaytrans.confirm_refund(org_req_date=org_req_date,org_req_seq_id=org_req_seq_id)
        assert result["resp_code"] == "23000001"

    def test_confirm_list(self):
        result = dg_sdk.Delaytrans.query_confirm_list(org_req_date=org_req_date,org_req_seq_id=org_req_seq_id)
        assert result["sub_resp_code"] == "20000004"
