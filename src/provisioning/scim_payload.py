from typing import Dict, Any

def user_row_to_scim(row: dict) -> Dict[str, Any]:
    """Map a MySQL row dict to a SCIM-style user payload."""
    return {
        "userName": row["email"],
        "name": {
            "givenName": row["first_name"],
            "familyName": row["last_name"]
        },
        "active": bool(row["active"])
    }
