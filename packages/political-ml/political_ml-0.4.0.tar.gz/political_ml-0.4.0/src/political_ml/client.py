import logging
import uuid
from os.path import join

import requests

from political_ml.__meta__ import __version__
from political_ml.utils import check_payload_format, to_json

logger = logging.getLogger(__name__)


class _BaseClient:
    def __init__(self, endpoint: str, token: str, timeout: int = 15):
        """
        :param endpoint: the https endpoint to do NER requests to
        :param token: the token to authenticate with the endpoint
        :param timeout: a timeout - in seconds - which determines when the https call will timeout
        """
        self._endpoint = endpoint
        self._token = token
        self.timeout = timeout

    def exec_request(self, method, url, **kwargs):
        """ Executes a request, assigning a unique id beforehand and throwing on 4xx / 5xx """
        reqid = str(uuid.uuid4())

        logging.debug(
            f"{self.__class__.__qualname__} -> {method.upper()} {url} {reqid=}"
        )

        # requests.post / requests.get / ...
        method_exec = getattr(
            requests, method.lower()
        )  # retrieves the right method from requests

        headers = self._build_headers()
        response = method_exec(url, headers=headers, timeout=self.timeout, **kwargs)

        status_code = response.status_code
        content_length = len(response.content or "")
        logging.debug(
            f"{self.__class__.__qualname__} <- {status_code} {content_length} {reqid=}"
        )

        if response.status_code >= 300:
            logging.debug(response.json())

        # raise by default to halt further exec and bubble
        response.raise_for_status()

        return to_json(response)

    def build_url(self, *paths):
        return join(self._endpoint, *paths)

    def _build_headers(self):
        return {
            "Accept": "application/json",
            "User-Agent": f"Political ML Python package {__version__}",
            "Authorization": f"Bearer {self._token}",
        }


class NerClient(_BaseClient):
    def ner(self, payload) -> list:
        check_payload_format(payload)
        response = self.exec_request(
            method="POST",
            url=self.build_url("api/v1/ner"),
            json=payload,
        )
        return response or []


class CategoriseClient(_BaseClient):
    def categorise(self, payload) -> list:
        check_payload_format(payload)
        response = self.exec_request(
            method="POST",
            url=self.build_url("api/v1/categorise"),
            json=payload,
        )
        return response or []


class ArticleExtractionClient(_BaseClient):
    def by_url(self, url: str, clean: bool = True) -> dict:
        assert type(url) == str, "Url must be a string"
        payload = {"url": url}
        response = self.exec_request(
            method="POST",
            url=self.build_url(f"extract/url?clean={clean}"),
            json=payload,
        )
        return response or {}

    def by_html(self, html: str, clean: bool = True) -> dict:
        assert type(html) == str, "Html must be a string"
        payload = {"html": html}
        response = self.exec_request(
            method="POST",
            url=self.build_url(f"extract/html?clean={clean}"),
            json=payload,
        )
        return response or {}
