from typing import Any, Dict
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger("iam-training")


class ApiClient:
    def __init__(self, base_url: str, token_provider, timeout_seconds: int, max_retries: int):
        self.base_url = base_url.rstrip("/")
        self.token_provider = token_provider
        self.timeout = timeout_seconds

        self.session = requests.Session()

        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PATCH"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _headers(self) -> Dict[str, str]:
        token = self.token_provider.get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def post(self, path: str, json_body: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"

        resp = self.session.post(
            url,
            headers=self._headers(),
            json=json_body,
            timeout=self.timeout
        )

        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            logger.error(
                "POST %s failed with status %s: %s",
                url,
                resp.status_code,
                e
            )
            raise

        return resp.json()
