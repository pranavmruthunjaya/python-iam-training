import os
import sys

# Add project root (python-iam-training) to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
    
from src.db.mysql_db import get_connection, init_schema, insert_user
def main():
    conn = get_connection()
    init_schema(conn)
    insert_user(conn, "alice@example.com", "Alice", "Doe", True)
    insert_user(conn, "bob@example.com", "Bob", "Smith", True)
    conn.close()
if __name__ == "__main__":
    main()