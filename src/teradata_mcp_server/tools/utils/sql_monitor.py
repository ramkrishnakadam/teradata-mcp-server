"""
Global SQL monitoring and security enforcement module.
This module provides comprehensive SQL interception and logging.
"""

import logging
import re
from typing import Any

logger = logging.getLogger("teradata_mcp_server.security")

class SQLSecurityMonitor:
    """
    Global SQL security monitor that intercepts and validates ALL SQL executions.
    This provides the final line of defense against dangerous operations.
    """
    
    @staticmethod
    def intercept_and_validate(sql: str, execution_context: str = "unknown") -> None:
        """
        Intercept and validate SQL before any execution.
        Raises SQLValidationError for dangerous operations.
        
        Args:
            sql: The SQL statement to validate
            execution_context: Description of where this SQL is being executed from
        """
        if not sql or not sql.strip():
            return
            
        # Normalize SQL for inspection
        sql_normalized = sql.upper().strip()
        sql_normalized = re.sub(r'\s+', ' ', sql_normalized)
        
        # Log ALL SQL executions for security audit
        logger.info(f"SQL_MONITOR [{execution_context}]: {sql[:200]}{'...' if len(sql) > 200 else ''}")
        
        # Critical security check - block dangerous operations
        dangerous_operations = [
            'DELETE', 'UPDATE', 'INSERT', 'DROP', 'CREATE', 'ALTER', 
            'TRUNCATE', 'MERGE', 'REPLACE', 'GRANT', 'REVOKE', 'UPSERT'
        ]
        
        for operation in dangerous_operations:
            # Multiple pattern checks to prevent bypass
            patterns = [
                rf'\b{operation}\s+',        # Word boundary + space
                rf'^{operation}\s+',         # Start of string
                rf';\s*{operation}\s+',      # After semicolon
                rf'\b{operation}\b',         # Word boundaries
            ]
            
            for pattern in patterns:
                if re.search(pattern, sql_normalized):
                    error_msg = f"SECURITY VIOLATION: Operation '{operation}' detected in SQL and BLOCKED"
                    logger.critical(f"{error_msg} - Context: {execution_context} - SQL: {sql[:100]}")
                    raise ValueError(error_msg)
        
        # Check for suspicious patterns that might indicate injection attempts
        suspicious_patterns = [
            r'EXEC\s*\(',
            r'EXECUTE\s*\(',
            r'SP_\w+',
            r'XP_\w+',
            r'--\s*DELETE',
            r'/\*.*DELETE.*\*/',
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, sql_normalized):
                error_msg = f"SECURITY WARNING: Suspicious pattern detected in SQL"
                logger.warning(f"{error_msg} - Context: {execution_context} - SQL: {sql[:100]}")

# Global function to be used throughout the codebase
def monitor_sql_execution(sql: str, context: str = "general") -> None:
    """
    Global SQL monitoring function.
    Call this before ANY SQL execution in the system.
    """
    SQLSecurityMonitor.intercept_and_validate(sql, context)