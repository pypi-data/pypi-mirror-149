import unittest
from tests.conftest import *


class TestMember(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_create_enterprise(self):
        lic_info = dg_sdk.BussinessLicInfo(reg_name="test",
                                           ent_type="1",
                                           license_code="20200513509363672",
                                           reg_prov_id="350000",
                                           reg_area_id="350200",
                                           reg_district_id="350203",
                                           reg_detail="吉林省长春市思明区解放2路61686340",
                                           license_validity_type="0",
                                           license_begin_date="20200401",
                                           license_end_date="20300101")

        legal_info = dg_sdk.LegalInfo(legal_name="陈立健",
                                      legal_cert_type="00",
                                      legal_cert_no="321084198912066512",
                                      legal_cert_validity_type="1",
                                      legal_cert_begin_date="20121201",
                                      legal_cert_end_date="20301201")
        result = dg_sdk.Member.create_enterprise("test", lic_info, legal_info, "李四", '13144445555')
        assert result["resp_code"] == "00000000"

    def test_create_individual(self):
        result = dg_sdk.Member.create_individual("test",
                                                 "00",
                                                 "301000000009888878",
                                                 "0",
                                                 "20210101",
                                                 '13144445555',
                                                 '20310101')
        assert result["resp_code"] == "00000003"

    def test_modify_individual_base_info(self):
        result = dg_sdk.Member.modify_individual_base_info(contact_email="www123@163.com")
        assert result["resp_code"] == "00000003"

    def test_modify_enter_base_info(self):
        result = dg_sdk.Member.modify_enter_base_info(legal_cert_type="00",
                                                      legal_cert_no="321084198912066512",
                                                      legal_cert_validity_type="1",
                                                      legal_cert_begin_date="20121201",
                                                      legal_cert_end_date="20301201",
                                                      license_validity_type="0",
                                                      license_begin_date="20200401",
                                                      license_end_date="20300101"
                                                      )
        assert result["resp_code"] == "00000003"

    def test_reg_busi_info(self):
        result = dg_sdk.Member.reg_busi_info(upper_huifu_id=upper_huifu_id)
        assert result["resp_code"] == "00000003"

    def test_query_user_detail(self):
        result = dg_sdk.Member.query_user_detail()
        assert result["resp_code"] == "00000003"
