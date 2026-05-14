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

# Step 7: Warn the User if the App is Running in Demo Mode
if not API_KEY:
    st.warning(
        "Missing OPENAI_API_KEY in .env file. The app will run in demo mode "
        "using metric-based placeholder output."
    )

# Step 8: Define the Supported Business Questions
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

# Step 9: Format the Computed Metrics for Prompt Use
def format_metrics_for_prompt(metrics_df: pd.DataFrame) -> str:
    """Convert computed metrics into a readable text block for the prompt preview."""
    return metrics_df.to_string(index=False)

# Step 10: Build the User Prompt Preview
def build_prompt_preview(business_question: str, metrics_df: pd.DataFrame) -> str:
    """Build the final user prompt that would be sent to an LLM."""
    return USER_PROMPT_TEMPLATE.format(
        business_question=business_question,
        computed_metrics=format_metrics_for_prompt(metrics_df),
    )

# Step 11: Generate the Insight Brief with OpenAI
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

# Step 12: Build a Demo Insight Brief from Computed Metrics Only
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

# Step 13: Read the Uploaded CSV File
def read_uploaded_csv(uploaded_file) -> pd.DataFrame:
    """Read an uploaded CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(uploaded_file)
    except pd.errors.EmptyDataError as exc:
        raise ValueError("The uploaded CSV is empty.") from exc
    except pd.errors.ParserError as exc:
        raise ValueError("The uploaded file could not be parsed as a valid CSV.") from exc

# Step 14: Build the App Header
st.title("InsightSprint")
st.subheader("From Retail Transaction Data to Reviewable Insight Briefs")

# Step 15: Explain the Project Workflow
with st.expander("Project Workflow", expanded=False):
    st.markdown(
        """
        Upload a CSV, validate the required retail transaction columns, preview the dataset,
        choose one supported business question, compute descriptive metrics, and generate a
        draft insight brief for review.
        """
    )

# Step 16: Build the Sidebar
with st.sidebar:
    st.header("Required Columns")
    st.write(", ".join(sorted(REQUIRED_COLUMNS)))
    st.header("Scope")
    st.write(
        "Descriptive analytics only. The app uses grounded computed metrics before drafting the brief."
    )

# Step 17: Upload the Dataset
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is None:
    st.info("Upload a CSV file to begin.")
    st.stop()

# Step 18: Validate the Uploaded Dataset
try:
    data = read_uploaded_csv(uploaded_file)
    validate_required_columns(data)
except ValueError as exc:
    st.error(str(exc))
    st.stop()

st.success("Dataset uploaded and required columns validated.")

# Step 19: Preview the Uploaded Dataset
st.markdown("### Dataset Preview")
st.dataframe(data.head(10), use_container_width=True)
st.caption(f"Previewing 10 rows from {len(data):,} total rows and {len(data.columns):,} columns.")

# Step 20: Let the User Choose a Supported Business Question
selected_question = st.selectbox(
    "Choose a supported business question",
    options=list(SUPPORTED_QUESTIONS.keys()),
)
st.caption(SUPPORTED_QUESTIONS[selected_question]["description"])

# Step 21: Run the Selected Analysis and Generate the Brief
if st.button("Run Analysis", type="primary"):
    analysis_function = SUPPORTED_QUESTIONS[selected_question]["analysis_function"]

    try:
        metrics = analysis_function(data)
    except (TypeError, ValueError) as exc:
        st.error(str(exc))
        st.stop()

    # Step 22: Display the Computed Metrics
    st.markdown("### Computed Metrics")
    st.dataframe(metrics, use_container_width=True)

    # Step 23: Generate the Draft Insight Brief
    st.markdown("### Draft Insight Brief for Review")

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

    # Step 24: Show the Prompt Preview
    with st.expander("Prompt Preview", expanded=False):
        st.markdown("**System Prompt**")
        st.code(SYSTEM_PROMPT, language="text")

        st.markdown("**User Prompt With Computed Metrics**")
        st.code(build_prompt_preview(selected_question, metrics), language="text")