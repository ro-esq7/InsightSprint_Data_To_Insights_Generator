"""Descriptive Analytics Functions for the InsightSprint"""

# Step 1: Import Libraries
from pathlib import Path

import pandas as pd


# Step 2: Define Required Columns
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

MONTH_ORDER = ["Month 1", "Month 2", "Month 3"]


# Step 3: Build Helper Functions
def validate_required_columns(data: pd.DataFrame, required_columns: set[str] | None = None) -> None:
    """Validate that the input DataFrame contains the columns needed for analysis.

    Args:
        data: Transaction-level retail data.
        required_columns: Optional custom set of required column names.

    Raises:
        TypeError: If data is not a pandas DataFrame.
        ValueError: If one or more required columns are missing.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input data must be a pandas DataFrame.")

    columns_to_check = required_columns or REQUIRED_COLUMNS
    missing_columns = sorted(columns_to_check.difference(data.columns))

    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"Input data is missing required columns: {missing_text}")


def sort_by_month_order(data: pd.DataFrame, month_column: str = "order_month") -> pd.DataFrame:
    """Sort a DataFrame by the expected InsightSprint month order.

    Args:
        data: DataFrame containing an order month column.
        month_column: Name of the month column to sort by.

    Returns:
        A DataFrame sorted by Month 1, Month 2, and Month 3.
    """
    sorted_data = data.copy()
    sorted_data[month_column] = pd.Categorical(
        sorted_data[month_column],
        categories=MONTH_ORDER,
        ordered=True,
    )
    sorted_data = sorted_data.sort_values(month_column).reset_index(drop=True)
    sorted_data[month_column] = sorted_data[month_column].astype(str)

    return sorted_data


# Step 4: Analyze Most Popular Product by Month
def analyze_most_popular_item_per_month(data: pd.DataFrame) -> pd.DataFrame:
    """Identify the most popular product in each month based on units sold.

    Popularity is ranked first by total units sold, then by distinct order count,
    and finally by total revenue.

    Args:
        data: Transaction-level retail data.

    Returns:
        A DataFrame with the top product for each month.
    """
    required_columns = {
        "order_month",
        "product_name",
        "units_sold",
        "order_id",
        "order_revenue",
    }
    validate_required_columns(data, required_columns)

    product_summary = (
        data.groupby(["order_month", "product_name"], as_index=False)
        .agg(
            total_units_sold=("units_sold", "sum"),
            total_orders=("order_id", "nunique"),
            total_revenue=("order_revenue", "sum"),
        )
        .sort_values(
            by=[
                "order_month",
                "total_units_sold",
                "total_orders",
                "total_revenue",
                "product_name",
            ],
            ascending=[True, False, False, False, True],
        )
    )

    top_products = product_summary.groupby("order_month", as_index=False).head(1)
    top_products = sort_by_month_order(top_products)

    return top_products[
        [
            "order_month",
            "product_name",
            "total_units_sold",
            "total_orders",
            "total_revenue",
        ]
    ]


# Step 5: Analyze Revenue Change Across Months
def analyze_revenue_change_month1_to_month3(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize revenue, orders, units sold, and month-over-month revenue change.

    Args:
        data: Transaction-level retail data.

    Returns:
        A DataFrame with month-level revenue metrics and change calculations.
    """
    required_columns = {
        "order_month",
        "order_revenue",
        "order_id",
        "units_sold",
    }
    validate_required_columns(data, required_columns)

    monthly_summary = (
        data.groupby("order_month", as_index=False)
        .agg(
            total_revenue=("order_revenue", "sum"),
            total_orders=("order_id", "nunique"),
            total_units_sold=("units_sold", "sum"),
        )
        .pipe(sort_by_month_order)
    )

    monthly_summary["revenue_change_vs_prior"] = monthly_summary["total_revenue"].diff()
    monthly_summary["pct_change_vs_prior"] = monthly_summary["total_revenue"].pct_change() * 100

    return monthly_summary[
        [
            "order_month",
            "total_revenue",
            "total_orders",
            "total_units_sold",
            "revenue_change_vs_prior",
            "pct_change_vs_prior",
        ]
    ]


# Step 6: Analyze Revenue by Sales Channel
def analyze_channel_revenue(data: pd.DataFrame) -> pd.DataFrame:
    """Compare total revenue, orders, units sold, and revenue share by sales channel.

    Args:
        data: Transaction-level retail data.

    Returns:
        A DataFrame with channel-level revenue metrics.
    """
    required_columns = {
        "order_channel",
        "order_revenue",
        "order_id",
        "units_sold",
    }
    validate_required_columns(data, required_columns)

    channel_summary = (
        data.groupby("order_channel", as_index=False)
        .agg(
            total_revenue=("order_revenue", "sum"),
            total_orders=("order_id", "nunique"),
            total_units_sold=("units_sold", "sum"),
        )
        .sort_values("total_revenue", ascending=False)
        .reset_index(drop=True)
    )

    total_revenue = channel_summary["total_revenue"].sum()
    if total_revenue == 0:
        channel_summary["revenue_share_pct"] = 0.0
    else:
        channel_summary["revenue_share_pct"] = (
            channel_summary["total_revenue"] / total_revenue * 100
        )

    return channel_summary[
        [
            "order_channel",
            "total_revenue",
            "total_orders",
            "total_units_sold",
            "revenue_share_pct",
        ]
    ]


# Step 7: Run Script and Save Outputs
if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent
    data_path = project_root / "data" / "insightsprint_synthetic_jewelry_transactions_v2.csv"
    output_dir = project_root / "outputs"

    output_dir.mkdir(parents=True, exist_ok=True)

    transactions = pd.read_csv(data_path)

    top_product_by_month = analyze_most_popular_item_per_month(transactions)
    revenue_change = analyze_revenue_change_month1_to_month3(transactions)
    channel_revenue = analyze_channel_revenue(transactions)

    top_product_by_month.to_csv(output_dir / "top_product_by_month.csv", index=False)
    revenue_change.to_csv(output_dir / "revenue_change.csv", index=False)
    channel_revenue.to_csv(output_dir / "channel_revenue.csv", index=False)

    print(f"Success: InsightSprint output files were saved to {output_dir}")
