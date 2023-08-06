from dg_sdk.core.rsa_utils import rsa_design, rsa_long_encrypt
from dg_sdk.request_tools import request_post
from dg_sdk.dg_client import DGClient
from Crypto.Hash import MD5
from dg_sdk.core.api_request import verify_sign


class DGTools(object):

    @classmethod
    def verify_sign(cls, data, sign, pub_key=""):
        """
        校验返回报文签名
        :param data: 返回data
        :param sign:  返回签名
        :param pub_key: 公钥，默认使用SDK初始化时的公钥
        :return: 是否通过校验
        """
        if not pub_key:
            pub_key = DGClient.mer_config.public_key
        return verify_sign(sign, data, pub_key)

    @classmethod
    def verify_webhook_sign(cls, data:str, sign:str, key:str):
        """
        校验 webhook 返回报文签名
        :param data: 返回 data
        :param sign:  返回签名
        :param key: 加签key
        :return: 是否通过校验
        """
        h = MD5.new()
        h.update(str(data + key).encode('utf-8'))
        return h.hexdigest().lower() == sign.lower()


    @classmethod
    def encrypt_with_public_key(cls, orignal_str, public_key=""):
        """
        通过RSA 公钥加密敏感信息
        :param orignal_str: 原始字符串
        :param public_key: 公钥，不传使用商户配置公钥
        :return: 密文
        """
        if not public_key:
            public_key = DGClient.mer_config.public_key
        return rsa_long_encrypt(orignal_str, public_key)

    @classmethod
    def request_post(cls, url, request_params, files=None):
        """
        网络请求通用方法，根据请求的URL 地址判断是V1还是V2版本接口
        :param url: 请求地址
        :param request_params: 请求参数
        :param files: 附带文件，可为空
        :return: 网络请求返回内容
        """
        required_params = {
        }
        required_params.update(request_params)
        return request_post(url=url, request_params=required_params, files=files)


