from dg_sdk.request_tools import request_post
from dg_sdk.pay.pay_api_urls import drawcash_create, drawcash_query


class Settlement(object):
    """
    取现相关接口，取现，取现交易查询
    """

    @classmethod
    def query(cls, org_req_date, *, org_req_seq_id="", org_hf_seq_id="", **kwargs):
        """
        取现交易查询
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
    def create(cls, cash_amt, token_no, into_acct_date_type, **kwargs):
        """
        取现
        :param cash_amt: 取现金额
        :param token_no: 取现卡序列号
        :param into_acct_date_type: 到账日期类型，["t0:t0单笔","t1:t1交易","d1:d1交易","t0b:t0批量"]
        :param kwargs: 非必填额外参数
        :return: 返回报文
        """
        required_params = {
            "cash_amt": cash_amt,
            "token_no": token_no,
            "into_acct_date_type": into_acct_date_type
        }
        required_params.update(kwargs)
        return request_post(drawcash_create, required_params)
