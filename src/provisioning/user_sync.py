import logging
from typing import Any
from .scim_payload import user_row_to_scim
from ..db.mysql_db import fetch_active_users

logger = logging.getLogger("iam-training")

def sync_users(conn: Any, api_client, users_endpoint: str) -> None:
    rows = list(fetch_active_users(conn))
    logger.info("Starting sync of %d active users", len(rows))

    success = 0
    failed = 0

    for row in rows:
        payload = user_row_to_scim(row)
        email = row["email"]

        try:
            resp = api_client.post(users_endpoint, payload)
            logger.info("Synced user %s, SCIM id %s", email, resp.get("id"))
            success += 1

        except Exception as e:
            logger.error("Failed to sync user %s: %s", email, e)
            failed += 1

    logger.info("Sync finished. Success: %d, Failed: %d", success, failed)
