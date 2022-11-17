from django.conf import settings
from twilio.rest import Client
import random

                            # .services('VAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') \

class messageHandler:
    phone_number = None
    def __init__(self,phone_number) -> None:
        self.phone_number = phone_number
        # self.otp = otp
    def send_otp_on_phone(self):
        client = Client(settings.ACCOUNT_SID,settings.ACCOUNT_SECURITY_API_KEY)

        verification = client.verify \
                             .v2 \
                             .services('VA6e4c6e36e255e57c4c173f4046296036') \
                             .verifications \
                             .create(to=self.phone_number, channel='sms')
    def validate(self,otp):
        client = Client(settings.ACCOUNT_SID,settings.ACCOUNT_SECURITY_API_KEY)


        verification_check = client.verify \
                                .v2 \
                                .services('VA6e4c6e36e255e57c4c173f4046296036') \
                                .verification_checks \
                                .create(to=self.phone_number, code=otp)

        print(verification_check.status)
        return verification_check.status