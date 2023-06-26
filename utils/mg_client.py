
import requests


class MGClient:

    def __init__(self, api_url, api_key, sender):
        self._mg_endpoint = api_url
        self._api_key = api_key
        self._sender = sender

    def send_mail(self, to, subject, body, html=None):
        return requests.post(
            self._mg_endpoint,
            auth=("api", self._api_key),
            data={"from": self._sender, "to": to, "subject": subject, "text": body, "html": html}
        )
