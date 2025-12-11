  # Python IAM Training Project

  An enterprise-style Identity & Access Management (IAM) training project that demonstrates user provisioning, OAuth2 client credentials authentication, SCIM style payload generation, and API communication in Python.

  ## Overview
  This project models an IAM provisioning pipeline:
    - Retrieve users from a MySQL identity store
    - Acquire and cache OAuth2 access tokens
    - Construct SCIM compatible user payloads
    - Send updates to an external API with retry, backoff, and session reuse
  The structure reflects real IAM engineering practices: modular components, configuration-driven setup, token lifecycle control, and production-grade HTTP handling.

  ## Project Layout
    src/
      auth.py            # OAuth token provider
      api_client.py      # HTTP client with retries
      config_loader.py   # Env + YAML configuration
      db/                # MySQL data layer
      provisioning/      # SCIM mapping and sync logic
      main.py            # Entry point
    scripts/
      init_db.py         # Database bootstrap
    config/
      config.yaml

  ## Quick Start
  1. Install dependencies:
      python3 -m venv .venv
      source .venv/bin/activate
      pip install -r requirements.txt

  2. Configure environment:
      cp .env.example .env

  3. Prepare MySQL:
      CREATE DATABASE iam_db;
      CREATE USER 'iam_user'@'%' IDENTIFIED BY 'iam_password';
      GRANT ALL PRIVILEGES ON iam_db.* TO 'iam_user'@'%';

     Initialize sample data:
      python scripts/init_db.py

  4. Run provisioning:
      python -m src.main

  ## Capabilities
    - OAuth2 client-credential token acquisition and caching
    - Resilient API communication (retry, backoff, session pooling)
    - SCIM-style user payload generation
    - Clear separation of concerns: config, DB, auth, HTTP, provisioning
    - Logging patterns suitable for observability and troubleshooting


