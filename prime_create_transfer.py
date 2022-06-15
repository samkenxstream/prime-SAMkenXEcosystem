import json, hmac, hashlib, time, requests, base64, uuid, os
from urllib.parse import urlparse

####credentials
api_key = os.environ.get("ACCESS_KEY")
secret_key = os.environ.get("SIGNING_KEY")
passphrase = os.environ.get("PASSPHRASE")
portfolio_id = os.environ.get("PORTFOLIO_ID")

timestamp = str(int(time.time()))
idempotency_key = uuid.uuid4()
method = 'POST'
origin_wallet_id = os.environ.get('ORIGIN_WALLET_ID')
amount = '0.01'
currency_symbol = 'ETH'
url = 'https://api.prime.coinbase.com/v1/portfolios/'+portfolio_id+'/wallets/'+origin_wallet_id+'/transfers'
payload = {
    'portfolio_id': portfolio_id,
    'wallet_id': origin_wallet_id,
    'amount': amount,
    'destination': os.environ.get('WALLET_ID'),
    'idempotency_key': str(idempotency_key),
    'currency_symbol': currency_symbol
}
####signature and request
url_path = urlparse(url).path
message = timestamp + method + url_path + json.dumps(payload)
signature = hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()
signature_b64 = base64.b64encode(signature).decode()
headers = {
   'X-CB-ACCESS-SIGNATURE': signature_b64,
   'X-CB-ACCESS-TIMESTAMP': timestamp,
   'X-CB-ACCESS-KEY': api_key,
   'X-CB-ACCESS-PASSPHRASE': passphrase,
   'Accept': 'application/json'
}
response = requests.post(url, json=payload, headers=headers)
parse = json.loads(response.text)
print(json.dumps(parse, indent=3))