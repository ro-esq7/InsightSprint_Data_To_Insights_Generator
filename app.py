"""Streamlit App for InsightSprint"""

# Step 1: Import Libraries
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


# Step 2: Import Prompt Files
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


# Step 3: Import InsightSprint Question Logic
from insightsprint_question_logic import (
    REQUIRED_COLUMNS,
    analyze_channel_revenue,
    analyze_most_popular_item_per_month,
    analyze_revenue_change_month1_to_month3,
    validate_required_columns,
)


# Step 4: Load Environment Variables
load_dotenv()


# Step 5: Store API Key and Initialize OpenAI Client
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)
MODEL_NAME = "gpt-5.2"


# Step 6: Configure the Streamlit Page
st.set_page_config(page_title="InsightSprint", page_icon="💎", layout="wide")


# Step 7: Add Custom Styling
st.markdown(
    """
    <style>
    /* Main app background */
    .stApp {
        background-color: #F5F5F5;
        color: #37474F;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #37474F;
    }

    section[data-testid="stSidebar"] * {
        color: #F5F5F5 !important;
    }

    /* Main headers */
    h1, h2, h3 {
        color: #37474F !important;
        font-weight: 700;
    }

    /* Buttons */
    .stButton > button {
        background-color: #64BEB6;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #4fa9a1;
        color: white;
    }

    /* File uploader outer container */
    [data-testid="stFileUploader"] {
        background-color: #37474F;
        border: 1px solid #64BEB6;
        border-radius: 12px;
        padding: 0.75rem;
    }

    /* File uploader text */
    [data-testid="stFileUploader"] * {
        color: #F5F5F5 !important;
    }

    /* Upload button inside file uploader */
    [data-testid="stFileUploader"] section button {
        background-color: #64BEB6 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
    }

    [data-testid="stFileUploader"] section button:hover {
        background-color: #4fa9a1 !important;
        color: white !important;
    }

    /* Selectbox / text inputs */
    div[data-baseweb="select"] > div,
    .stTextInput > div > div > input {
        border-radius: 10px;
    }

    /* Info / success / warning message boxes */
    [data-testid="stAlertContainer"] {
        border-radius: 10px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        color: #37474F !important;
        font-weight: 600;
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border: 1px solid #d9d9d9;
        border-radius: 10px;
        overflow: hidden;
    }

    /* Main content spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Horizontal rule */
    hr {
        border: none;
        height: 1px;
        background-color: #64BEB6;
        margin: 1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Step 8: Create Helper Function to Format Section Cards
def section_card(title: str):
    st.markdown(
        f"""
        <div style="background-color:#FFFFFF; padding:0.9rem 1.1rem; border-radius:12px; border-left:6px solid #64BEB6; margin-top:1rem; margin-bottom:0.5rem;">
            <h3 style="margin:0; color:#37474F;">{title}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


# Step 9: Warn the User if the App is Running in Demo Mode
if not API_KEY:
    st.warning(
        "Missing OPENAI_API_KEY in .env file. The app will run in demo mode "
        "using metric-based placeholder output."
    )


# Step 10: Define the Supported Business Questions
SUPPORTED_QUESTIONS = {
    "Which product was the most popular in each month?": {
        "analysis_function": analyze_most_popular_item_per_month,
        "description": "Identifies the top product in each month based on units sold.",
    },
    "How did total revenue change from Month 1 to Month 3?": {
        "analysis_function": analyze_revenue_change_month1_to_month3,
        "description": "Summarizes revenue by month and calculates month-over-month revenue change.",
    },
    "Which channel generated more revenue: online or in-store?": {
        "analysis_function": analyze_channel_revenue,
        "description": "Compares total revenue contribution across sales channels.",
    },
}


# Step 11: Format the Computed Metrics for Prompt Use
def format_metrics_for_prompt(metrics_df: pd.DataFrame) -> str:
    """Convert computed metrics into a readable text block for the prompt preview."""
    return metrics_df.to_string(index=False)


# Step 12: Build the User Prompt Preview
def build_prompt_preview(business_question: str, metrics_df: pd.DataFrame) -> str:
    """Build the final user prompt that would be sent to an LLM."""
    return USER_PROMPT_TEMPLATE.format(
        business_question=business_question,
        computed_metrics=format_metrics_for_prompt(metrics_df),
    )


# Step 13: Generate the Insight Brief with OpenAI
def generate_insight_brief_with_openai(business_question: str, metrics_df: pd.DataFrame) -> str:
    """Generate an insight brief with OpenAI using the computed metrics."""
    api_key = API_KEY
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY in the .env file.")

    user_prompt = build_prompt_preview(business_question, metrics_df)

    response = client.responses.create(
        model=MODEL_NAME,
        instructions=SYSTEM_PROMPT,
        input=user_prompt,
    )

    if not response.output_text:
        raise ValueError("OpenAI returned an empty response.")

    return response.output_text


# Step 14: Build a Demo Insight Brief from Computed Metrics Only
def build_demo_insight_brief_from_metrics(business_question: str, metrics_df: pd.DataFrame) -> str:
    """Build a grounded draft insight brief from computed metrics only.

    This keeps the class/demo version runnable without requiring an API key while
    preserving the same structure expected from the prompt.
    """
    if business_question == "Which product was the most popular in each month?":
        key_findings = [
            f"- {row['order_month']}: {row['product_name']} led with "
            f"{int(row['total_units_sold'])} units sold across {int(row['total_orders'])} orders."
            for _, row in metrics_df.iterrows()
        ]
        supporting_metrics = [
            f"- {row['order_month']}: {row['product_name']} | Units Sold = "
            f"{int(row['total_units_sold'])} | Orders = {int(row['total_orders'])} | "
            f"Revenue = ${row['total_revenue']:,.2f}"
            for _, row in metrics_df.iterrows()
        ]
        caveats = [
            "- Popularity is based on units sold, not revenue or profitability.",
            "- The metrics describe what happened but do not explain why product demand shifted.",
        ]
        follow_ups = [
            "- Did the most popular product in each month also generate the most revenue?",
            "- Were product shifts consistent across channels or regions?",
        ]

    elif business_question == "How did total revenue change from Month 1 to Month 3?":
        first_month = metrics_df.iloc[0]
        last_month = metrics_df.iloc[-1]
        key_findings = [
            f"- Revenue changed from ${first_month['total_revenue']:,.2f} in "
            f"{first_month['order_month']} to ${last_month['total_revenue']:,.2f} in "
            f"{last_month['order_month']}.",
            f"- Total units sold changed from {int(first_month['total_units_sold'])} to "
            f"{int(last_month['total_units_sold'])} over the same period.",
        ]
        supporting_metrics = []
        for _, row in metrics_df.iterrows():
            if pd.isna(row["revenue_change_vs_prior"]):
                supporting_metrics.append(
                    f"- {row['order_month']}: Revenue = ${row['total_revenue']:,.2f} | "
                    f"Orders = {int(row['total_orders'])} | Units Sold = {int(row['total_units_sold'])}"
                )
            else:
                supporting_metrics.append(
                    f"- {row['order_month']}: Revenue = ${row['total_revenue']:,.2f} | "
                    f"Change vs Prior = ${row['revenue_change_vs_prior']:,.2f} | "
                    f"Percent Change = {row['pct_change_vs_prior']:.2f}%"
                )
        caveats = [
            "- This analysis is descriptive and does not identify the cause of revenue movement.",
            "- The results do not account for promotions, pricing changes, or seasonality.",
        ]
        follow_ups = [
            "- Which products contributed most to the revenue change?",
            "- Was revenue movement driven more by order volume or product mix?",
        ]

    else:
        top_channel = metrics_df.iloc[0]
        comparison_channel = metrics_df.iloc[1] if len(metrics_df) > 1 else None
        if comparison_channel is not None:
            key_findings = [
                f"- {top_channel['order_channel']} generated more revenue than "
                f"{comparison_channel['order_channel']} during the analysis period.",
                f"- {top_channel['order_channel']} accounted for "
                f"{top_channel['revenue_share_pct']:.2f}% of total revenue.",
            ]
        else:
            key_findings = [
                f"- {top_channel['order_channel']} was the only channel present in the uploaded data.",
                f"- It accounted for {top_channel['revenue_share_pct']:.2f}% of total revenue.",
            ]
        supporting_metrics = [
            f"- {row['order_channel']}: Revenue = ${row['total_revenue']:,.2f} | "
            f"Orders = {int(row['total_orders'])} | Units Sold = {int(row['total_units_sold'])} | "
            f"Revenue Share = {row['revenue_share_pct']:.2f}%"
            for _, row in metrics_df.iterrows()
        ]
        caveats = [
            "- This comparison reflects revenue only and does not account for profitability or channel costs.",
            "- The metrics do not explain whether channel differences were driven by product mix or order size.",
        ]
        follow_ups = [
            "- Which products performed best within each channel?",
            "- Did channel performance remain consistent across all three months?",
        ]

    return f"""## 1. Business Question
{business_question}

## 2. Key Findings
{chr(10).join(key_findings)}

## 3. Supporting Metrics
{chr(10).join(supporting_metrics)}

## 4. Limitations / Caveats
{chr(10).join(caveats)}

## 5. Suggested Follow-Up Questions
{chr(10).join(follow_ups)}
"""


# Step 15: Read the Uploaded CSV File
def read_uploaded_csv(uploaded_file) -> pd.DataFrame:
    """Read an uploaded CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(uploaded_file)
    except pd.errors.EmptyDataError as exc:
        raise ValueError("The uploaded CSV is empty.") from exc
    except pd.errors.ParserError as exc:
        raise ValueError("The uploaded file could not be parsed as a valid CSV.") from exc


# Step 16: Format Metrics for Display in Streamlit
def format_metrics_for_display(metrics_df: pd.DataFrame) -> pd.DataFrame:
    """Format metric columns for cleaner display in Streamlit."""
    formatted_df = metrics_df.copy()

    currency_columns = ["total_revenue", "revenue_change_vs_prior"]
    percent_columns = ["pct_change_vs_prior", "revenue_share_pct"]

    for col in currency_columns:
        if col in formatted_df.columns:
            formatted_df[col] = formatted_df[col].apply(
                lambda x: f"${x:,.2f}" if pd.notna(x) else ""
            )

    for col in percent_columns:
        if col in formatted_df.columns:
            formatted_df[col] = formatted_df[col].apply(
                lambda x: f"{x:.2f}%" if pd.notna(x) else ""
            )

    return formatted_df


# Step 17: Build the App Header
st.markdown(
    """
    <div style="background-color:#FFFFFF; padding:1.25rem 1.5rem; border-radius:14px; border-left:8px solid #64BEB6; box-shadow:0 2px 8px rgba(0,0,0,0.05);">
        <h1 style="margin-bottom:0.25rem; color:#37474F;">InsightSprint</h1>
        <p style="margin-bottom:0; color:#37474F; font-size:1.1rem;">
            From Retail Transaction Data to Reviewable Insight Briefs
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# Step 18: Build the Sidebar
with st.sidebar:
    st.title(
        "👩🏽‍💻 InsightSprint"
        )
    
    st.markdown("---")

    st.header("Project Workflow")
    st.markdown(
        """
        1. Upload a CSV  
        2. Ensure the required columns are present  
        3. Preview the dataset  
        4. Select 1 supported business question  
        5. Compute descriptive metrics  
        6. Generate a draft insight brief for review
        """
    )

    st.markdown("---")

    st.header("Required Columns")
    st.markdown(
        """
        - customer_id
        - customer_status
        - order_channel
        - order_date
        - order_id
        - order_month
        - order_revenue
        - product_category
        - product_name
        - region
        - sku_id
        - units_sold
        """
    )

    st.markdown("---")

    st.header("Learn More")
    st.markdown(
        """
        [**GitHub Repository**](https://github.com/ro-esq7/InsightSprint_Data_To_Insights_Generator)
        
        Rosarys Esquilin  
        Final Project  
        BU.330.760.41.SP26 - Generative AI  
        Carey Business School  
        Johns Hopkins University
        """
    )


# Step 19: Upload the Dataset
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is None:
    st.info("Upload a CSV File to Begin.")
    st.stop()


# Step 20: Validate the Uploaded Dataset
try:
    data = read_uploaded_csv(uploaded_file)
    validate_required_columns(data)
except ValueError as exc:
    st.error(str(exc))
    st.stop()

st.success("Data Upload Successful.")


# Step 21: Preview the Uploaded Dataset
section_card("Dataset Preview")
st.dataframe(data.head(10), use_container_width=True)
st.caption(f"Previewing 10 rows from {len(data):,} total rows and {len(data.columns):,} columns.")


# Step 22: Let the User Choose a Supported Business Question
selected_question = st.selectbox(
    "Choose a Business Question",
    options=list(SUPPORTED_QUESTIONS.keys()),
)
st.caption(SUPPORTED_QUESTIONS[selected_question]["description"])


# Step 23: Run the Selected Analysis and Generate the Brief
if st.button("Run Analysis", type="primary"):
    analysis_function = SUPPORTED_QUESTIONS[selected_question]["analysis_function"]

    try:
        metrics = analysis_function(data)
    except (TypeError, ValueError) as exc:
        st.error(str(exc))
        st.stop()

    # Step 24: Display the Computed Metrics
    section_card("Metrics")
    st.dataframe(format_metrics_for_display(metrics), use_container_width=True)

    # Step 25: Generate the Draft Insight Brief
    section_card("Insight Brief for Review")

    try:
        if API_KEY:
            insight_brief = generate_insight_brief_with_openai(selected_question, metrics)
            st.markdown(insight_brief)
        else:
            st.markdown(build_demo_insight_brief_from_metrics(selected_question, metrics))
            st.caption("Demo mode: showing a grounded placeholder brief because no API key was found.")
    except Exception as exc:
        st.error(f"OpenAI request failed: {exc}")
        st.markdown(build_demo_insight_brief_from_metrics(selected_question, metrics))
        st.caption("Fallback mode: showing a grounded placeholder brief because the live API request was unavailable.")