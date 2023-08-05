import base64
import hashlib
import hmac
import time
from wsgiref.handlers import format_date_time


def autorization_headers(api_key, shared_key):
    date_header = format_date_time(time.time())

    msg = "licenseSpring\ndate: {}".format(date_header)
    hashed = hmac.new(
        bytes(shared_key, "utf-8"), msg.encode("utf-8"), hashlib.sha256
    ).digest()
    signature = base64.b64encode(hashed).decode()
    auth = [
        'algorithm="hmac-sha256"',
        'headers="date"',
        'signature="{}"'.format(signature),
        'apiKey="{}"'.format(api_key),
    ]
    authorization = ",".join(auth)

    return {"Date": date_header, "Authorization": authorization}
