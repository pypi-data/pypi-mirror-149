from dg_sdk.request_tools import request_post
from dg_sdk.pay.pay_api_urls import surrogate_create, drawcash_query
from dg_sdk.pay.module.bank_card import BankCard


class Surrogate(object):
    """
    代发相关接口，代发，代发交易查询
    """

    @classmethod
    def query(cls, org_req_date, *, org_req_seq_id="", org_hf_seq_id="", **kwargs):
        """
        出金交易查询
        :param org_req_date: 原机构请求日期
        :param org_req_seq_id: 原机构请求流水号
        :param org_hf_seq_id: 交易返回的全局流水号
        :param kwargs: 非必填额外参数
        :return: 返回报文
        """
        required_params = {
            "org_req_date": org_req_date,
            "org_req_seq_id": org_req_seq_id,
            "org_hf_seq_id": org_hf_seq_id,
        }

        required_params.update(kwargs)
        return request_post(drawcash_query, required_params)

    @classmethod
    def create(cls, cash_amt, bank_card_info: BankCard, into_acct_date_type, purpose_desc, **kwargs):
        """
        代发
        :param cash_amt: 交易金额
        :param bank_card_info: 银行卡信息
        :param into_acct_date_type: 到账日期类型，["t0:t0单笔","t1:t1交易","d1:d1交易","t0b:t0批量"]
        :param purpose_desc: 代发用途描述
        :param kwargs: 非必填额外参数
        :return: 返回报文
        """

        required_params = {
            "cash_amt": cash_amt,
            "bank_account_name": bank_card_info.bank_account_name,
            "bank_card_no_crypt": bank_card_info.bank_card_no_crypt,
            "bank_code": bank_card_info.bank_code,
            "card_acct_type": bank_card_info.card_acct_type,
            "province": bank_card_info.province,
            "area": bank_card_info.area,
            "purpose_desc": purpose_desc,
            "into_acct_date_type": into_acct_date_type
        }
        required_params.update(kwargs)
        return request_post(surrogate_create, required_params)
