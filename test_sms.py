import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

message = client.messages.create(
    body="Secure Banking Test: Login approval request received.",
    from_=twilio_number,
    to="+919360278108"
)

print("SMS sent successfully!")
print("Message SID:", message.sid)