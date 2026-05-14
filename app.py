import pandas as pd
import streamlit as st

from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from insightsprint_question_logic import (
    analyze_most_popular_item_per_month,
    analyze_revenue_change_month1_to_month3,
    analyze_channel_revenue,
)

st.set_page_config(page_title="InsightSprint", page_icon="💎", layout="wide")

SUPPORTED_QUESTIONS = {
    "Which product was the most popular in each month?": {
        "analysis_function": analyze_most_popular_item_per_month,
        "description": "Identifies the top product in each month based on units sold.",
    },
    "How did total revenue change from Month 1 to Month 3?": {
        "analysis_function": analyze_revenue_change_month1_to_month3,
        "description": "Summarizes revenue by month and calculates month-over-month change.",
    },
    "Which channel generated more revenue: online or in-store?": {
        "analysis_function": analyze_channel_revenue,
        "description": "Compares total revenue contribution across sales channels.",
    },
}

REQUIRED_COLUMNS = {
    "order_month",
    "order_date",
    "order_id",
    "customer_id",
    "order_channel",
    "sku_id",
    "product_category",
    "product_name",
    "units_sold",
    "order_revenue",
    "customer_status",
    "region",
}


def validate_columns(df: pd.DataFrame) -> tuple[bool, list[str]]:
    missing = sorted(list(REQUIRED_COLUMNS - set(df.columns)))
    return len(missing) == 0, missing


def format_metrics_for_prompt(metrics_df: pd.DataFrame) -> str:
    """Convert computed metrics into a clean text block for the LLM prompt."""
    return metrics_df.to_string(index=False)


def build_demo_insight_brief(business_question: str, metrics_df: pd.DataFrame) -> str:
    """
    Placeholder output for the Streamlit skeleton.
    Later, replace this with a real LLM call that uses SYSTEM_PROMPT and USER_PROMPT_TEMPLATE.
    """
    metrics_text = format_metrics_for_prompt(metrics_df)

    if business_question == "Which product was the most popular in each month?":
        lines = []
        for _, row in metrics_df.iterrows():
            lines.append(
                f"- {row['order_month']}: {row['product_name']} led with {int(row['total_units_sold'])} units sold "
                f"across {int(row['total_orders'])} orders."
            )
        supporting = [
            f"- {row['order_month']}: {row['product_name']} | Units Sold = {int(row['total_units_sold'])} | "
            f"Orders = {int(row['total_orders'])} | Revenue = ${row['total_revenue']:,.2f}"
            for _, row in metrics_df.iterrows()
        ]
        follow_ups = [
            "- Did the most popular product in each month also generate the most revenue?",
            "- Were product shifts consistent across channels and regions?",
        ]
        caveats = [
            "- Popularity is based on units sold rather than revenue or profitability.",
            "- These findings are descriptive and do not explain why product preferences changed over time.",
        ]
    elif business_question == "How did total revenue change from Month 1 to Month 3?":
        lines = [
            f"- Revenue increased from ${metrics_df.iloc[0]['total_revenue']:,.2f} in {metrics_df.iloc[0]['order_month']} "
            f"to ${metrics_df.iloc[-1]['total_revenue']:,.2f} in {metrics_df.iloc[-1]['order_month']}.",
            f"- The largest month-over-month increase occurred between {metrics_df.iloc[1]['order_month']} and "
            f"{metrics_df.iloc[2]['order_month']}.",
        ]
        supporting = []
        for _, row in metrics_df.iterrows():
            change = row.get("revenue_change_vs_prior")
            pct = row.get("pct_change_vs_prior")
            if pd.isna(change):
                supporting.append(
                    f"- {row['order_month']}: Revenue = ${row['total_revenue']:,.2f}, Orders = {int(row['total_orders'])}, "
                    f"Units Sold = {int(row['total_units_sold'])}"
                )
            else:
                supporting.append(
                    f"- {row['order_month']}: Revenue = ${row['total_revenue']:,.2f}, Change vs Prior = ${change:,.2f}, "
                    f"% Change = {pct:.2f}%"
                )
        follow_ups = [
            "- Which products contributed most to the revenue growth across months?",
            "- Was revenue growth driven more by order volume or product mix?",
        ]
        caveats = [
            "- This analysis is descriptive and does not identify the cause of revenue growth.",
            "- The results do not account for promotions, pricing changes, or external seasonality effects.",
        ]
    else:
        winner = metrics_df.iloc[0]
        runner_up = metrics_df.iloc[1]
        lines = [
            f"- {winner['order_channel']} generated more revenue than {runner_up['order_channel']} over the three-month period.",
            f"- {winner['order_channel']} accounted for {winner['revenue_share_pct']:.2f}% of total revenue.",
        ]
        supporting = [
            f"- {row['order_channel']}: Revenue = ${row['total_revenue']:,.2f} | Orders = {int(row['total_orders'])} | "
            f"Units Sold = {int(row['total_units_sold'])} | Revenue Share = {row['revenue_share_pct']:.2f}%"
            for _, row in metrics_df.iterrows()
        ]
        follow_ups = [
            "- Which products performed best within each channel?",
            "- Did channel performance remain consistent in each month?",
        ]
        caveats = [
            "- This comparison reflects revenue only and does not account for profitability or channel costs.",
            "- The results do not explain whether channel differences were driven by product mix or order volume.",
        ]

    brief = f"""## 1. Business Question
{business_question}

## 2. Key Findings
{chr(10).join(lines)}

## 3. Supporting Metrics
{chr(10).join(supporting)}

## 4. Limitations / Caveats
{chr(10).join(caveats)}

## 5. Suggested Follow-Up Questions
{chr(10).join(follow_ups)}
"""
    return brief


st.title("💎 InsightSprint")
st.subheader("From Retail Transaction Data to Reviewable Insight Briefs")

with st.expander("Project workflow", expanded=False):
    st.markdown(
        """
        **Workflow:** Upload a retail transaction dataset, select one supported business question,
        compute descriptive metrics, and generate a first-pass insight brief for review.

        **Current scope:** Descriptive analytics only.
        """
    )

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

question = st.selectbox(
    "Select a business question",
    options=list(SUPPORTED_QUESTIONS.keys()),
    index=0,
)

st.caption(SUPPORTED_QUESTIONS[question]["description"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        is_valid, missing_columns = validate_columns(df)

        if not is_valid:
            st.error(
                "The uploaded file is missing required columns: "
                + ", ".join(missing_columns)
            )
        else:
            st.success("Dataset uploaded successfully.")
            with st.expander("Preview uploaded data", expanded=False):
                st.dataframe(df.head(10), use_container_width=True)

            if st.button("Generate Insight Brief", type="primary"):
                analysis_function = SUPPORTED_QUESTIONS[question]["analysis_function"]
                metrics_df = analysis_function(df)

                st.markdown("### Computed Metrics")
                st.dataframe(metrics_df, use_container_width=True)

                st.markdown("### Draft Insight Brief")
                st.markdown(build_demo_insight_brief(question, metrics_df))

                with st.expander("Prompt preview", expanded=False):
                    st.markdown("**System Prompt**")
                    st.code(SYSTEM_PROMPT, language="text")

                    st.markdown("**User Prompt Template**")
                    st.code(
                        USER_PROMPT_TEMPLATE.format(
                            business_question=question,
                            computed_metrics=format_metrics_for_prompt(metrics_df),
                        ),
                        language="text",
                    )

                st.info(
                    "This is the Streamlit skeleton with a placeholder brief generator. "
                    "The next step is to replace the placeholder output with a real LLM call."
                )
    except Exception as e:
        st.error(f"Something went wrong while processing the file: {e}")
else:
    st.warning("Upload a CSV file to begin.")

with st.sidebar:
    st.header("About")
    st.write(
        "InsightSprint is a descriptive analytics workflow for a freelance consultant "
        "working with small retail transaction datasets."
    )
    st.write("Supported questions are intentionally limited to keep the scope narrow and evaluable.")
