import unittest
from tests.conftest import *


class TestHuabei(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_create_enterprise(self):
        result = dg_sdk.Huabei.create_pcredit_solution("test",
                                                       start_time="2022-06-01 00:00:00",
                                                       end_time="2023-07-01 00:00:00",
                                                       max_money_limit="200.00",
                                                       amount_budget="100.00",
                                                       install_num_str_list="3",
                                                       budget_warning_money="100",
                                                       budget_warning_mail_list="wwww@123.com",
                                                       min_money_limit="100.00",
                                                       budget_warning_mobile_no_list="13122223333")
        assert result["resp_code"] == "00000001"

    def test_add_ali_cert_info(self):
        file = dg_sdk.FileInfo("F120", "fadsfasdfasdfsdfs", "fileName")
        file2 = dg_sdk.FileInfo("F121", "fadsfasdfasdfsdfs", "fileName")
        file_list = [file, file2]
        result = dg_sdk.Huabei.add_ali_cert_info("test", file_list)
        assert result["resp_code"] == "00000003"

    def test_modify_solution_status(self):
        result = dg_sdk.Huabei.modify_solution_status("test", "2")
        assert result["resp_code"] == "00000001"

    def test_modify_pcredit_solution(self):
        result = dg_sdk.Huabei.modify_pcredit_solution("test",
                                                       solution_id="2fasdf",
                                                       start_time="2022-06-01 00:00:00",
                                                       end_time="2023-07-01 00:00:00")
        assert result["resp_code"] == "00000003"

    def test_query_hb_solution(self):
        result = dg_sdk.Huabei.query_hb_solution(solution_id="2fasdf",
                                                 start_time="2022-06-01 00:00:00",
                                                 end_time="2023-07-01 00:00:00")
        assert result["resp_code"] == "00000001"

    def test_query_hb_activity(self):
        result = dg_sdk.Huabei.query_hb_activity(solution_id="2fasdf")
        assert result["resp_code"] == "00000000"
