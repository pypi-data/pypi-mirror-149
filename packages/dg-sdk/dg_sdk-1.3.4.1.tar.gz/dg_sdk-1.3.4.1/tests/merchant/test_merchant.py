import unittest
from tests.conftest import *


class TestMerchant(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(private_key, public_key, sys_id, product_id, huifu_id)
        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_query_merch_info(self):
        result = dg_sdk.Merchant.query_merch_info()
        assert result["resp_code"] == "00000000"

    def test_modify(self):
        result = dg_sdk.Merchant.modify(upper_huifu_id=upper_huifu_id)
        assert result["resp_code"] == "00000000"

    def test_download_file(self):
        result = dg_sdk.Merchant.download_bill(check_order_type="2", file_date="20211128")

        assert result["resp_code"] == "00000000"

    def test_upload(self):
        result = dg_sdk.Merchant.upload(file_type="F01", picture_path=pic_path)
        print(result)
        assert result["data"]["resp_code"] == "00000000"

    def test_create_enterprise(self):
        merchant_info = dg_sdk.MerchantInfo(short_name="test",
                                            prov_id="350000",
                                            area_id="310100",
                                            district_id="350203",
                                            detail_addr="吉林省长春市思明区解放2路61686340",
                                            contact_name="test",
                                            contact_mobile_no="13111112222",
                                            contact_email="123@123.com",
                                            busi_type="1",
                                            receipt_name="盈盈超市",
                                            mcc="5411",
                                            service_phone="13133333333",
                                            sms_send_flag="0",
                                            login_name="test1123456")

        card_info = dg_sdk.MerCardInfo(card_type="1",
                                       card_name="陈立健",
                                       card_no="6225682141000002951",
                                       prov_id="310000",
                                       area_id="310100",
                                       bank_code="01030000",
                                       branch_name="中国农业银行股份有限公司上海马当路支行",
                                       cert_type="00",
                                       cert_no="321084198912066512",
                                       cert_validity_type="1",
                                       cert_begin_date="20121201",
                                       cert_end_date="20301201",
                                       mp="13700000214")
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
        settle_info = dg_sdk.SettleConfigInfo(settle_cycle="D1",
                                              min_amt="1.00",
                                              remained_amt="2.00",
                                              settle_abstract="abstract",
                                              out_settle_flag="2",
                                              out_settle_huifuid="",
                                              fixed_ratio="5.00")
        cash_config = dg_sdk.CashConfigInfo(cash_type="D0",
                                            fix_amt="1.00",
                                            fee_rate="0.11")
        cash_list = [cash_config]

        result = dg_sdk.Merchant.create_enterprise(upper_huifu_id=upper_huifu_id,
                                                   merch_info=merchant_info,
                                                   card_info=card_info,
                                                   lic_info=lic_info,
                                                   legal_person=legal_info,
                                                   settle_info=settle_info,
                                                   cash_config=cash_list)

        assert result["resp_code"] == "00000001"

    def test_create_individual(self):
        merchant_info = dg_sdk.MerchantInfo(short_name="test",
                                            prov_id="350000",
                                            area_id="310100",
                                            district_id="350203",
                                            detail_addr="吉林省长春市思明区解放2路61686340",
                                            contact_name="test",
                                            contact_mobile_no="13111112222",
                                            contact_email="123@123.com",
                                            busi_type="1",
                                            receipt_name="盈盈超市",
                                            mcc="5411",
                                            service_phone="13133333334",
                                            sms_send_flag="0",
                                            login_name="te1st1123456")

        card_info = dg_sdk.MerCardInfo(card_type="1",
                                       card_name="陈立健",
                                       card_no="6225682141000002951",
                                       prov_id="310000",
                                       area_id="310100",
                                       bank_code="01030000",
                                       branch_name="中国农业银行股份有限公司上海马当路支行",
                                       cert_type="00",
                                       cert_no="321084198912066512",
                                       cert_validity_type="1",
                                       cert_begin_date="20121201",
                                       cert_end_date="20301201",
                                       mp="13700000214")

        settle_info = dg_sdk.SettleConfigInfo(settle_cycle="D1",
                                              min_amt="1.00",
                                              remained_amt="2.00",
                                              settle_abstract="abstract",
                                              out_settle_flag="2",
                                              out_settle_huifuid="",
                                              fixed_ratio="5.00")
        cash_config = dg_sdk.CashConfigInfo(cash_type="D0",
                                            fix_amt="1.00",
                                            fee_rate="0.11")
        cash_list = [cash_config]

        result = dg_sdk.Merchant.create_individual(upper_huifu_id=upper_huifu_id,
                                                   reg_name="商户名称",
                                                   merch_info=merchant_info,
                                                   card_info=card_info,
                                                   settle_info=settle_info,
                                                   cash_config=cash_list)

        assert result["resp_code"] == "00000001"

    def test_modify_headquarters(self):
        result = dg_sdk.Merchant.modify_headquarters(chains_id="test",
                                                     name="总部123",
                                                     contact_name="联系人1",
                                                     contact_mobile_no="13122223333",
                                                     contact_cert_no="110101200208179198")

        assert result["resp_code"] == "00000003"

    def test_add_head(self):
        result = dg_sdk.Merchant.add_headquarters(name="总部123",
                                                  contact_name="联系人1",
                                                  contact_mobile_no="13122223333",
                                                  contact_cert_no="110101200208179198")

        assert result["resp_code"] == "00000003"

    def test_bind_headquarters(self):
        result = dg_sdk.Merchant.bind_headquarters(chains_id="test_id",
                                                   mer_type="0",
                                                   state="1"
                                                   )

        assert result["resp_code"] == "00000003"

    def test_acct_info(self):
        result = dg_sdk.Merchant.query_acct_info()
        assert result["sub_resp_code"] == "00000000"

    def test_reg_busi_info(self):
        result = dg_sdk.Merchant.reg_busi_info(upper_huifu_id, "2")
        assert result["resp_code"] == "00000000"

    def test_modify_busi_info(self):
        result = dg_sdk.Merchant.modify_busi_info()
        assert result["resp_code"] == "00000000"

    def test_query_apply_status(self):
        result = dg_sdk.Merchant.modify_busi_info()
        apply_no = result["apply_no"]
        result = dg_sdk.Merchant.query_apply_status(apply_no)
        assert result["resp_code"] == "00000000"

    def test_add_split_config(self):
        result = dg_sdk.Merchant.add_split_config(rule_origin="01",
                                                  repeal_flag="N",
                                                  refund_flag="N",
                                                  div_flag="N",
                                                  apply_ratio="50",
                                                  start_type="0")
        assert result["sub_resp_code"] == "90000000"

    def test_query_split_config(self):
        result = dg_sdk.Merchant.query_split_config()
        assert result["sub_resp_code"] == "00000000"

    def test_installment_config(self):
        result = dg_sdk.Merchant.installment_config()
        assert result["resp_code"] == "00000000"

    def test_query_installment_config(self):
        result = dg_sdk.Merchant.query_installment_config()
        assert result["resp_code"] == "00000000"

    def test_reg_activity(self):
        result = dg_sdk.Merchant.reg_activity(pay_way="W",
                                              fee_type="7",
                                              syt_photo="42204258-967e-373c-88d2-1afa4c7bb8ef",
                                              mm_photo="42204258-967e-373c-88d2-1afa4c7bb8ef",
                                              bl_photo="42204258-967e-373c-88d2-1afa4c7bb8ef",
                                              dh_photo="42204258-967e-373c-88d2-1afa4c7bb8ef")

        assert result["resp_code"] == "00000007"

    def test_query_activities(self):
        result = dg_sdk.Merchant.query_activities()

        assert result["resp_code"] == "00000000"

    def test_settlement_query(self):
        result = dg_sdk.Merchant.settlement_query(begin_date="20210910", end_date="20210911")

        assert result["resp_code"] == "00000000"

    def test_branch_query(self):
        result = dg_sdk.Merchant.branch_query(query_mode="0")

        assert result["resp_code"] == "00000000"

    def test_branch_config(self):
        result = dg_sdk.Merchant.branch_config(mercust_list="6666000103669284",
                                               upper_huifu_id=upper_huifu_id,
                                               bind_type="1")

        assert result["resp_code"] == "00000003"

    def test_branch_mercust_query(self):
        result = dg_sdk.Merchant.branch_mercust_query(query_mode="0")

        assert result["resp_code"] == "00000000"
