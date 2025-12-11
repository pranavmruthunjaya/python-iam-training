from typing import Any, Dict, Iterable

import mysql.connector
from ..config_loader import get_env_var



def get_connection():
    host=get_env_var("MYSQL_HOST", required=True)
    port=get_env_var("MYSQL_PORT", default="3306")
    user=get_env_var("MYSQL_USER", required=True)
    password=get_env_var("MYSQL_PASSWORD", required=True)
    database=get_env_var("MYSQL_DATABASE", required=True)
    
    conn=mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    return conn

def init_schema(conn):
    ddl="""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        active TINYINT(1) NOT NULL DEFAULT 1,
        updated_at DATETIME NOT NULL
        )
        """
    cursor=conn.cursor()
    cursor.execute(ddl)
    conn.commit()
    cursor.close()
    
def insert_user(conn, email: str, first: str, last: str, active: bool = True) -> None:
    cursor=conn.cursor()
    insert_query="""
    INSERT INTO users (email, first_name, last_name, active, updated_at) VALUES (%s, %s, %s, %s, NOW())
    """
    cursor.execute(insert_query, (email, first, last, 1 if active else 0))
    conn.commit()
    cursor.close()
    
def fetch_users(conn)->Iterable[Dict[str, Any]]:
    cursor=conn.cursor(dictionary=True)
    fetch_query="""
    SELECT * FROM users WHERE active = 1
    """
    cursor.execute(fetch_query)
    rows=cursor.fetchall()
    cursor.close()
    return rows

def deactivate_user(conn, email: str):
    cursor=conn.cursor()
    deactivate_query="""
    UPDATE users SET active = 0, updated_at = NOW() WHERE email = %s
    """
    cursor.execute(deactivate_query, (email))
    conn.commit()
    cursor.close()
    
    