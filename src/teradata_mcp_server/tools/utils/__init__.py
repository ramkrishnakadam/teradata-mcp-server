"""Utilities for Teradata tools package.

Exposes helper functions used across tools implementations. This package
replaces the older single-module utils.py to avoid name conflicts and to group
protocol-agnostic helpers together.
"""

from __future__ import annotations

import base64
import hashlib
import json
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional

from .queryband import build_queryband, sanitize_qb_value  # noqa: F401


# -------------------- Serialization & response helpers -------------------- #
def serialize_teradata_types(obj: Any) -> Any:
    """Convert Teradata-specific types to JSON serializable formats."""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    return str(obj)


def rows_to_json(cursor_description: Any, rows: list[Any]) -> list[dict[str, Any]]:
    """Convert DB rows into JSON objects using column names as keys."""
    if not cursor_description or not rows:
        return []
    columns = [col[0] for col in cursor_description]
    out: list[dict[str, Any]] = []
    for row in rows:
        out.append({col: serialize_teradata_types(val) for col, val in zip(columns, row)})
    return out


def create_response(data: Any, metadata: dict[str, Any] | None = None, error: dict[str, Any] | None = None) -> str:
    """Create a standardized JSON response structure."""
    if error:
        resp = {"status": "error", "message": error}
        if metadata:
            resp["metadata"] = metadata
        return json.dumps(resp, default=serialize_teradata_types)
    resp = {"status": "success", "results": data}
    if metadata:
        resp["metadata"] = metadata
    return json.dumps(resp, default=serialize_teradata_types)


# ------------------------------ Auth helpers ------------------------------ #
def parse_auth_header(auth_header: Optional[str]) -> tuple[str, str]:
    """Parse an HTTP Authorization header into (scheme, value).

    Returns ("", "") if header is missing or malformed. Scheme is lowercased
    and stripped. Value is stripped (but not decoded).
    """
    if not auth_header:
        return "", ""
    try:
        scheme, _, value = auth_header.partition(" ")
        return scheme.strip().lower(), value.strip()
    except Exception:
        return "", ""


def compute_auth_token_sha256(auth_header: Optional[str]) -> Optional[str]:
    """Return a hex SHA-256 over the value portion of Authorization header."""
    scheme, value = parse_auth_header(auth_header)
    if not value:
        return None
    try:
        h = hashlib.sha256()
        h.update(value.encode("utf-8"))
        return h.hexdigest()
    except Exception:
        return None


def parse_basic_credentials(b64_value: str) -> tuple[Optional[str], Optional[str]]:
    """Decode a Basic credential value into (username, secret)."""
    try:
        raw = base64.b64decode(b64_value).decode("utf-8")
        if ":" not in raw:
            return None, None
        user, secret = raw.split(":", 1)
        user = user.strip()
        secret = secret.strip()
        if not user or not secret:
            return None, None
        return user, secret
    except Exception:
        return None, None


def infer_logmech_from_header(auth_header: Optional[str], default_basic_logmech: str = "LDAP") -> tuple[str, str]:
    """Infer LOGMECH and the credential payload based on the header.

    Returns (logmech, payload) where:
      - If scheme == 'bearer' → ("JWT", <token>)
      - If scheme == 'basic'  → (default_basic_logmech, <secret>)
      - Otherwise → ("", "")
    """
    scheme, value = parse_auth_header(auth_header)
    if scheme == "bearer" and value:
        return "JWT", value
    if scheme == "basic" and value:
        return default_basic_logmech.upper(), value
    return "", ""


# ----------------------- SQL Security Validation ----------------------- #
import logging
import os
import re

logger = logging.getLogger("teradata_mcp_server")


class SQLValidationError(Exception):
    """Raised when SQL query fails validation checks"""
    pass


def validate_sql(sql: str) -> None:
    """
    Validate SQL query to prevent dangerous operations.
    
    Raises:
        SQLValidationError: If the SQL contains prohibited operations
    """
    if not sql or not sql.strip():
        raise SQLValidationError("Empty SQL query not allowed")
    
    # Convert to uppercase for case-insensitive matching
    sql_upper = sql.upper().strip()
    sql_normalized = re.sub(r'\s+', ' ', sql_upper)  # Normalize whitespace
    
    # Check if SQL validation is disabled via environment variable
    if os.getenv("DISABLE_SQL_VALIDATION", "false").lower() == "true":
        logger.warning("SQL validation is DISABLED - this is a security risk!")
        return
    
    # Define dangerous operations that should be blocked
    dangerous_keywords = [
        'UPDATE', 'DELETE', 'INSERT', 'DROP', 'CREATE', 'ALTER', 'TRUNCATE', 
        'MERGE', 'REPLACE', 'GRANT', 'REVOKE', 'CALL', 'EXECUTE'
    ]
    
    # Check for dangerous keywords at statement boundaries
    for keyword in dangerous_keywords:
        # Look for keyword at start of statement or after semicolon
        patterns = [
            rf'^{keyword}\s',           # At start of query
            rf';\s*{keyword}\s',        # After semicolon
            rf'^{keyword}$',            # Standalone keyword
            rf';\s*{keyword}$'          # After semicolon at end
        ]
        
        for pattern in patterns:
            if re.search(pattern, sql_normalized):
                raise SQLValidationError(f"Operation '{keyword}' is not allowed for security reasons")
    
    # Block SELECT * without WHERE clause to prevent full table scans
    # Allow exceptions for system tables and small utility queries
    if re.search(r'^SELECT\s+\*\s+FROM', sql_normalized):
        # Check if there's a WHERE clause
        if not re.search(r'\bWHERE\b', sql_normalized):
            # Allow exceptions for system catalogs and limited queries
            system_table_patterns = [
                r'FROM\s+DBC\.',           # DBC system tables
                r'FROM\s+INFORMATION_SCHEMA\.',  # Information schema
                r'TOP\s+\d+',              # Queries with TOP clause
                r'SAMPLE\s+\d+',           # Queries with SAMPLE clause
            ]
            
            is_system_query = any(re.search(pattern, sql_normalized) for pattern in system_table_patterns)
            
            if not is_system_query:
                raise SQLValidationError(
                    "SELECT * without WHERE clause is not allowed. "
                    "Use specific columns or add a WHERE clause to limit results."
                )
    
    # Block potentially dangerous functions
    dangerous_functions = [
        'EXEC', 'EXECUTE', 'SP_', 'XP_'  # Stored procedures
    ]
    
    for func in dangerous_functions:
        if re.search(rf'\b{func}\b', sql_normalized):
            raise SQLValidationError(f"Function '{func}' is not allowed for security reasons")
    
    # Warn about queries that might return large result sets
    large_result_indicators = [
        r'SELECT\s+\*.*FROM.*(?!.*LIMIT|.*TOP|.*SAMPLE|.*WHERE)',
        r'COUNT\(\*\).*FROM.*(?!.*WHERE)',
    ]
    
    for pattern in large_result_indicators:
        if re.search(pattern, sql_normalized):
            logger.warning(f"Query may return large result set: {sql[:100]}...")
    
    logger.info(f"SQL validation passed for query: {sql[:100]}{'...' if len(sql) > 100 else ''}")

