import requests
import json
from datetime import datetime
import base64
from requests.api import request
from requests.auth import HTTPBasicAuth
from django.conf import settings
url = settings.BASE_URL

def getAccessToken():
        consumer_key = '7NGrk2RPIW1SGZirGOn6A3xfRUA9egN8'
        consumer_secret = 'luKizjW5A47Te73h'
        api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        return r.json()['access_token']


lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
Business_short_code = "174379"
passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
data_to_encode = Business_short_code + passkey + lipa_time
online_password = base64.b64encode(data_to_encode.encode())
decode_password = online_password.decode('utf-8')


def lipa_na_mpesa_online(Amount,PhoneNumber):
    access_token = getAccessToken()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = { "Authorization": "Bearer "+str(access_token) ,"Content-Type": "application/json" }
    request = {
        "BusinessShortCode": Business_short_code,
        "Password": decode_password,
        "Timestamp":lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": Amount,
        "PartyA": PhoneNumber,  # replace with your phone number to get stk push
        "PartyB": Business_short_code,
        "PhoneNumber": PhoneNumber,  # replace with your phone number to get stk push
        "CallBackURL": "http://127.0.0.1:8000/lipa_na_mpesa",
        "AccountReference": "Patazone Marketplace",
        "TransactionDesc": "Testing stk push"
    }

    response = requests.post(api_url, json=request, headers=headers)
    print(response.text)

    # check response code for errors and return response
    if response.status_code > 299:
        return{
            "success": False,
            "message":"Sorry, something went wrong please try again later."
        },400

    # CheckoutRequestID = response.text['CheckoutRequestID']

    # Do something in your database e.g store the transaction or as an order
    # make sure to store the CheckoutRequestID to identify the tranaction in
    # your CallBackURL endpoint.

    # return a response to your user
    return {
        "data": json.loads(response.text)
    },200



