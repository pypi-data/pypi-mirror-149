import hashlib
import hmac
import io
import logging
from datetime import datetime
from typing import Optional
from urllib.parse import urljoin

import requests

from . import errors
from .internal_utils import _modify_params_for_logging, get_user_agent
from .response import Response


class BaseClient:
    BASE_URL = "https://4zvgsgkj2i.execute-api.us-east-2.amazonaws.com"

    def __init__(
        self,
        token: str,
        callback_url: str,
        base_url: str = BASE_URL,
        timeout: int = 30,
        proxy: Optional[dict] = None,
        additional_headers: Optional[dict] = None,
        logger: Optional[logging.Logger] = None,
    ):
        self.token = token.strip()
        self.callback_url = callback_url
        self.base_url = base_url
        self.timeout = timeout
        self.proxy = proxy
        self.additional_headers = additional_headers or {}

        self._logger = logger if logger is not None else logging.getLogger(__name__)
        self.ALLOWED_HTTP_METHODS = ["GET", "POST"]

    def _build_auth_headers(
        self,
        token: str,
        request_id: str,
        has_json: bool,
        has_files: bool,
        app_id: str = None,
        program_id: str = None,
    ) -> dict:
        """
        Helper method to construct request headers
        Args:
            token: Authentication credentials to the Fraud Framework
            request_id: Reference ID to track your verification request
            has_json: Request body has been passed in order to update header with the correct `Content-Type`
            has_files: Request file has been passed in order to update header with the correct `Content-Type`
            app_id: Reference ID to track your verification request
            program_id: Reference ID to track your verification request
        Returns:
            Request Headers
        """
        headers = {
            "x-api-key": token,
            "x-request-id": request_id,
            "User-Agent": get_user_agent(),
        }
        if has_json:
            headers.update({"Content-Type": "application/json;charset=utf-8"})
        if has_files:
            headers.update({"Content-Type": "multipart/form-data"})
        if program_id:
            headers.update({"x-program-id": program_id})
        if app_id:
            headers.update({"x-app-id": app_id})
        if self.additional_headers:
            headers.update(self.additional_headers)
        return headers

    def _send_request(self, http_method, url, params, data, file, headers):
        """
        Abstracted out for easy mock-testing
        """
        return requests.request(
            method=http_method,
            url=url,
            params=params,
            json=data,
            files=dict(uploadFile=file),
            headers=headers,
            timeout=self.timeout,
            proxies=self.proxy,
        )

    def _api_call(
        self,
        endpoint: str,
        request_id: str,
        *,
        program_id: Optional[str] = None,
        app_id: Optional[str] = None,
        http_method: str = "POST",
        data: Optional[dict] = None,
        file: Optional[io.BytesIO] = None,
        params: Optional[dict] = None,
    ) -> Response:
        """Create a request and execute the API call to Fraud Framework.
        Args:
            endpoint (str): The target Fraud Framework API method.
                e.g. 'chat.postMessage'
            request_id: Reference ID to track your verification request
            program_id: Reference ID to track your verification request
            app_id: Reference ID to track your verification request
            http_method (str): HTTP method. e.g. 'POST'
            data: The body to attach to the request. If a dictionary is
                provided, form-encoding will take place.
                e.g. {'key1': 'value1', 'key2': 'value2'}
            file (bytes): File to multipart upload.
                e.g. file_object
            params (dict): The URL parameters to append to the URL.
                e.g. {'key1': 'value1', 'key2': 'value2'}
        Returns:
            (Response)
                The server's response to an HTTP request. Data
                from the response can be accessed like a dict.
        """
        if http_method not in self.ALLOWED_HTTP_METHODS:
            raise errors.FraudFrameworkRequestError(f"{http_method} method is not allowed")

        url = urljoin(self.base_url, endpoint)

        request_headers = self._build_auth_headers(
            token=self.token,
            request_id=request_id,
            program_id=program_id,
            app_id=app_id,
            has_json=data is not None,
            has_files=file is not None,
        )

        request_args = {
            "headers": request_headers,
            "params": params,
            "json": data,
            "files": file,
        }
        request_time = datetime.utcnow()

        if self._logger.level <= logging.DEBUG:
            redacted_headers = {
                k: "(redacted)" if k.lower() == "x-api-key" else v for k, v in request_headers.items()
            }
            self._logger.debug(
                f"Sending a request - url: {url}, "
                f"query_params: {_modify_params_for_logging(params)}, "
                f"json_body: {data}, "
                f"headers: {redacted_headers}"
            )

        response = self._send_request(
            http_method=http_method,
            url=url,
            params=params,
            data=data,
            files=file,
            headers=request_headers,
        )
        response_body = response.json()
        response_time = datetime.utcnow()

        return Response(
            client=self,
            http_method=http_method,
            api_url=url,
            req_args=request_args,
            data=response_body,
            headers=dict(response.headers),
            status_code=response.status_code,
            request_time=request_time,
            response_time=response_time,
        ).validate()

    @staticmethod
    def validate_signature(*, signing_secret: str, data: str, timestamp: str, signature: str) -> bool:
        """
        Args:
            signing_secret: Your application's signing secret
            data: The raw body of the incoming request - no headers, just the body.
            timestamp: from the response header
            signature: from the response header - the calculated signature
                should match this.
        Returns:
            True if signatures matches
        """
        format_req = str.encode(f"v0:{timestamp}:{data}")
        encoded_secret = str.encode(signing_secret)
        request_hash = hmac.new(encoded_secret, format_req, hashlib.sha256).hexdigest()
        calculated_signature = f"v0={request_hash}"
        return hmac.compare_digest(calculated_signature, signature)


class WebClient(BaseClient):
    def perform_risk_review(
        self,
        data,
        request_id,
        app_id=None,
        program_id=None,
        callback_url=None,
        **kwargs,
    ) -> Response:
        """
        Args:
            data: The raw body of the incoming request - no headers, just the body.
            request_id: Reference ID to track your verification request
            app_id: Reference ID to track your verification request
            program_id: Reference ID to track your verification request
            callback_url: Callback URL that the Fraud Framework will ping back.
            kwargs:
        Returns:
            Response object
        """
        kwargs.update({"callbackUrl": callback_url or self.callback_url})
        return self._api_call(
            "/risk/verify",
            data=data,
            request_id=request_id,
            app_id=app_id,
            program_id=program_id,
            params=kwargs,
        )

    def search_request_id(self, request_id, *args, **kwargs) -> Response:
        """
        Args:
            request_id: Reference ID to track your verification request
            kwargs: Extra query params that can be passed in the request
        Returns:
            Response object
        """
        return self._api_call(f"/risk/fetch/{request_id}", request_id, params=kwargs)

    def upload_document(self, request_id, file, *args, **kwargs) -> Response:
        """
        Args:
            request_id: Reference ID to track your verification request
            file: File object that will be sent for external upload
            kwargs: Extra query params that can be passed in the request
        Returns:
            Response object
        """
        return self._api_call(f"/document/upload/{request_id}", request_id, file=file, params=kwargs)
