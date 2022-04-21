import os
from twilio.rest import Client

TWILIO_ACCOUNT_SID='ACaac7876c9dd88571de990f5b39525293'
TWILIO_AUTH_TOKEN='0e360095573216920584fd6889182934'

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'ACaac7876c9dd88571de990f5b39525293'
auth_token = '0e360095573216920584fd6889182934'
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='This is the ship that made the Kessel Run in fourteen parsecs?',
         from_='+19377293887',
         to='+918341885927'
     )

print(message.sid)
