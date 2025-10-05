#!/usr/bin/env python3
"""
Security Test Script for SQL Validation
Tests that DELETE and other dangerous operations are properly blocked
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.teradata_mcp_server.tools.utils import validate_sql, SQLValidationError

def test_delete_blocking():
    """Test that DELETE statements are blocked in various forms"""
    
    delete_statements = [
        "DELETE FROM table1",
        "delete from table1 where id=1",
        "  DELETE FROM database.table WHERE condition = 'value'  ",
        "DELETE FROM DB.table1",  # Your specific case
        "/* comment */ DELETE FROM table1",
        "SELECT * FROM table1; DELETE FROM table2",
        "WITH cte AS (SELECT * FROM table1) DELETE FROM table2",
        "(DELETE FROM table1)",
        "delete\nfrom\ntable1",
        "DELETE   FROM   table1",
        "UPSERT INTO table1 VALUES (1,2,3)",
        "MERGE INTO table1 USING table2 ON (condition)",
        "UPDATE table1 SET col1 = 'value'",
        "INSERT INTO table1 VALUES (1,2,3)",
        "DROP TABLE table1",
        "CREATE TABLE table1 (id INT)",
        "ALTER TABLE table1 ADD COLUMN col2 VARCHAR(50)",
        "TRUNCATE TABLE table1",
        "GRANT SELECT ON table1 TO user1",
        "REVOKE SELECT ON table1 FROM user1",
        "CALL procedure1()",
        "EXECUTE statement1",
    ]
    
    print("Testing DELETE and dangerous operation blocking...")
    
    blocked_count = 0
    failed_tests = []
    
    for i, sql in enumerate(delete_statements, 1):
        try:
            validate_sql(sql)
            # If we reach here, the validation failed to block the statement
            failed_tests.append(f"Test {i}: FAILED - Statement was not blocked: {sql[:50]}...")
        except SQLValidationError as e:
            # This is expected - the statement should be blocked
            blocked_count += 1
            print(f"✓ Test {i}: PASSED - Correctly blocked: {sql[:50]}...")
        except Exception as e:
            failed_tests.append(f"Test {i}: ERROR - Unexpected error: {str(e)} for: {sql[:50]}...")
    
    print(f"\nResults: {blocked_count}/{len(delete_statements)} statements correctly blocked")
    
    if failed_tests:
        print("\nFAILED TESTS:")
        for failure in failed_tests:
            print(f"❌ {failure}")
        return False
    else:
        print("✅ All dangerous operations were successfully blocked!")
        return True

def test_safe_statements():
    """Test that safe SELECT statements are allowed"""
    
    safe_statements = [
        "SELECT * FROM table1",
        "select id, name from table1 where id > 10",
        "WITH cte AS (SELECT * FROM table1) SELECT * FROM cte",
        "SELECT COUNT(*) FROM database.table1",
        "SELECT t1.*, t2.name FROM table1 t1 JOIN table2 t2 ON t1.id = t2.id",
    ]
    
    print("\nTesting safe SELECT statements...")
    
    allowed_count = 0
    failed_tests = []
    
    for i, sql in enumerate(safe_statements, 1):
        try:
            validate_sql(sql)
            allowed_count += 1
            print(f"✓ Test {i}: PASSED - Correctly allowed: {sql[:50]}...")
        except SQLValidationError as e:
            failed_tests.append(f"Test {i}: FAILED - Safe statement was blocked: {sql[:50]}... Error: {str(e)}")
        except Exception as e:
            failed_tests.append(f"Test {i}: ERROR - Unexpected error: {str(e)} for: {sql[:50]}...")
    
    print(f"\nResults: {allowed_count}/{len(safe_statements)} safe statements correctly allowed")
    
    if failed_tests:
        print("\nFAILED TESTS:")
        for failure in failed_tests:
            print(f"❌ {failure}")
        return False
    else:
        print("✅ All safe SELECT operations were correctly allowed!")
        return True

if __name__ == "__main__":
    print("=" * 60)
    print("SQL SECURITY VALIDATION TEST SUITE")
    print("=" * 60)
    
    test1_passed = test_delete_blocking()
    test2_passed = test_safe_statements()
    
    print("\n" + "=" * 60)
    if test1_passed and test2_passed:
        print("🎉 ALL TESTS PASSED - SQL validation is working correctly!")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED - SQL validation needs improvement!")
        sys.exit(1)