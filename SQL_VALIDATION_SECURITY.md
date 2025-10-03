# SQL Validation Security Feature

## Overview

The Teradata MCP server now includes SQL validation logic in the `base_readQuery` tool to prevent potentially dangerous SQL operations. This feature helps protect against:

- Data modification attacks (UPDATE, DELETE, INSERT)
- Schema changes (CREATE, DROP, ALTER, TRUNCATE)
- Full table scans without WHERE clauses
- Execution of stored procedures and system commands
- SQL injection attempts

## What's Protected

### Blocked Operations
The following SQL operations are completely blocked:
- `UPDATE` - Data modification
- `DELETE` - Data deletion
- `INSERT` - Data insertion
- `DROP` - Object deletion
- `CREATE` - Object creation
- `ALTER` - Schema modification
- `TRUNCATE` - Table truncation
- `MERGE` - Data merging
- `REPLACE` - Data replacement
- `GRANT`/`REVOKE` - Permission changes
- `CALL`/`EXECUTE` - Procedure execution
- `EXEC`/`SP_`/`XP_` - System procedures

### SELECT * Restrictions
- `SELECT *` without `WHERE` clause is blocked for user tables
- Exceptions allowed for:
  - System tables (DBC.*)
  - Information schema tables
  - Queries with `TOP` clause
  - Queries with `SAMPLE` clause

## Configuration

### Disabling Validation (NOT RECOMMENDED)
You can disable SQL validation by setting an environment variable:

```bash
export DISABLE_SQL_VALIDATION=true
```

**⚠️ WARNING**: Disabling SQL validation removes all protection and is a significant security risk.

### Error Handling
When a query fails validation:
- The query is NOT executed
- An error message is returned explaining why it was blocked
- The incident is logged for security monitoring
- The original SQL is truncated in the response for security

## Examples

### ✅ Allowed Queries
```sql
-- System table access
SELECT * FROM dbc.dbcinfo;

-- Specific columns with WHERE
SELECT name, email FROM users WHERE id = 1;

-- Limited result sets
SELECT TOP 10 * FROM orders;

-- Aggregates with filters
SELECT COUNT(*) FROM products WHERE category = 'electronics';

-- SELECT * with WHERE clause
SELECT * FROM customers WHERE country = 'USA';
```

### ❌ Blocked Queries
```sql
-- Data modification
UPDATE users SET password = 'hacked';

-- Data deletion
DELETE FROM orders;

-- Schema changes
DROP TABLE sensitive_data;

-- Full table scans
SELECT * FROM large_table;

-- System procedures
EXEC xp_cmdshell 'dangerous_command';

-- SQL injection
SELECT * FROM users; DROP TABLE users;
```

## Security Benefits

1. **Prevents Data Loss**: Blocks DELETE and TRUNCATE operations
2. **Prevents Data Modification**: Blocks UPDATE and INSERT operations
3. **Prevents Schema Changes**: Blocks CREATE, DROP, ALTER operations
4. **Prevents System Access**: Blocks stored procedure execution
5. **Prevents Performance Issues**: Blocks unrestricted SELECT * queries
6. **Audit Trail**: All blocked attempts are logged

## Implementation Details

The validation occurs in `handle_base_readQuery()` before the SQL is executed:

1. **Input Validation**: Checks for empty/null queries
2. **Keyword Detection**: Uses regex to detect dangerous operations
3. **Context Analysis**: Allows system table access and limited queries
4. **Error Response**: Returns structured error without executing query
5. **Logging**: Records all validation failures for monitoring

## Testing

Run the validation test suite:

```bash
python3 test_sql_validation_standalone.py
```

This tests various SQL patterns to ensure the validation logic works correctly.

## Monitoring

Monitor blocked queries using Teradata's DBQL:

```sql
-- Check for validation failures in application logs
SELECT 
    getQueryBandValue(QueryBand, 0, 'TOOL_NAME') as tool_name,
    getQueryBandValue(QueryBand, 0, 'AUTH_HASH') as user_hash,
    QueryText,
    StartTime
FROM dbc.qrylog 
WHERE getQueryBandValue(QueryBand, 0, 'APPLICATION') = 'teradata-mcp-server'
    AND UPPER(QueryText) LIKE '%SQL VALIDATION FAILED%'
ORDER BY StartTime DESC;
```

## Additional Security Recommendations

While SQL validation provides significant protection, also consider:

1. **Database Permissions**: Grant minimal required privileges to the MCP user
2. **Authentication**: Enable authentication (`AUTH_MODE=basic` or `AUTH_MODE=oauth`)
3. **Network Security**: Use HTTPS and restrict network access
4. **Service Account**: Use proxy users with `GRANT CONNECT THROUGH`
5. **Monitoring**: Set up alerts for validation failures

## Backwards Compatibility

This is a breaking change that may block previously allowed queries. If you need to temporarily allow dangerous operations:

1. Set `DISABLE_SQL_VALIDATION=true` (not recommended)
2. Use specific tools instead of `base_readQuery`
3. Grant appropriate database permissions and use direct SQL tools

## Support

For questions about SQL validation:

1. Check the validation error message for specific guidance
2. Review the allowed vs blocked query examples above
3. Consider using more specific MCP tools instead of raw SQL
4. Ensure your use case genuinely requires the blocked operation