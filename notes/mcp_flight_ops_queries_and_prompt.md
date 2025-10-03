# MCP Flight Operations SQL Queries and Prompt Summary

---

## Conversation Prompt Summary (added September 1, 2025)

You are working with employee and flight operations data in a Teradata MCP server environment. The user may ask for:

- The number of flights delayed due to specific reasons (e.g., maintenance) on a given date.
- The total number of flights flown and delayed on a specific date.
- A breakdown of delayed flights by delay reason code, with counts for each code.
- A list of all questions previously asked about flight operations and baggage.
- Employment summaries for specific employees (e.g., Ramkrishna Kadam, Yashodhan Joshi, Phillip Waller), including department, manager, location, employment start date, and status.
- The active employee with the maximum service years.
- Details for any employee, using the `CERT_ORIONDBOPS_DB.AA_USR` table, referencing columns like FIRST_NAME, LAST_NAME, EMAIL_ADDR, DEPARTMENT, STATUS, VALID_DT, and manager information.

Always refer to the notes folder for context and use the correct SQL syntax for Teradata (e.g., use `TOP 1` instead of `LIMIT 1`). If a field like employment start date is unclear, check all relevant columns (e.g., VALID_DT, EDW_START_TSP).

---

## Prompt Summary

You are working with flight operations and baggage data in a Teradata MCP server environment. The user asked for:
- The status of flight 121 on August 24, 2025 (last week Sunday), including departure/arrival times and delays.
- The number of missing or delayed bags for that flight, using the `bags_CERT_Prep_db` database.
- The number of delayed flights on specific dates, and the total number of flights flown.
- A breakdown of delayed flights by delay duration buckets for August 30, 2025.
- The flight with the highest delay and its details.
- A categorization of delayed flights by delay reason code, and a request for explanations of those codes.
- Attempts to retrieve code explanations from reference tables, which were not found in the schema.

The conversation included SQL queries against tables like `CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG` and `bags_CERT_Prep_db.LOSS_DELAY_BAG_INCDNT`, and explored available reference tables for delay reason codes.

---

## SQL Queries Used

1. **Status of flight 121 on August 24, 2025:**
```sql
SELECT * FROM CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG WHERE ACTL_OPMETAL_FLIGHT_NBR = '121' AND ACTL_LEG_DEP_DT = '2025-08-24'
```

2. **Number of missing or delayed bags for the flight:**
```sql
SELECT SUM(BAG_CT) AS TOTAL_BAGS, INCDNT_STATUS_NM FROM bags_CERT_Prep_db.LOSS_DELAY_BAG_INCDNT WHERE TRACE_CREATE_DT = '2025-08-24' AND INCDNT_STATUS_NM IN ('MISSING','DELAYED') GROUP BY INCDNT_STATUS_NM
```

3. **Number of delayed flights on a specific date (example for August 31, 2025):**
```sql
SELECT COUNT(*) AS DELAYED_FLIGHTS FROM CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG WHERE ACTL_LEG_DEP_DT = '2025-08-31' AND DEP_DELAY_IND = 'Y'
```

4. **Number of delayed flights on August 30, 2025:**
```sql
SELECT COUNT(*) AS DELAYED_FLIGHTS FROM CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG WHERE ACTL_LEG_DEP_DT = '2025-08-30' AND DEP_DELAY_IND = 'Y'
```

5. **Total number of flights flown on August 30, 2025:**
```sql
SELECT COUNT(*) AS TOTAL_FLIGHTS FROM CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG WHERE ACTL_LEG_DEP_DT = '2025-08-30'
```

6. **Delayed flights by delay duration buckets:**
```sql
SELECT
  SUM(CASE WHEN LEG_TTL_DEP_DELAY_MINUTE_QTY > 0 AND LEG_TTL_DEP_DELAY_MINUTE_QTY < 15 THEN 1 ELSE 0 END) AS DELAY_LT_15,
  SUM(CASE WHEN LEG_TTL_DEP_DELAY_MINUTE_QTY >= 15 AND LEG_TTL_DEP_DELAY_MINUTE_QTY < 30 THEN 1 ELSE 0 END) AS DELAY_15_30,
  SUM(CASE WHEN LEG_TTL_DEP_DELAY_MINUTE_QTY >= 30 AND LEG_TTL_DEP_DELAY_MINUTE_QTY < 60 THEN 1 ELSE 0 END) AS DELAY_30_60,
  SUM(CASE WHEN LEG_TTL_DEP_DELAY_MINUTE_QTY >= 60 AND LEG_TTL_DEP_DELAY_MINUTE_QTY < 120 THEN 1 ELSE 0 END) AS DELAY_60_120,
  SUM(CASE WHEN LEG_TTL_DEP_DELAY_MINUTE_QTY >= 120 AND LEG_TTL_DEP_DELAY_MINUTE_QTY < 240 THEN 1 ELSE 0 END) AS DELAY_120_240,
  SUM(CASE WHEN LEG_TTL_DEP_DELAY_MINUTE_QTY >= 240 THEN 1 ELSE 0 END) AS DELAY_GT_240
FROM CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG
WHERE ACTL_LEG_DEP_DT = '2025-08-30' AND DEP_DELAY_IND = 'Y'
```

7. **Flight with the highest delay:**
```sql
SELECT TOP 1 ACTL_OPMETAL_FLIGHT_NBR, ACTL_OPMETAL_AIRLN_IATA_CD, ACTL_LEG_DEP_DT, LEG_TTL_DEP_DELAY_MINUTE_QTY
FROM CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG
WHERE ACTL_LEG_DEP_DT = '2025-08-30' AND DEP_DELAY_IND = 'Y'
ORDER BY LEG_TTL_DEP_DELAY_MINUTE_QTY DESC
```

8. **Details of the most delayed flight:**
```sql
SELECT * FROM CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG
WHERE ACTL_OPMETAL_FLIGHT_NBR = '3309' AND ACTL_OPMETAL_AIRLN_IATA_CD = 'AA    ' AND ACTL_LEG_DEP_DT = '2025-08-30'
```

9. **Delayed flights categorized by delay reason:**
```sql
SELECT LEG_INCDNT_PRIME_REASON_GRP_CD, COUNT(*) AS DELAYED_FLIGHTS
FROM CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG
WHERE ACTL_LEG_DEP_DT = '2025-08-30' AND DEP_DELAY_IND = 'Y'
GROUP BY LEG_INCDNT_PRIME_REASON_GRP_CD
ORDER BY DELAYED_FLIGHTS DESC
```

10. **Attempt to get delay reason code explanations:**
```sql
SELECT * FROM CERT_FLIGHT_OPERATIONS_VWS.DELAY_REASON_XREF
```
(And attempted, but failed due to missing tables:)
```sql
SELECT * FROM CERT_FLIGHT_OPERATIONS_VWS.LEG_INCDNT_REASON_GROUP
SELECT * FROM CERT_FLIGHT_OPERATIONS_VWS.LEG_INCDNT_REASON
```
