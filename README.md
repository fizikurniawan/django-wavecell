# django-wavecell
A library to use wavecell

# Pull Request
Welcome to pull request.

# Installation
just `pip install -e git+https://github.com/fizikurniawan/django-wavecell#egg=wavecell` in your python environment

# Before Usage

Add variable to settings.py
- WAVECELL_BRAND - SMS SenderID
- WAVECELL_API_KEY - API Key got from wavecell dashboard
- WAVECELL_SUB_ACC_OTP - Subaccount to send OTP got from wavecell dashboard. Default subaccount has prefix `_hq`
- WAVECELL_SUB_ACC_NOTIF - Subaccount to send notification got from wavecell dashboard. Default subaccount has prefix `_hq`
- VERIFY_TEMPLATE - Template mobile verification.

Note:
You can use subaccount to WAVECELL_SUB_ACC_OTP and WAVECELL_SUB_ACC_NOTIF. I recommended to use transaction to OTP and promotion to NOTIF.

# Usage
### Sending OTP
```python
from wavecell import Wavecell

    def send_otp_code(self, request):
        phone_number = "628123456789"

        # instance wavecell
        wc = Wavecell()
        wc.request_otp(phone_number)

        ...
```

### Verify OTP
```python
from wavecell import Wavecell

    def verify_otp(self, request):
        session_id = request.POST.get('session_id')
        code = request.POST.get('code')

        # instance wavecell
        wc = Wavecell()
        verify = wc.verify_otp(session_id, code)

        if verify.status_code == 200:
            print('success')
        else:
            print('code and session id is invalid')
        
        ...
```
