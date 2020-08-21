import requests
from django.conf import settings
from django.utils import timezone

WAVECELL_BRAND = getattr(settings, 'WAVECELL_BRAND', 'MyBrand')
WAVECELL_API_KEY = getattr(settings, "WAVECELL_API_KEY")
WAVECELL_SUB_ACC_OTP = getattr(settings, "WAVECELL_SUB_ACC_OTP")
WAVECELL_SUB_ACC_NOTIF = getattr(settings, "WAVECELL_SUB_ACC_NOTIF")
DEFAULT_VERIFY_TEMPLATE = "JAGA KERAHASIAAN ANDA, KODE TIDAK UNTUK DIBAGIKAN. Kode RAHASIA anda untuk %s adalah {code}" % WAVECELL_BRAND
VERIFY_TEMPLATE = getattr(settings, 'VERIFY_TEMPLATE', DEFAULT_VERIFY_TEMPLATE)

URL = "https://api.wavecell.com/{}/{}/"


class Wavecell(object):
    def __init__(self):
        # validate key
        if (
            not WAVECELL_API_KEY
            or not WAVECELL_SUB_ACC_OTP
            or not WAVECELL_SUB_ACC_NOTIF
        ):
            raise Exception(
                "%s is required. Please put at settings."
                % (
                    "WAVECELL_SUB_ACC_OTP"
                    if not WAVECELL_SUB_ACC_OTP
                    else (
                        "WAVECELL_API_KEY"
                        if not WAVECELL_API_KEY
                        else "WAVECELL_SUB_ACC_NOTIF"
                    )
                )
            )

        self.headers = {"Authorization": "Bearer %s" % WAVECELL_API_KEY}

    def request_otp(self, phone_number, brand=WAVECELL_BRAND):
        url = URL.format("verify/v2", WAVECELL_SUB_ACC_OTP)
        headers = self.headers
        body = {
            "destination": "%s" % phone_number,
            "brand": brand,
            "codeLength": 6,
            "template": VERIFY_TEMPLATE,
            "codeType": "NUMERIC",
            "channel": "sms",
            "sms": {"source": brand, "encoding": "AUTO"},
        }

        return requests.post(url, headers=headers, json=body)

    def verify_otp(self, session_id, code):
        headers = self.headers
        url = URL.format("verify/v2", WAVECELL_SUB_ACC_OTP)
        verify_url = "{}{}?code={}".format(url, session_id, code)

        return requests.get(verify_url, headers=headers)

    def send_single_sms(self, phone_number, text, brand=WAVECELL_BRAND):
        """ Sending single SMS by phone number

        Args:
            phone_number (string): Phone want to send, please always put country code
            text (string): SMS text (content)
            brand (str, optional): Brand or name will be show on SMS sender. Defaults to MyBrand.
        """
        headers = self.headers
        url = URL.format("sms/v1", WAVECELL_SUB_ACC_NOTIF) + "single"

        body = {"destination": "%s" % phone_number, "text": text, "source": brand}

        return requests.post(url, headers=headers, json=body)

    def send_batch_sms(
        self, messages, text_template, brand=WAVECELL_BRAND, *args, **kwargs
    ):
        """ Sending batch sms with customize properties.

        Args:
            messages (array object): Every object must contains key "destination" and "text"
                example: 
                message = [
                    {
                        "destination": "62811222334455",
                        "text": "Dear, John Doe. You will be get discount 10% if you donate at 10PM"
                    },
                    {
                        "destination": "62811222334466",
                        "text": "Dear, Cooler John Doe. You will be get discount 10% if you donate at 10PM"
                    }
                ] 

            text_template (if text are same): Default template.
                example:
                text_template = "Dear Customer, You will be get discount 10% if you donate at 10PM"

            brand (str, optional): SenderId. Defaults to "MyBarand".

        Returns:
            response: HTTP Response
        """

        headers = self.headers
        url = URL.format("sms/v1", WAVECELL_SUB_ACC_NOTIF) + "many"

        body = {
            "messages": messages,
            "template": {"source": brand, "text": text_template, "encoding": "AUTO",},
        }

        # able to use schedule
        if kwargs.get("scheduled_at"):
            body["template"]["scheduled"] = kwargs.get("scheduled_at", timezone.now())

        return requests.post(url, headers=headers, json=body)

    def send_batch_sms_compact(
        self, destinations, text_template, brand=WAVECELL_BRAND, *args, **kwargs
    ):
        """ Sending batch sms, but can't custom message every recipient

        Args:
            destinations (array string): List of recipients
            text_template (string): Message want to send. Example: "Donate min Rp10.000 at 25 May 2020 to get free GoJek Voucher"
            brand (str, optional): SenderId. Defaults to "MyBrand".

        Returns:
            response: HTTP Response
        """
        headers = self.headers
        url = URL.format("sms/v1", WAVECELL_SUB_ACC_NOTIF) + "many/compact"

        body = {
            "destinations": destinations,
            "template": {"source": brand, "text": text_template, "encoding": "AUTO",},
        }

        # able to use schedule
        if kwargs.get("scheduled_at"):
            body["template"]["scheduled"] = kwargs.get("scheduled_at", timezone.now())

        return requests.post(url, headers=headers, json=body)

