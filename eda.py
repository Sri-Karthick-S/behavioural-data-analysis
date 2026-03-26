import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

# Loading the data
df_raw = pd.read_csv("mxmh_survey_results.csv")
print("Shape:", df_raw.shape)
print("\nColumns:\n", df_raw.columns.tolist())
print(df_raw.dtypes)

missing = df_raw.isnull().sum()
missing_pct = (missing / len(df_raw) * 100).round(2)
missing_report = pd.DataFrame({"Missing Count": missing, "Missing %": missing_pct})
missing_report = missing_report[missing_report["Missing Count"] > 0].sort_values("Missing %", ascending=False)
print(missing_report)

print(f"Duplicate rows: {df_raw.duplicated().sum()}")
print(df_raw.describe())

# Preprocessing
genre_columns = [col for col in df_raw.columns if col.startswith("Frequency [")]
selected_columns = [
    "Age", "Primary streaming service", "Hours per day", "While working",
    "Instrumentalist", "Composer", "Fav genre", "Exploratory", "Foreign languages",
    "Anxiety", "Depression", "Insomnia", "OCD", "Music effects"
] + genre_columns

df = df_raw[selected_columns].copy()

for col in ["Instrumentalist", "Foreign languages", "While working",
            "Primary streaming service", "Composer"]:
    df[col].fillna(df[col].mode()[0], inplace=True)

# Impute Age with median
df["Age"] = df["Age"].fillna(df["Age"].median())

df.dropna(subset=["Music effects"], inplace=True)

# Remove outliers
df = df[(df["Age"] >= 10) & (df["Age"] <= 90)]
df = df[df["Hours per day"] <= 24]

freq_map = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Very frequently": 3}
df[genre_columns] = df[genre_columns].apply(lambda x: x.map(freq_map))

# Encode binary columns
binary_map = {"Yes": 1, "No": 0}
binary_cols = ["While working", "Instrumentalist", "Composer", "Exploratory", "Foreign languages"]
df[binary_cols] = df[binary_cols].apply(lambda x: x.map(binary_map))

# Feature Engineering
df["Total Distress Score"] = df[["Anxiety", "Depression", "Insomnia", "OCD"]].sum(axis=1)

q1, q2 = df["Total Distress Score"].quantile([1/3, 2/3])
df["Distress Category"] = pd.cut(
    df["Total Distress Score"],
    bins=[-1, q1, q2, 40],
    labels=["Low", "Moderate", "High"]
)

# Age groups
age_bins = [10, 20, 30, 40, 50, 60, 100]
age_labels = ["10-20", "21-30", "31-40", "41-50", "51-60", "61+"]
df["AgeGroup"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels, include_lowest=True).astype(str)

# Convert floats to int where appropriate
float_cols = df.select_dtypes(include="float64").columns.tolist()
for c in ["Hours per day", "Age"]:
    if c in float_cols:
        float_cols.remove(c)
df[float_cols] = df[float_cols].astype(int)

print(f"\nClean dataset shape: {df.shape}")

# Univariate Analysis
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
fig.suptitle("Univariate Analysis")

df["Age"].plot(kind="hist", bins=20, ax=axes[0, 0], title="Age Distribution")
axes[0, 0].set_xlabel("Age")

df["Hours per day"].plot(kind="hist", bins=20, ax=axes[0, 1], title="Hours Listening Per Day")
axes[0, 1].set_xlabel("Hours")

df["Total Distress Score"].plot(kind="hist", bins=20, ax=axes[0, 2], title="Total Distress Score")
axes[0, 2].set_xlabel("Score")

df["Fav genre"].value_counts().plot(kind="bar", ax=axes[1, 0], title="Favourite Genre")
axes[1, 0].set_xlabel("Genre")
axes[1, 0].tick_params(axis="x", rotation=45)

df["Primary streaming service"].value_counts().plot(kind="bar", ax=axes[1, 1], title="Streaming Service")
axes[1, 1].set_xlabel("Service")
axes[1, 1].tick_params(axis="x", rotation=45)

df["Music effects"].value_counts().plot(kind="bar", ax=axes[1, 2], title="Perceived Music Effect")
axes[1, 2].set_xlabel("Effect")

plt.tight_layout()
plt.savefig("eda_01_univariate.png", bbox_inches="tight")
plt.show()

# ==============================================================================
# 5. MENTAL HEALTH INDICATORS
# ==============================================================================
mh_cols = ["Anxiety", "Depression", "Insomnia", "OCD"]

fig, axes = plt.subplots(1, 4, figsize=(16, 5))
fig.suptitle("Mental Health Indicators")
for i, col in enumerate(mh_cols):
    df[col].plot(kind="box", ax=axes[i], title=col)
    axes[i].set_ylabel("Score (0-10)")
plt.tight_layout()
plt.savefig("eda_02_mh_distributions.png", bbox_inches="tight")
plt.show()

# Correlation heatmap
fig, ax = plt.subplots(figsize=(7, 5))
corr = df[mh_cols + ["Total Distress Score"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
ax.set_title("Mental Health Correlation Matrix")
plt.tight_layout()
plt.savefig("eda_03_mh_correlation.png", bbox_inches="tight")
plt.show()

# ==============================================================================
# 6. GENRE vs MENTAL HEALTH
# ==============================================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle("Genre vs Mental Health Indicators")
for ax, col in zip(axes.flatten(), mh_cols):
    df.groupby("Fav genre")[col].median().sort_values(ascending=False).plot(kind="bar", ax=ax, title=f"Median {col} by Genre")
    ax.set_xlabel("Genre")
    ax.set_ylabel(f"{col} Score")
    ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
plt.savefig("eda_04_genre_vs_mh.png", bbox_inches="tight")
plt.show()

# ==============================================================================
# 7. LISTENING HOURS vs DISTRESS
# ==============================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Listening Hours vs Distress")

axes[0].scatter(df["Hours per day"], df["Total Distress Score"], alpha=0.3)
m, b, r, p, _ = stats.linregress(df["Hours per day"], df["Total Distress Score"])
x_line = np.linspace(0, df["Hours per day"].max(), 100)
axes[0].plot(x_line, m * x_line + b, color="black")
axes[0].set_xlabel("Hours / Day")
axes[0].set_ylabel("Total Distress Score")
axes[0].set_title(f"Scatter (r={r:.2f}, p={p:.3f})")

df.boxplot(column="Hours per day", by="Distress Category", ax=axes[1])
axes[1].set_title("Hours per Day by Distress Category")
axes[1].set_xlabel("Distress Category")
axes[1].set_ylabel("Hours / Day")

plt.tight_layout()
plt.savefig("eda_05_hours_vs_distress.png", bbox_inches="tight")
plt.show()

# ==============================================================================
# 8. AGE GROUP PATTERNS
# ==============================================================================
age_order = ["10-20", "21-30", "31-40", "41-50", "51-60", "61+"]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Age Group Patterns")

df.groupby("AgeGroup")["Total Distress Score"].mean().reindex(age_order).plot(kind="bar", ax=axes[0], title="Avg Distress Score by Age Group")
axes[0].set_xlabel("Age Group")
axes[0].set_ylabel("Avg Distress Score")

df.boxplot(column="Hours per day", by="AgeGroup", ax=axes[1])
axes[1].set_title("Listening Hours by Age Group")
axes[1].set_xlabel("Age Group")
axes[1].set_ylabel("Hours / Day")

plt.tight_layout()
plt.savefig("eda_06_age_patterns.png", bbox_inches="tight")
plt.show()

# ==============================================================================
# 9. PERCEPTION vs REALITY
# ==============================================================================
df["MH_Category"] = pd.cut(
    df["Total Distress Score"],
    bins=[-1, 10, 20, 40],
    labels=["Low", "Moderate", "High"]
)
df["mismatch"] = (
    ((df["Music effects"] == "Improve") & (df["MH_Category"] == "High")) |
    ((df["Music effects"] == "Worsen") & (df["MH_Category"] == "Low"))
).astype(int)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Perception vs Reality")

df.boxplot(column="Total Distress Score", by="Music effects", ax=axes[0])
axes[0].set_title("Distress Score by Perceived Music Effect")
axes[0].set_xlabel("Perceived Effect")
axes[0].set_ylabel("Total Distress Score")

mismatch_by_genre = df.groupby("Fav genre")["mismatch"].mean().sort_values(ascending=False) * 100
mismatch_by_genre.plot(kind="bar", ax=axes[1], title="Mismatch Rate (%) by Genre")
axes[1].set_xlabel("Genre")
axes[1].set_ylabel("Mismatch %")
axes[1].tick_params(axis="x", rotation=45)
axes[1].axhline(df["mismatch"].mean() * 100, color="red", linestyle="--", label="Overall avg")
axes[1].legend()

plt.tight_layout()
plt.savefig("eda_07_perception_reality.png", bbox_inches="tight")
plt.show()

# ==============================================================================
# 10. STATISTICAL TESTS
# ==============================================================================
print("\n" + "="*60)
print("STATISTICAL TESTS")
print("="*60)

# Kruskal-Wallis: Distress across genres
groups = [group["Total Distress Score"].values for _, group in df.groupby("Fav genre")]
stat, p = stats.kruskal(*groups)
print(f"\n[Kruskal-Wallis] Distress Score across Genres")
print(f"  H={stat:.2f}, p={p:.4f} → {'Significant' if p < 0.05 else 'Not significant'}")

# Pearson: Hours vs Distress
r, p = stats.pearsonr(df["Hours per day"], df["Total Distress Score"])
print(f"\n[Pearson] Hours/Day vs Total Distress Score")
print(f"  r={r:.3f}, p={p:.4f} → {'Significant' if p < 0.05 else 'Not significant'}")

# Chi-square: Music effects vs Distress Category
ct = pd.crosstab(df["Music effects"], df["Distress Category"])
chi2, p, dof, _ = stats.chi2_contingency(ct)
print(f"\n[Chi-Square] Music Effects vs Distress Category")
print(f"  chi2={chi2:.2f}, dof={dof}, p={p:.4f} → {'Significant' if p < 0.05 else 'Not significant'}")

# Mann-Whitney: Work listeners vs non-work listeners
work_yes = df[df["While working"] == 1]["Total Distress Score"]
work_no  = df[df["While working"] == 0]["Total Distress Score"]
stat, p = stats.mannwhitneyu(work_yes, work_no, alternative="two-sided")
print(f"\n[Mann-Whitney] Distress: Work listeners vs Non-work listeners")
print(f"  U={stat:.0f}, p={p:.4f} → {'Significant' if p < 0.05 else 'Not significant'}")

# ==============================================================================
# 11. EXPORT
# ==============================================================================
df.to_csv("mxmh_cleaned.csv", index=False, encoding="utf-8")
print(f"\nExported: mxmh_cleaned.csv | Shape: {df.shape}")
