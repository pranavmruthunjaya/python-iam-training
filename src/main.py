from .logger import setup_logger
from .config_loader import load_yaml_config
from .auth import TokenProvider
from .api_client import ApiClient
from .db.mysql_db import get_connection
from .provisioning.user_sync import sync_users


def main() -> None:
    logger = setup_logger()

    cfg = load_yaml_config("config/config.yaml")

    token_provider = TokenProvider(
        token_url=cfg["auth"]["token_url"],
        client_id_env=cfg["auth"]["client_id_env"],
        client_secret_env=cfg["auth"]["client_secret_env"]
    )

    api_client = ApiClient(
        base_url=cfg["scim"]["base_url"],
        token_provider=token_provider,
        timeout_seconds=cfg["scim"]["timeout_seconds"],
        max_retries=cfg["sync"]["max_retries"]
    )

    conn = get_connection()

    logger.info("Starting user sync")
    sync_users(conn, api_client, cfg["scim"]["users_endpoint"])
    logger.info("User sync finished")

    conn.close()


if __name__ == "__main__":
    main()
