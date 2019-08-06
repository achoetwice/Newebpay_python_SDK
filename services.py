from datetime import datetime, date, timedelta
from copy import deepcopy
import json, os, uuid, time
from .gateway_service import *

def FASTLAUNCH_NEWEBPAY(fastlaunch_no, email, charge_type='CREDIT'):
    """
    TradeInfo:1.將交易資料參數（下方列表中參數）透過商店 Key 及 IV 進行 AES 加密。
    TradeSha:1.將交易資料經過上述 AES 加密過的字串，透過商店 Key 及 IV 進行 SHA256 加密。
    Version:請帶 1.5

    charge_tyep = ['CREDIT', 'BARCODE', 'CVS'] 分別代表信用卡,超商條碼,超商QR CODE
    """
    # Setting price
    fastlaunch_price = 50 #自行控制或者由參數傳入
    if charge_type == 'BARCODE':
        fastlaunch_price += 20
        order_comment = '超商條碼固定手續費20元'
    elif charge_type == 'CVS':
        fastlaunch_price += 28
        order_comment = '超商QR CODE或代碼付款固定手續費28元'

    # Setting transaction number
    fastlaunch_no = fastlaunch_no
    item_name = '上架費'
    email=email
    
    # Better Use environment variable(自己設定環境參數)
    MerchantID = os.getenv('MERCHANT_ID')
    key = os.getenv('NEWEBPAY_KEY')
    iv = os.getenv('NEWEBPAY_IV')

    # Setting order parameters
    order_params = {
        'MerchantID': MerchantID,
        'RespondType': 'JSON',
        'TimeStamp': f'{int(time.time())}',
        'Version': '1.5',
        'LangType': 'zh-tw',
        'MerchantOrderNo': fastlaunch_no,
        'Amt':  fastlaunch_price,
        'ItemDesc': item_name,
        'TradeLimit': 0, # 0 for no limit, use any int number 60~900 seconds as trade time limit 
        'NotifyURL': public_url + '/payment/newebpay_return_fastlaunch_data/', # 接收交易資訊
        'Email':email, # 交易完成通知付款人
        'EmailModify': 0,
        'LoginType': 0,
        'OrderComment': f'{order_comment}',
        f'{charge_type}': 1
        # 'InstFlag': 0, # 分期功能
    }
    
    # AES encode 
    AES_info_str = NEWEBPAY_AES(order_params, key, iv)

    # SHA256 encode
    AES_plus = 'HashKey=' + key + '&' + AES_info_str + '&' + 'HashIV=' + iv
    SHA_info_STR = NEWEBPAY_SHA(AES_plus)

    # Combine all needed parameters
    data = {
        'NEWEBPAY_URL':os.getenv('NEWEBPAY_URL'),
        'MerchantID':MerchantID,
        'TradeInfo':AES_info_str,
        'TradeSha':SHA_info_STR,
        'Version':'1.5'
    }

    return data