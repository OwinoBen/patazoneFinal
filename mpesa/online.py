import requests
import json
from datetime import datetime
import base64
from requests.auth import HTTPBasicAuth


def getAccessToken():
    consumer_key = 'DreE5Tw3IZ0c4K0q8vINnEMERs68Lqf9'
    consumer_secret = 'elCYrk0bAJfcDkHv'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return r.json()['access_token']


lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
Business_short_code = "174379"
passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
data_to_encode = Business_short_code + passkey + lipa_time
online_password = base64.b64encode(data_to_encode.encode())
decode_password = online_password.decode('utf-8')


def lipa_na_mpesa_online(Amount, PhoneNumber):
    initial_phone = str(254)
    final_phone = (initial_phone + PhoneNumber)
    print(final_phone)
    access_token = getAccessToken()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer " + str(access_token), "Content-Type": "application/json"}
    request = {
        "BusinessShortCode": Business_short_code,
        "Password": decode_password,
        "Timestamp": lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": Amount,
        "PartyA": final_phone,  # replace with your phone number to get stk push
        "PartyB": Business_short_code,
        "PhoneNumber": final_phone,  # replace with your phone number to get stk push
        "CallBackURL": "https://patazone.herokuapp.com/lipa_na_mpesa",
        "AccountReference": "Patazone Marketplace",
        "TransactionDesc": "Testing stk push"
    }

    response = requests.post(api_url, json=request, headers=headers)
    print(response.text)

    # check response code for errors and return response
    if response.status_code > 299:
        return {
                   "success": False,
                   "message": "Sorry, something went wrong please try again later."
               }, 400

    # CheckoutRequestID = response.text['CheckoutRequestID']

    # return a response to your user
    return {
               "data": json.loads(response.text)
           }, 200
