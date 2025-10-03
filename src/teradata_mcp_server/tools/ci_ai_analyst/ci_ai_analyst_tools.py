# 1. Customer Value & Segmentation
def handle_ci_customer_value_segmentation(conn, *args, **kwargs):
  sql = '''SELECT TIER_EOP, HOME_CITY, SUM(TOTAL_ICC) / SUM(TOTAL_POTENTIAL_REVENUE) AS ICC_MARGIN\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2025_YE07_V05_00\nGROUP BY TIER_EOP, HOME_CITY\nORDER BY ICC_MARGIN DESC;'''
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "ci_customer_value_segmentation"})

# 2. Digital Engagement & App Usage
def handle_ci_app_usage(conn, *args, **kwargs):
  sql = '''SELECT APP_USER_IND, AVG(TOTAL_ICC) AS AVG_ICC, COUNT(*) AS NUM_CUSTOMERS\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2025_YE07_V05_00\nGROUP BY APP_USER_IND;'''
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "ci_app_usage"})

# 3. Co-Brand Cardholder Analysis
def handle_ci_cobrand_card_analysis(conn, *args, **kwargs):
  sql = '''SELECT CARD_CATEGORY, SUM(TOTAL_ICC) AS TOTAL_ICC, SUM(TOTAL_ANCILLARY_REV) AS ANC_REV\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2025_YE07_V05_00\nGROUP BY CARD_CATEGORY;'''
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "ci_cobrand_card_analysis"})

# 4. Share of Wallet & Industry Spend
def handle_ci_share_of_wallet(conn, *args, **kwargs):
  sql = '''SELECT PARTY_ID, EST_AA_SHARE_OF_WALLET_PCT_BAND, EST_AIRLINE_SPEND_BAND\nFROM PROD_CUST_SEGMENTATION_VW.CUST_AIRLINE_SPEND_SUMRY\nWHERE EST_AA_SHARE_OF_WALLET_PCT_BAND < 20;'''
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "ci_share_of_wallet"})

# 5. Breakage & Credit Utilization
def handle_ci_breakage_credit_utilization(conn, *args, **kwargs):
  sql = '''SELECT SUM(FLIGHT_CREDIT_BREAKAGE + FLIGHT_NOGO_BREAKAGE + TRIP_CREDIT_BREAKAGE + OTHER_CREDIT_BREAKAGE) AS TOTAL_BREAKAGE\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2025_YE07_V05_00;'''
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "ci_breakage_credit_utilization"})

# 6. Campaign Impact & Marketing Analytics
def handle_ci_campaign_impact(conn, *args, **kwargs):
  sql = '''SELECT CAMPAIGN_GROUP, COUNT(*) AS NUM_CUSTOMERS, AVG(CONVERSION_RATE) AS AVG_CONV\nFROM CAMPAIGN_RESULTS_TABLE\nWHERE CAMPAIGN_NAME = 'Boost & Renew 2025'\nGROUP BY CAMPAIGN_GROUP;'''
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "ci_campaign_impact"})

# 7. Loyalty & Churn Prediction
def handle_ci_loyalty_churn(conn, *args, **kwargs):
  sql = '''SELECT PARTY_ID, CHURN_SCORE, PRED_FLT_ICC, PRED_CUR_ICC\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2025_YE07_V05_00\nWHERE CHURN_SCORE > 0.8;'''
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "ci_loyalty_churn"})

# 8. Ancillary Product Analysis
def handle_ci_ancillary_product(conn, *args, **kwargs):
  sql = '''SELECT ANC_PREF_SEAT, ANC_MCE_SEAT, ANC_UPG_LFBU, ANC_BAG_FEE, SUM(TOTAL_ANCILLARY_REV)\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2025_YE07_V05_00\nGROUP BY ANC_PREF_SEAT, ANC_MCE_SEAT, ANC_UPG_LFBU, ANC_BAG_FEE;'''
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "ci_ancillary_product"})

# 9. Booking Channel & Digital Trends
def handle_ci_booking_channel(conn, *args, **kwargs):
  sql = '''SELECT CUST_CHANNEL_TYPE, COUNT(*) AS NUM_CUSTOMERS, AVG(TOTAL_ICC) AS AVG_ICC\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2025_YE07_V05_00\nGROUP BY CUST_CHANNEL_TYPE;'''
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "ci_booking_channel"})

# 10. Premium Customer Analysis
def handle_ci_premium_customer(conn, *args, **kwargs):
  sql = '''SELECT AP_IND, AVG(AP_CASH_FLT_ICC) AS AVG_PREMIUM_ICC\nFROM RM_CUST_INTELLIGENCE.CIAP_CUST_VIEW_2025_YE07_V05_00\nWHERE AP_IND = 'Y'\nGROUP BY AP_IND;'''
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "ci_premium_customer"})

# 11. Companion Certificates & Bag Benefits
def handle_ci_companion_bag_benefits(conn, *args, **kwargs):
  sql = '''SELECT SUM(COMP_CERT_REV) AS TOTAL_COMP_CERT_REV, SUM(CITI_BAG_REV + BCUS_BAG_REV) AS TOTAL_BAG_REV\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2025_YE07_V05_00;'''
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "ci_companion_bag_benefits"})

# 12. Award CPM & Redemption Analysis
def handle_ci_award_cpm(conn, *args, **kwargs):
  sql = '''SELECT PNR_LOCATOR_CODE_S, AWD_BID_PRICE\nFROM RM_CUST_INTELLIGENCE.CI50_INPUT_AWD_CPM\nWHERE TRANS_DT BETWEEN '2024-01-01' AND '2024-12-31';'''
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  columns = [desc[0] for desc in cursor.description]
  return create_response([dict(zip(columns, row)) for row in rows], {"tool_name": "ci_award_cpm"})

def handle_ci_ai_analyst_sql_examples(conn: TeradataConnection, *args, **kwargs):
  """
  Returns all CI 5.0 business scenario SQL examples and their scenario descriptions as a structured list.
  No arguments required.
  """
  logger.debug("Tool: handle_ci_ai_analyst_sql_examples: Args: None")

  sql_examples = [
    {
      "scenario": "Customer Value & Segmentation",
      "description": "Identify high-value customers by ICC margin, segment by tier, tenure, or home city.",
      "sql": """SELECT TIER_EOP, HOME_CITY, SUM(TOTAL_ICC) / SUM(TOTAL_POTENTIAL_REVENUE) AS ICC_MARGIN\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2024_YE08_V05_00\nGROUP BY TIER_EOP, HOME_CITY\nORDER BY ICC_MARGIN DESC;"""
    },
    {
      "scenario": "Digital Engagement & App Usage",
      "description": "Analyze the impact of app usage on revenue and loyalty.",
      "sql": """SELECT APP_USER_IND, AVG(TOTAL_ICC) AS AVG_ICC, COUNT(*) AS NUM_CUSTOMERS\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2024_YE08_V05_00\nGROUP BY APP_USER_IND;"""
    },
    {
      "scenario": "Co-Brand Cardholder Analysis",
      "description": "Compare spend, ICC, and ancillary revenue by co-brand card type.",
      "sql": """SELECT CARD_CATEGORY, SUM(TOTAL_ICC) AS TOTAL_ICC, SUM(TOTAL_ANCILLARY_REV) AS ANC_REV\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2024_YE08_V05_00\nGROUP BY CARD_CATEGORY;"""
    },
    {
      "scenario": "Share of Wallet & Industry Spend",
      "description": "Identify customers with low AA share of wallet for targeted campaigns.",
      "sql": """SELECT PARTY_ID, EST_AA_SHARE_OF_WALLET_PCT_BAND, EST_AIRLINE_SPEND_BAND\nFROM PROD_CUST_SEGMENTATION_VW.CUST_AIRLINE_SPEND_SUMRY\nWHERE EST_AA_SHARE_OF_WALLET_PCT_BAND < 20;"""
    },
    {
      "scenario": "Breakage & Credit Utilization",
      "description": "Quantify breakage revenue and identify customers with high unused credits.",
      "sql": """SELECT SUM(FLIGHT_CREDIT_BREAKAGE + FLIGHT_NOGO_BREAKAGE + TRIP_CREDIT_BREAKAGE + OTHER_CREDIT_BREAKAGE) AS TOTAL_BREAKAGE\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2024_YE08_V05_00;"""
    },
    {
      "scenario": "Campaign Impact & Marketing Analytics",
      "description": "Measure conversion rates and revenue lift from Boost & Renew or status match campaigns.",
      "sql": """SELECT CAMPAIGN_GROUP, COUNT(*) AS NUM_CUSTOMERS, AVG(CONVERSION_RATE) AS AVG_CONV\nFROM CAMPAIGN_RESULTS_TABLE\nWHERE CAMPAIGN_NAME = 'Boost & Renew 2025'\nGROUP BY CAMPAIGN_GROUP;"""
    },
    {
      "scenario": "Loyalty & Churn Prediction",
      "description": "Identify customers at risk of churn and recommend retention actions.",
      "sql": """SELECT PARTY_ID, CHURN_SCORE, PRED_FLT_ICC, PRED_CUR_ICC\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2024_YE08_V05_00\nWHERE CHURN_SCORE > 0.8;"""
    },
    {
      "scenario": "Ancillary Product Analysis",
      "description": "Analyze ancillary revenue by product and customer segment.",
      "sql": """SELECT ANC_PREF_SEAT, ANC_MCE_SEAT, ANC_UPG_LFBU, ANC_BAG_FEE, SUM(TOTAL_ANCILLARY_REV)\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2024_YE08_V05_00\nGROUP BY ANC_PREF_SEAT, ANC_MCE_SEAT, ANC_UPG_LFBU, ANC_BAG_FEE;"""
    },
    {
      "scenario": "Booking Channel & Digital Trends",
      "description": "Track booking channel shifts and digital adoption.",
      "sql": """SELECT CUST_CHANNEL_TYPE, COUNT(*) AS NUM_CUSTOMERS, AVG(TOTAL_ICC) AS AVG_ICC\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2024_YE08_V05_00\nGROUP BY CUST_CHANNEL_TYPE;"""
    },
    {
      "scenario": "Premium Customer Analysis",
      "description": "Deep dive into AAdvantage Premium customer performance.",
      "sql": """SELECT AP_IND, AVG(AP_CASH_FLT_ICC) AS AVG_PREMIUM_ICC\nFROM RM_CUST_INTELLIGENCE.CIAP_CUST_VIEW_2024_YE08_V05_00\nWHERE AP_IND = 'Y'\nGROUP BY AP_IND;"""
    },
    {
      "scenario": "Companion Certificates & Bag Benefits",
      "description": "Evaluate usage and revenue impact of companion certificates and co-brand bag benefits.",
      "sql": """SELECT SUM(COMP_CERT_REV) AS TOTAL_COMP_CERT_REV, SUM(CITI_BAG_REV + BCUS_BAG_REV) AS TOTAL_BAG_REV\nFROM RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2024_YE08_V05_00;"""
    },
    {
      "scenario": "Award CPM & Redemption Analysis",
      "description": "Analyze the cost and value of award redemptions.",
      "sql": """SELECT PNR_LOCATOR_CODE_S, AWD_BID_PRICE\nFROM RM_CUST_INTELLIGENCE.CI50_INPUT_AWD_CPM\nWHERE TRANS_DT BETWEEN '2024-01-01' AND '2024-12-31';"""
    },
    {
      "scenario": "Revenue for a Specified Location and Time Period",
      "description": "Retrieve American Airlines revenue for a specified airport/location and time period.",
      "sql": """SELECT\n    SUM(TICKET_REV) AS AA_Location_Revenue\nFROM\n    RM_CUST_INTELLIGENCE.CI_FLT_VIEW_<PERIOD>_V05_00\nWHERE\n    (MIRS_LEG LIKE '%<LOCATION_CODE>%' OR MIRS_PNR_POO = '<LOCATION_CODE>' OR MIRS_PNR_POC = '<LOCATION_CODE>')\n    AND MIRS_LEG_DEP_DT BETWEEN '<START_DATE>' AND '<END_DATE>'"""
    },
    {
      "scenario": "Solo vs. Family Travelers",
      "description": "Compare how customers that travel alone differ from customers that travel in a family.",
      "sql": """SELECT\n    CASE\n        WHEN PNR_ADULT_COUNT = 1 AND PNR_MINOR_COUNT = 0 THEN 'Solo'\n        WHEN PNR_ADULT_COUNT >= 1 AND PNR_MINOR_COUNT >= 1 THEN 'Family'\n        ELSE 'Other'\n    END AS Traveler_Type,\n    AVG(TICKET_REV) AS Avg_Revenue,\n    AVG(NO_OF_TRIPS) AS Avg_Trips,\n    AVG(ANCILLARY_REVENUE) AS Avg_Ancillary,\n    AVG(ICC) AS Avg_ICC\nFROM\n    RM_CUST_INTELLIGENCE.CI_CUST_VIEW_2024_YE08_V05_00\nGROUP BY\n    Traveler_Type"""
    }
  ]

  metadata = {
    "tool_name": "ci_ai_analyst_sql_examples",
    "source": "CI_AI_Analyst.md",
    "row_count": len(sql_examples)
  }
  return create_response(sql_examples, metadata)
"""
Tool: CI AI Analyst
This tool provides CI 5.0 (Mosaic) Customer Intelligence Data Analyst reference and mapping, based on the CI_AI_Analyst.md documentation.
"""

import logging
from teradatasql import TeradataConnection
from teradata_mcp_server.tools.utils import create_response

logger = logging.getLogger("teradata_mcp_server")

#------------------ Tool  ------------------#
def handle_ci_ai_analyst_reference(conn: TeradataConnection, *args, **kwargs):
    """
    Returns CI 5.0 Customer Intelligence Data Analyst reference, including core datasets, terminology, and physical mappings.
    No arguments required.
    """
    logger.debug("Tool: handle_ci_ai_analyst_reference: Args: None")

    # This is a static reference tool, so we return the markdown content as a string (or could parse to JSON if needed)
    reference_md = '''
# Prompt: Customer Intelligence Data Analyst for CI 5.0 (Mosaic)

## Persona
You are a **Customer Intelligence Data Analyst** working in the Mosaic analytics environment (use mmosaic_lcl_mcp mcp) at American Airlines. You use the CI 5.0 (RM_CUST_INTELLIGENCE) database and related datasets to generate actionable, data-driven insights about customers, segments, and business performance. You do not assume prior knowledge of CI terminology—always explain terms and map them to their physical database locations.
Use mmosaic_lcl_mcp connection

---

## CI 5.0 Database: Datasets & Terminology

### **A. Core Datasets and Their Physical Mapping**

| Dataset Name | Physical Table/View | Description |
|--------------|--------------------|-------------|
| Customer View | `CI_CUST_VIEW_YYYY_YE##` | One row per customer, with all core metrics, segmentation, and activity flags |
| AAdvantage Premium View | `CIAP_CUST_VIEW_YYYY_YE##` | Same as Customer View, plus premium-specific metrics (e.g., premium yield, premium ICC) |
| Flight View | `CI_FLT_VIEW_YYYY_YE##` | One row per flight segment, with revenue, cost, displacement, network value, and segmentation |
| App Usage | `CI50_INPUT_APP_USAGE` | App login/activity flags for each customer/account |
| Award CPM | `CI50_INPUT_AWD_CPM` | Bid price for award redemptions, by PNR and date |
| Barclays Bag Benefit | `CI50_INPUT_BCUS_BAG` | Barclays co-brand bag benefit usage, by customer and flight |
| Citi Bag Benefit | `CI50_INPUT_CITI_BAG` | Citi co-brand bag benefit usage, by customer and flight |
| Companion Certificate | `CI50_INPUT_COMP_CERT` | Companion certificate usage and revenue, by customer and flight |
| Epsilon Share of Wallet & Industry Spend | `PROD_CUST_SEGMENTATION_VW.CUST_AIRLINE_SPEND_SUMRY` | Third-party data on customer airline spend and AA share of wallet |
| NPS Survey Data | (varies, e.g., `NPS_RESPONSES`) | Net Promoter Score and survey responses (if available) |

---

### **B. Key CI Terminology (with Plain English and Mapping)**

- **ICC (Incremental Customer Contribution):**  
  The net value a customer brings after accounting for revenue, costs, network value, and displacement.  
  - *Physical mapping:* `FLIGHT_ICC`, `CURRENCY_ICC`, `TOTAL_ICC` columns in `CI_CUST_VIEW_YYYY_YE##` and `CIAP_CUST_VIEW_YYYY_YE##`

- **Displacement:**  
  The opportunity cost of a customer’s transaction (how replaceable is this revenue?).  
  - *Physical mapping:* `DISPLACEMENT` column

- **Network Value:**  
  The inherent value of the AA network for a given transaction (e.g., how much of the ticket price is due to AA’s schedule strength).  
  - *Physical mapping:* `NETWORK_ADJ` column

- **Breakage:**  
  Revenue from expired credits (flight, trip, or other).  
  - *Physical mapping:* `FLIGHT_CREDIT_BREAKAGE`, `TRIP_CREDIT_BREAKAGE`, `OTHER_CREDIT_BREAKAGE` columns

- **Ancillary Revenue:**  
  Revenue from non-ticket sources (seats, upgrades, baggage, lounge, etc.).  
  - *Physical mapping:* `ANC_*` columns (e.g., `ANC_PREF_SEAT`, `ANC_BAG_FEE`)

- **Share of Wallet (SoW):**  
  The percentage of a customer’s total airline spend that goes to AA.  
  - *Physical mapping:* `EST_AA_SHARE_OF_WALLET_PCT_BAND` in `CUST_AIRLINE_SPEND_SUMRY`

- **App Usage:**  
  Whether a customer logged into the AA mobile app.  
  - *Physical mapping:* `APP_USER_IND` in `CI_CUST_VIEW_YYYY_YE##` and `APP_LOGIN` in `CI50_INPUT_APP_USAGE`

- **Co-brand Earn Indicators:**  
  Flags for Citi, Barclays, International, Premium, Business cards.  
  - *Physical mapping:* `COBRAND_CITI_IND`, `COBRAND_BCUS_IND`, etc.
'''

    metadata = {
        "tool_name": "ci_ai_analyst_reference",
        "source": "CI_AI_Analyst.md",
        "row_count": 1
    }
    return create_response([{"reference": reference_md}], metadata)
