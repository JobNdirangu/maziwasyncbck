import os

import requests
class MpesaPayment:

    def __init__(self):

        # Safaricom app credentials used to generate access token
        self.consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        self.consumer_secret = "amFbAoUByPV2rM5A"

        # Daraja B2C credentials
        self.initiator = "testapi"
        self.security_credential = "PPMASUVMORtu7gUEIBKFL+UPQDIKW/yEJnZ0F6rsocxI2rOIj5QJOM3u5kukzdwBy9kJtrcghpa8qPT4rDI5sobdhNstp1EVabfVql5BKsp25hUACi8bSBofWjx1M3YuWRQcjjFJvRJY+a0fsWAzlSuYVCxLj3Dgy8L+xKQ9S8teuvWNz6wazrON7T/bg4oQQJFoP0R0XxeNHgiKG+qdjJTecOfBAsk/FBZnIw+HaLBE3LvrGkbjZKIs2BS2SGME1iBplFjBVR1TMtDibuc04cUCD5PkRaqkyiSIAP6R+XCej+TMedCgb7InOlsxYdaJnFjThIw0zUaQC3jiivSA5A=="
        # Daraja endpoints
        self.token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        self.payment_url = "https://sandbox.safaricom.co.ke/mpesa/b2b/v1/paymentrequest"

        # Public HTTPS endpoint where Safaricom sends transaction results (Generated via ngrok)
        self.callback_url = "https://f28c-197-237-20-103.ngrok-free.app/api/cooperative/callback"

    def get_token(self):
        # Requests an OAuth2 temporary access token from Safaricom
        response = requests.get( self.token_url, auth=requests.auth.HTTPBasicAuth( self.consumer_key, self.consumer_secret))

        # Return only the token
        return response.json()["access_token"]

    def pay_farmer(self, phone, amount):
        # Get temporary token before making payment request
        token = self.get_token()

        # Data sent to Safaricom
        payload = {

            "Initiator": self.initiator,
            "SecurityCredential": self.security_credential,
            "CommandID": "BusinessPayToBulk",
            "Amount": amount,
            "PartyA": "600989",  # Cooperative Shortcode
            "PartyB": "600000",
            "SenderIdentifierType": "4",
            "RecieverIdentifierType": "4",
            "AccountReference": "MILK",
            "Requester": phone,     # Farmer phone number
            "Remarks": "Milk payment",
            "QueueTimeOutURL": self.callback_url,
            "ResultURL": self.callback_url
        }

        # Send payment request to Daraja
        response = requests.post(self.payment_url, json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type":"application/json"
            }
        )


        # Give Django the Safaricom response
        return response.json()
   
