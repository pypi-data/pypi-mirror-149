# ---------- 聚合正扫----------
scan_payment_create = '/v2/trade/payment/jspay'  # 聚合正扫
scan_payment_close = '/v2/trade/payment/scanpay/close'  # 交易关单
scan_payment_close_query = '/v2/trade/payment/scanpay/closequery'  # 交易关单查询
scan_payment_query = '/v2/trade/payment/scanpay/query'  # 交易查询
scan_payment_refund = '/v2/trade/payment/scanpay/refund'  # 交易退款
scan_payment_refund_query = '/v2/trade/payment/scanpay/refundquery'  # 退款查询

payment_confirm = "/v2/trade/payment/delaytrans/confirm"  # 交易确认
payment_confirm_query = "/v2/trade/payment/delaytrans/confirmquery"  # 交易确认查询
payment_confirm_refund = "/v2/trade/payment/delaytrans/confirmrefund"  # 交易确认退款


split_list = '/v2/trade/trans/split/query'

withhold_pay = "/v2/trade/onlinepayment/withholdpay"  # 代扣

customer_reg = "/v2/merchant/customer/add"  # 快捷支付用户注册

# ---------- 反扫----------
offline_payment_scan = '/v2/trade/payment/micropay'  # 聚合反扫
union_user_id = '/v2/trade/payment/usermark/query'  # 获取银联用户标识

# ---------------快捷支付-------------------

card_payment_page_pay = '/v2/trade/onlinepayment/quickpay/pageinfo'  # 快捷支付页面版
card_bind_apply = '/v2/quickbuckle/apply'  # 快捷绑卡申请
card_bind_confirm = '/v2/quickbuckle/confirm'  # 快捷绑卡确认
card_un_bind = '/v2/quickbuckle/unbind'  # 快捷卡解绑

card_payment_apply = '/v2/trade/onlinepayment/quickpay/apply'  # 快捷支付申请
card_payment_confirm = '/v2/trade/onlinepayment/quickpay/confirm'  # 快捷支付确认

# ---------------线上交易-------------------
union_app_pay = '/v2/trade/onlinepayment/unionpay'  # 银联APP 支付
wap_pay = '/v2/trade/onlinepayment/wappay'  # 手机网页支付
web_page = '/v2/trade/onlinepayment/bankpay/pageinfo'  # 网银支付

online_payment_query = '/v2/trade/onlinepayment/query'  # 查询
online_payment_refund = '/v2/trade/onlinepayment/refund'  # 退款
online_payment_refund_query = '/v2/trade/onlinepayment/refund/query'  # 退款查询

# 网银付款银行账户查询接口
bank_pay_payer_query = '/v2/trade/onlinepayment/bankpay/payerquery'
# 网银支付银行列表查询接口
bank_pay_bank_list = '/v2/trade/onlinepayment/bankpay/banklist'

# ------------------余额支付----------------
account_payment_create = '/v2/trade/acctpayment/pay'  # 余额支付创建
account_payment_query = '/v2/trade/acctpayment/pay/query'  # 余额支付查询
account_payment_refund = '/v2/trade/acctpayment/refund'  # 余额支付退款
account_payment_query_refund = '/v2/trade/acctpayment/refund/query'  # 余额支付退款查询
account_balance_query = '/v2/trade/acctpayment/balance/query'  # 余额信息查询

# ------------------取现--------------------

drawcash_create = '/v2/trade/settlement/enchashment'  # 创建取现
drawcash_query = '/v2/trade/settlement/query'  # 出金交易查询

# ------------------代发--------------------

surrogate_create = '/v2/trade/settlement/surrogate'  # 创建代发

# ------------------银行卡分期支付--------------------

bank_credit_sign = '/v2/trade/installment/bccredit/sign'  # 银行卡分期支付签约
bank_credit_payment = '/v2/trade/installment/bccredit/pay'  # 一段式分期支付
bank_credit_payment_apply = '/v2/trade/installment/bccredit/apply'  # 二段式分期支付申请
bank_credit_payment_confirm = '/v2/trade/installment/bccredit/confirm'  # 二段式分期支付确认
bank_credit_refund = '/v2/trade/installment/bccredit/refund'  # 银行卡分期退款
bank_credit_query = '/v2/trade/installment/bccredit/query'  # 银行卡分期查询

# ------------------银行卡刷卡交易--------------------
card_trade_query = '/v2/trade/card/query'  # 银行卡交易查询
card_payment_sms = '/ssproxy/quickSendSms'  # 短信重发

payment_confirm_list = "/topqur/payConfirmListQuery"  # 交易确认列表查询