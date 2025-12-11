import time
from typing import Optional, Tuple
import requests
from .config_loader import get_env_var


class TokenProvider:
    """Handles OAuth client credentials and token caching."""

    def __init__(self, token_url: str, client_id_env: str, client_secret_env: str):
        self.token_url = token_url
        self.client_id_env = client_id_env
        self.client_secret_env = client_secret_env
        self._cached_token: Optional[str] = None
        self._expires_at: Optional[float] = None

    def _request_new_token(self) -> Tuple[str, float]:
        cid = get_env_var(self.client_id_env, required=True)
        secret = get_env_var(self.client_secret_env, required=True)
        resp = requests.post(
            self.token_url,
            data={"grant_type": "client_credentials"},
            auth=(cid, secret),
            timeout=5
        )
        resp.raise_for_status()
        data = resp.json()
        token = data["access_token"]
        expires_in = data.get("expires_in", 3600)
        return token, time.time() + expires_in - 30

    def get_token(self) -> str:
        override = get_env_var("SCIM_TOKEN_OVERRIDE")
        if override:
            return override

        if (
            not self._cached_token
            or not self._expires_at
            or time.time() >= self._expires_at
        ):
            token, exp = self._request_new_token()
            self._cached_token = token
            self._expires_at = exp

        return self._cached_token
