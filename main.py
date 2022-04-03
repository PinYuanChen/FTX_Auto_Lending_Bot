import ccxt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--account', help='設置子帳號，預設是主帳號', default=None)
parser.add_argument('-c', '--coin', help='設定要貸出貨幣，我預設用UST', default='UST')
parser.add_argument('-r', '--rate', help='最低每小時貸出利率', default=1e-5)  # ~ 8.76 % / year

if __name__ == '__main__':

    args = parser.parse_args()

    params = {
        'apiKey': "你的API key",
        'secret': "你的API secret key"
    }

    # check subaccount
    subaccount = args.account
    if subaccount is not None:
        config['headers'] = { 'FTX-SUBACCOUNT': subaccount }

    # connect
    ftx = ccxt.ftx(params)

    # get balance
    balance = ftx.fetch_balance()
    coin = args.coin
    
    for item in balance['info']['result']:
        if item ['coin'] == coin:
            size = item['total']
            break

    
    # renew lending
    body = {
        "coin": coin,
        "size": size,
        "rate": args.rate
    }

    res = ftx.private_post_spot_margin_offers(body)

    if res['success']:
        print('Success')
    else:
        print(res.json())
        raise Exception('lending fail')