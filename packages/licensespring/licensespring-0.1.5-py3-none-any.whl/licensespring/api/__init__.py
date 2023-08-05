import requests
from licensespring.api.authorization import autorization_headers

from licensespring.api.error import HTTPClientError


class APIClient:
    def __init__(
        self, api_key, shared_key, api_domain="api.licensespring.com", api_version="v4"
    ):
        self.api_key = api_key
        self.shared_key = shared_key
        self.api_base = "https://{}/api/{}".format(api_domain, api_version)

    def api_url(self, endpoint):
        return "{}{}".format(self.api_base, endpoint)

    def request_headers(self, custom_headers={}):
        headers = {"Content-Type": "application/json"}
        authorization_headers = autorization_headers(self.api_key, self.shared_key)
        return {**headers, **authorization_headers, **custom_headers}

    def send_request(self, method, endpoint, params=None, data=None):
        response = requests.request(
            method=method,
            url=self.api_url(endpoint),
            headers=self.request_headers(),
            params=params,
            json=data,
        )
        if 400 <= response.status_code < 500:
            raise HTTPClientError(response)
        else:
            response.raise_for_status()
        return response.json()

    def activate_license(self, hardware_id, license_key, product):
        return self.send_request(
            method="post",
            endpoint="/activate_license",
            data={
                "hardware_id": hardware_id,
                "license_key": license_key,
                "product": product,
            },
        )

    def check_license(self, hardware_id, license_key, product):
        return self.send_request(
            method="get",
            endpoint="/check_license",
            params={
                "hardware_id": hardware_id,
                "license_key": license_key,
                "product": product,
            },
        )
