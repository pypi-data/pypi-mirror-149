from dg_sdk.core.api_request import ApiRequest
from dg_sdk.core.api_request_v1 import ApiRequest as ApiRequestV1
from dg_sdk.dg_client import DGClient
from dg_sdk.common_util import generate_mer_order_id
import datetime


def __req_url_init(url):
    """
    预处理请求地址，判断是否包含全量地址，还是仅有 path
    :param url: 请求地址
    :return:
    """

    if DGClient.env == "mertest":
        base_url = DGClient.BASE_URL_MER_TEST
    else:
        base_url = DGClient.BASE_URL

    if "http" in url:
        request_url = url
    else:
        request_url = base_url + url

    return request_url


def __req_param_init(request_params, need_seq_id=True):
    """
    预处理请求参数，补全汇付ID 以及 req_seq_id req_date
    :param request_params:
    :return:
    """
    mer_config = DGClient.mer_config

    if mer_config is None:
        raise RuntimeError('SDK 未初始化')

    if "huifu_id" not in request_params:
        request_params['huifu_id'] = mer_config.huifu_id

    if need_seq_id:
        if not request_params.get('req_seq_id'):
            request_params['req_seq_id'] = generate_mer_order_id()

        if not request_params.get('req_date'):
            request_params['req_date'] = datetime.datetime.now().strftime('%Y%m%d')

    return request_params, mer_config


def request_post(url, request_params, files=None, need_seq_id=True):
    """
    网络请求方法
    :param url: 请求地址
    :param request_params: 请求参数
    :param files: 附带文件，可为空
    :param need_seq_id: 是否需要自动生成 req_seq_id 与 req_date
    :return: 网络请求返回内容
    """

    url = __req_url_init(url)
    request_params, mer_config = __req_param_init(request_params, need_seq_id)

    if "v2" in url:

        ApiRequest.build(mer_config.product_id, mer_config.sys_id, mer_config.private_key, mer_config.public_key, url,
                         request_params, DGClient.__version__, DGClient.connect_timeout)

        return ApiRequest.post(files)
    else:

        ApiRequestV1.build(mer_config.product_id, mer_config.sys_id, mer_config.private_key, mer_config.public_key, url,
                           request_params, DGClient.__version__, DGClient.connect_timeout)
        return ApiRequestV1.post(files)
