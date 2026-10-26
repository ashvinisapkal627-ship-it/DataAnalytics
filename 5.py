import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid")
pd.set_option("display.max_columns", 120)
pd.set_option("display.max_rows", 30)

# settings
FILE_PATH = None
DATE_COLUMN = "order_date"
GROUP_COLUMN = "region"
TARGET_COLUMN = "sales"

#===================================================
#STEP 1: CREATE SAMPLE DATA
#==================================================
def make_sample_data(n=540, seed=7):
    rng = np.random.default_rng(seed)

    dates = pd.date_range(
        start="2024-06-01",
        periods=n,
        freq="D"
    )

    sales = (
        np.linspace(250, 400, n)
        + 25 * np.sin(np.arange(n) / 45)
        + rng.normal(0, 20, n)
    )

    # Add some outliers
    sales[rng.choice(n, 8, replace=False)] *= 2.2

    data = pd.DataFrame({
        "order_date": dates,
        "sales": sales,
        "units": rng.poisson(18, n),
        "price": rng.normal(120, 15, n),
        "region": rng.choice(
            ["Pune", "Mumbai", "Nashik", "Nagpur"],
            n,
            p=[0.30, 0.35, 0.20, 0.15]
        )
    })

    # Add missing values
    missing_rows = rng.choice(n, 18, replace=False)
    data.loc[missing_rows, "price"] = np.nan

    return data


# ==================================================
# LOAD DATA
# ==================================================
if FILE_PATH is None:
    df = make_sample_data()

elif FILE_PATH.lower().endswith((".xlsx", ".xls")):
    df = pd.read_excel(FILE_PATH)

else:
    df = pd.read_csv(FILE_PATH)


# Convert date column to datetime
if DATE_COLUMN and DATE_COLUMN in df.columns:
    df[DATE_COLUMN] = pd.to_datetime(
        df[DATE_COLUMN],
        errors="coerce"
    )


# ==================================================
# STEP 2: FIRST LOOK AT THE DATA
# ==================================================
print("\n===== STEP 2: FIRST LOOK AT THE DATA =====")

print("Shape (rows, columns):", df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

num_cols = df.select_dtypes(
    include="number"
).columns.tolist()

cat_cols = [
    col for col in df.columns
    if col not in num_cols
    and not pd.api.types.is_datetime64_any_dtype(df[col])
]

print("\nNumeric columns:", num_cols)
print("Categorical columns:", cat_cols)


# Check whether the target column exists
if TARGET_COLUMN not in df.columns:
    raise ValueError(
        f"Target column '{TARGET_COLUMN}' was not found in the dataset."
    )


# ==================================================
# STEP 3: DATA QUALITY
# ==================================================
print("\n===== STEP 3: DATA QUALITY =====")

missing = df.isnull().sum()

print("\nMissing values:")
if missing.sum() > 0:
    print(missing[missing > 0])
else:
    print("No missing values")

print("\nDuplicate rows:", df.duplicated().sum())


# ==================================================
# STEP 4: DESCRIPTIVE STATISTICS
# ==================================================
print("\n===== STEP 4: DESCRIPTIVE STATISTICS =====")

summary = df[num_cols].describe().T

summary["median"] = df[num_cols].median()
summary["variance"] = df[num_cols].var()
summary["IQR"] = summary["75%"] - summary["25%"]
summary["skewness"] = df[num_cols].skew()

print(summary.round(2))


# Identify distribution shape
print("\nDistribution shape:")

for col in num_cols:
    sk = summary.loc[col, "skewness"]

    if pd.isna(sk):
        shape = "cannot be determined"
    elif sk > 0.5:
        shape = "right-skewed"
    elif sk < -0.5:
        shape = "left-skewed"
    else:
        shape = "roughly symmetric"

    print(f"{col}: {shape}")


# Frequency counts for categorical columns
for col in cat_cols:
    print(f"\nCounts for '{col}':")
    print(df[col].value_counts(dropna=False))


# ==================================================
# STEP 5: DISTRIBUTIONS
# ==================================================
print("\n===== STEP 5: DISTRIBUTIONS =====")

target_data = pd.to_numeric(
    df[TARGET_COLUMN],
    errors="coerce"
).dropna()

if target_data.empty:
    raise ValueError(
        f"Target column '{TARGET_COLUMN}' has no valid numeric values."
    )

fig, axes = plt.subplots(
    1, 2,
    figsize=(11, 4)
)

# Histogram
sns.histplot(
    target_data,
    kde=True,
    ax=axes[0]
)

axes[0].axvline(
    target_data.mean(),
    linestyle="--",
    color="red",
    label="Mean"
)

axes[0].axvline(
    target_data.median(),
    color="green",
    label="Median"
)

axes[0].legend()
axes[0].set_title(f"Histogram of {TARGET_COLUMN}")

# Boxplot
sns.boxplot(
    x=target_data,
    ax=axes[1]
)

axes[1].set_title(f"Boxplot of {TARGET_COLUMN}")

plt.tight_layout()
plt.savefig("step5_distribution.png", dpi=120)
print("Chart saved: step5_distribution.png")
plt.show()


# ==================================================
# STEP 6: OUTLIER DETECTION
# ==================================================
print("\n===== STEP 6: OUTLIERS =====")

for col in num_cols:
    values = df[col].dropna()

    if values.empty:
        print(f"{col}: No valid numeric data")
        continue

    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)
    iqr = q3 - q1

    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr

    count = (
        (values < low) | (values > high)
    ).sum()

    print(
        f"{col:>10}: normal range = "
        f"[{low:.2f}, {high:.2f}] "
        f"-> outliers = {count}"
    )


# Display target column outliers
q1 = target_data.quantile(0.25)
q3 = target_data.quantile(0.75)
iqr = q3 - q1

outlier_mask = (
    (pd.to_numeric(df[TARGET_COLUMN], errors="coerce")
     < q1 - 1.5 * iqr)
    |
    (pd.to_numeric(df[TARGET_COLUMN], errors="coerce")
     > q3 + 1.5 * iqr)
)

outliers = df.loc[outlier_mask]

print(f"\nOutlier rows in '{TARGET_COLUMN}':")
print(outliers.head(10))


# ==================================================
# STEP 7: CORRELATION ANALYSIS
# ==================================================
print("\n===== STEP 7: CORRELATION =====")

corr = df[num_cols].corr()

print(corr.round(2))

plt.figure(figsize=(7, 5))

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1,
    vmax=1
)

plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("step7_correlation.png", dpi=120)

print("Chart saved: step7_correlation.png")
plt.show()


# ==================================================
# STEP 8: GROUP ANALYSIS
# ==================================================
if GROUP_COLUMN and GROUP_COLUMN in df.columns:

    print(
        f"\n===== STEP 8: {TARGET_COLUMN} "
        f"BY {GROUP_COLUMN} ====="
    )

    # Summary statistics by group
    group_summary = (
        df.groupby(GROUP_COLUMN)[TARGET_COLUMN]
        .agg([
            "count",
            "mean",
            "median",
            "std",
            "min",
            "max"
        ])
        .round(2)
    )

    print(group_summary)

    # Prepare bubble chart data
    if "units" in df.columns:
        bubble = (
            df.groupby(GROUP_COLUMN)
            .agg(
                avg_units=("units", "mean"),
                avg_sales=(TARGET_COLUMN, "mean"),
                orders=(TARGET_COLUMN, "count")
            )
            .reset_index()
        )

        print("\nBubble chart data:")
        print(bubble.round(2))

        plt.figure(figsize=(7, 4.5))

        sns.scatterplot(
            data=bubble,
            x="avg_units",
            y="avg_sales",
            size="orders",
            sizes=(400, 2500),
            hue=GROUP_COLUMN,
            alpha=0.6,
            legend=False
        )

        for _, row in bubble.iterrows():
            plt.text(
                row["avg_units"],
                row["avg_sales"],
                f"{row[GROUP_COLUMN]}\n({row['orders']})",
                ha="center",
                va="center",
                fontsize=8
            )

        plt.margins(0.25)
        plt.xlabel("Average units")
        plt.ylabel(f"Average {TARGET_COLUMN}")
        plt.title(
            f"Bubble Chart: {TARGET_COLUMN} by {GROUP_COLUMN}\n"
            "(Bubble size = number of orders)"
        )

        plt.tight_layout()
        plt.savefig("step8_groups.png", dpi=120)

        print("Chart saved: step8_groups.png")
        plt.show()

    else:
        print("Group bubble chart skipped: 'units' column not found.")


# ==================================================
# STEP 9: TIME TREND ANALYSIS
# ==================================================
if DATE_COLUMN and DATE_COLUMN in df.columns:

    print(
        f"\n===== STEP 9: TREND OF "
        f"{TARGET_COLUMN} OVER TIME ====="
    )

    # Prepare date and target data
    ts_df = df[[DATE_COLUMN, TARGET_COLUMN]].copy()

    ts_df[TARGET_COLUMN] = pd.to_numeric(
        ts_df[TARGET_COLUMN],
        errors="coerce"
    )

    ts_df = ts_df.dropna(
        subset=[DATE_COLUMN, TARGET_COLUMN]
    )

    ts = ts_df.set_index(DATE_COLUMN)[TARGET_COLUMN]

    # Monthly average
    monthly = ts.resample("ME").mean()

    # Fallback for older pandas versions
    if monthly.empty:
        monthly = ts.resample("M").mean()

    monthly = monthly.dropna()

    # Three-month rolling average
    rolling = monthly.rolling(
        window=3,
        min_periods=1
    ).mean()

    if len(monthly) >= 2:

        # Calculate trend line
        x = np.arange(len(monthly))

        slope, intercept = np.polyfit(
            x,
            monthly.values,
            1
        )

        # R-squared
        correlation = np.corrcoef(
            x,
            monthly.values
        )[0, 1]

        r_squared = correlation ** 2

        if slope > 0:
            direction = "UPWARD"
        elif slope < 0:
            direction = "DOWNWARD"
        else:
            direction = "FLAT"

        print("Trend direction :", direction)
        print(f"Slope           : {slope:.2f} per month")
        print(f"R-squared       : {r_squared:.2f}")

        # Plot the time trend
        plt.figure(figsize=(10, 4))

        plt.plot(
            monthly.index,
            monthly.values,
            marker="o",
            label="Monthly average"
        )

        plt.plot(
            monthly.index,
            rolling.values,
            linewidth=2,
            label="3-month rolling average"
        )

        plt.plot(
            monthly.index,
            intercept + slope * x,
            "r--",
            label="Trend line"
        )

        plt.title(f"Monthly Trend of {TARGET_COLUMN}")
        plt.xlabel("Date")
        plt.ylabel(TARGET_COLUMN)
        plt.legend()
        plt.tight_layout()

        plt.savefig("step9_trend.png", dpi=120)

        print("Chart saved: step9_trend.png")
        plt.show()

    else:
        print(
            "Trend analysis skipped: at least two valid "
            "monthly averages are required."
        )


# ==================================================
# STEP 10: BUBBLE CHART
# ==================================================
print("\n===== STEP 10: BUBBLE CHART =====")

required_columns = ["price", TARGET_COLUMN, "units", GROUP_COLUMN]

if all(
    col in df.columns
    for col in required_columns
):

    bubble_df = df.dropna(
        subset=["price", TARGET_COLUMN, "units", GROUP_COLUMN]
    ).copy()

    if not bubble_df.empty:

        plt.figure(figsize=(9, 6))

        sns.scatterplot(
            data=bubble_df,
            x="price",
            y=TARGET_COLUMN,
            size="units",
            hue=GROUP_COLUMN,
            sizes=(20, 400),
            alpha=0.6,
            edgecolor="black",
            linewidth=0.4
        )

        plt.title(
            "Bubble Chart: Price vs Sales "
            "(Bubble size = units)"
        )

        plt.xlabel("Price")
        plt.ylabel("Sales")

        plt.legend(
            bbox_to_anchor=(1.02, 1),
            loc="upper left"
        )

        plt.tight_layout()
        plt.savefig("step10_bubble.png", dpi=120)

        print("Chart saved: step10_bubble.png")
        plt.show()

    else:
        print("Bubble chart skipped: no complete rows available.")

else:
    print(
        "Bubble chart skipped: one or more required columns "
        "are missing."
    )


# ===========================================
# PROGRAM COMPLETED
# ==================================================
print("\n===== EDA COMPLETED SUCCESSFULLY =====")