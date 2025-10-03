"""
Tool: CERT_flight_operations_vws
This tool provides access to flight operations and employee data for American Airlines, based on the prompt and SQL queries in mcp_flight_ops_queries_and_prompt.md.
"""

import logging
from teradatasql import TeradataConnection
from teradata_mcp_server.tools.utils import create_response

logger = logging.getLogger("teradata_mcp_server")

def get_flight_status(conn: TeradataConnection, flight_number: str, flight_date: str):
    sql = f"""
    SELECT * FROM CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG 
    WHERE ACTL_OPMETAL_FLIGHT_NBR = '{flight_number}' AND ACTL_LEG_DEP_DT = '{flight_date}'
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "get_flight_status"})

def get_bag_status(conn: TeradataConnection, flight_date: str):
    sql = f"""
    SELECT SUM(BAG_CT) AS TOTAL_BAGS, INCDNT_STATUS_NM 
    FROM bags_CERT_Prep_db.LOSS_DELAY_BAG_INCDNT 
    WHERE TRACE_CREATE_DT = '{flight_date}' AND INCDNT_STATUS_NM IN ('MISSING','DELAYED') 
    GROUP BY INCDNT_STATUS_NM
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "get_bag_status"})

def get_delayed_flights_count(conn: TeradataConnection, flight_date: str):
    sql = f"""
    SELECT COUNT(*) AS DELAYED_FLIGHTS 
    FROM CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG 
    WHERE ACTL_LEG_DEP_DT = '{flight_date}' AND DEP_DELAY_IND = 'Y'
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    return create_response({"DELAYED_FLIGHTS": row[0]}, {"tool_name": "get_delayed_flights_count"})

def get_total_flights_count(conn: TeradataConnection, flight_date: str):
    sql = f"""
    SELECT COUNT(*) AS TOTAL_FLIGHTS 
    FROM CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG 
    WHERE ACTL_LEG_DEP_DT = '{flight_date}'
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    return create_response({"TOTAL_FLIGHTS": row[0]}, {"tool_name": "get_total_flights_count"})

def get_delay_buckets(conn: TeradataConnection, flight_date: str):
    sql = f"""
    SELECT
      SUM(CASE WHEN LEG_TTL_DEP_DELAY_MINUTE_QTY > 0 AND LEG_TTL_DEP_DELAY_MINUTE_QTY < 15 THEN 1 ELSE 0 END) AS DELAY_LT_15,
      SUM(CASE WHEN LEG_TTL_DEP_DELAY_MINUTE_QTY >= 15 AND LEG_TTL_DEP_DELAY_MINUTE_QTY < 30 THEN 1 ELSE 0 END) AS DELAY_15_30,
      SUM(CASE WHEN LEG_TTL_DEP_DELAY_MINUTE_QTY >= 30 AND LEG_TTL_DEP_DELAY_MINUTE_QTY < 60 THEN 1 ELSE 0 END) AS DELAY_30_60,
      SUM(CASE WHEN LEG_TTL_DEP_DELAY_MINUTE_QTY >= 60 AND LEG_TTL_DEP_DELAY_MINUTE_QTY < 120 THEN 1 ELSE 0 END) AS DELAY_60_120,
      SUM(CASE WHEN LEG_TTL_DEP_DELAY_MINUTE_QTY >= 120 AND LEG_TTL_DEP_DELAY_MINUTE_QTY < 240 THEN 1 ELSE 0 END) AS DELAY_120_240,
      SUM(CASE WHEN LEG_TTL_DEP_DELAY_MINUTE_QTY >= 240 THEN 1 ELSE 0 END) AS DELAY_GT_240
    FROM CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG
    WHERE ACTL_LEG_DEP_DT = '{flight_date}' AND DEP_DELAY_IND = 'Y'
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]
    return create_response(dict(zip(columns, row)), {"tool_name": "get_delay_buckets"})

def get_most_delayed_flight(conn: TeradataConnection, flight_date: str):
    sql = f"""
    SELECT TOP 1 ACTL_OPMETAL_FLIGHT_NBR, ACTL_OPMETAL_AIRLN_IATA_CD, ACTL_LEG_DEP_DT, LEG_TTL_DEP_DELAY_MINUTE_QTY
    FROM CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG
    WHERE ACTL_LEG_DEP_DT = '{flight_date}' AND DEP_DELAY_IND = 'Y'
    ORDER BY LEG_TTL_DEP_DELAY_MINUTE_QTY DESC
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]
    return create_response(dict(zip(columns, row)), {"tool_name": "get_most_delayed_flight"})

def get_flight_details(conn: TeradataConnection, flight_number: str, airline_code: str, flight_date: str):
    sql = f"""
    SELECT * FROM CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG
    WHERE ACTL_OPMETAL_FLIGHT_NBR = '{flight_number}' AND ACTL_OPMETAL_AIRLN_IATA_CD = '{airline_code}' AND ACTL_LEG_DEP_DT = '{flight_date}'
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "get_flight_details"})

def get_delays_by_reason(conn: TeradataConnection, flight_date: str):
    sql = f"""
    SELECT LEG_INCDNT_PRIME_REASON_GRP_CD, COUNT(*) AS DELAYED_FLIGHTS
    FROM CERT_FLIGHT_OPERATIONS_VWS.ACTL_FLIGHT_LEG
    WHERE ACTL_LEG_DEP_DT = '{flight_date}' AND DEP_DELAY_IND = 'Y'
    GROUP BY LEG_INCDNT_PRIME_REASON_GRP_CD
    ORDER BY DELAYED_FLIGHTS DESC
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "get_delays_by_reason"})

def get_delay_reason_xref(conn: TeradataConnection):
    sql = "SELECT * FROM CERT_FLIGHT_OPERATIONS_VWS.DELAY_REASON_XREF"
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "get_delay_reason_xref"})
