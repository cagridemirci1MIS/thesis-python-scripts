# ============================
# FINAL EDA + VISUALIZATION (Thesis Version)
# ============================

!pip install -q pandas numpy matplotlib seaborn openpyxl xlsxwriter

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ---- File Paths ----
P_TRANSCRIPT_XLSX = "/content/31_satir_veriseti__with_detect.xlsx"
P_ENGAGEMENT_XLSX = "/content/youtube_engagement_rates.xlsx"

# ---- Safe Read Function ----
def safe_read(path):
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return pd.DataFrame()
    try:
        if path.lower().endswith(".xlsx"):
            return pd.read_excel(path)
        elif path.lower().endswith(".csv"):
            return pd.read_csv(path)
    except Exception as e:
        print(f"⚠️ Error reading {path}: {e}")
        return pd.DataFrame()
    return pd.DataFrame()

# ---- Load Data ----
trans = safe_read(P_TRANSCRIPT_XLSX)
eng = safe_read(P_ENGAGEMENT_XLSX)

print("Transcript shape:", trans.shape)
print("Engagement shape:", eng.shape)

if trans.empty or eng.empty:
    raise RuntimeError("⚠️ One or both datasets are empty. Please upload both files to /content.")

# ---- Normalize column names ----
eng.columns = [c.strip().lower() for c in eng.columns]
rename_map = {
    "views": "views",
    "likes": "likes",
    "comments": "comments",
    "subscribers": "subscribers",
    "impressions": "impressions",
    "reach": "reach",
    "er_view_%": "ER_View_%",
    "er_subscriber_%": "ER_Subscriber_%"
}
eng = eng.rename(columns=rename_map)

# ---- Convert numeric formats (comma → dot, strings → numbers) ----
for c in eng.columns:
    if eng[c].dtype == object:
        eng[c] = eng[c].astype(str).str.replace(",", ".").str.replace(" ", "")
        eng[c] = pd.to_numeric(eng[c], errors="ignore")

numeric_cols_to_convert = ["views", "likes", "comments", "subscribers", "ER_View_%", "ER_Subscriber_%"]
for c in numeric_cols_to_convert:
    if c in eng.columns:
        eng[c] = pd.to_numeric(eng[c], errors="coerce")

# ---- Numeric Columns ----
num_cols = [c for c in ["views","likes","comments","subscribers","ER_View_%","ER_Subscriber_%"] if c in eng.columns]
print("\nNumeric columns:", num_cols)

# ---- Descriptive Statistics ----
if num_cols:
    print("\n--- Descriptive Statistics ---")
    display(eng[num_cols].describe().round(2))
else:
    print("⚠️ No numeric columns found.")

# ---- QC Report ----
qc = {
    "Video Count": len(eng),
    "Average ER_View_%": round(eng["ER_View_%"].mean(), 2) if "ER_View_%" in eng.columns else "-",
    "Average ER_Subscriber_%": round(eng["ER_Subscriber_%"].mean(), 2) if "ER_Subscriber_%" in eng.columns else "-",
    "Max ER_View_%": round(eng["ER_View_%"].max(), 2) if "ER_View_%" in eng.columns else "-",
    "Max ER_Subscriber_%": round(eng["ER_Subscriber_%"].max(), 2) if "ER_Subscriber_%" in eng.columns else "-",
}
print("\n📊 QC REPORT:")
for k, v in qc.items():
    print(f"- {k}: {v}")

# ============================
# VISUALIZATION SECTION
# ============================

os.makedirs("/content/eda_images", exist_ok=True)
sns.set(style="whitegrid")

# 1. Histogram – ER_View_%
if "ER_View_%" in eng.columns:
    plt.figure(figsize=(6,4))
    sns.histplot(eng["ER_View_%"].dropna(), bins=15, kde=True, color="skyblue")
    plt.xlabel("Engagement Rate (per View) [%]", fontsize=11)
    plt.ylabel("Frequency", fontsize=11)
    plt.tight_layout()
    plt.savefig("/content/eda_images/hist_ER_View.png", dpi=300)
    plt.close()

# 2. Histogram – ER_Subscriber_%
if "ER_Subscriber_%" in eng.columns:
    plt.figure(figsize=(6,4))
    sns.histplot(eng["ER_Subscriber_%"].dropna(), bins=15, kde=True, color="lightcoral")
    plt.xlabel("Engagement Rate (per Subscriber) [%]", fontsize=11)
    plt.ylabel("Frequency", fontsize=11)
    plt.tight_layout()
    plt.savefig("/content/eda_images/hist_ER_Subscriber.png", dpi=300)
    plt.close()

# 3. Scatter – Subscribers vs ER_View
if all(c in eng.columns for c in ["subscribers", "ER_View_%"]):
    plt.figure(figsize=(6,4))
    sns.scatterplot(data=eng, x="subscribers", y="ER_View_%", alpha=0.8)
    plt.xlabel("Subscribers", fontsize=11)
    plt.ylabel("Engagement Rate (per View) [%]", fontsize=11)
    plt.tight_layout()
    plt.savefig("/content/eda_images/scatter_subs_vs_erview.png", dpi=300)
    plt.close()

# 4. Heatmap – Spearman correlations
corr_cols = [c for c in ["views","likes","comments","subscribers","ER_View_%","ER_Subscriber_%"] if c in eng.columns]
if len(corr_cols) >= 3:
    plt.figure(figsize=(6,5))
    corr = eng[corr_cols].corr(method="spearman")
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f",
                cbar_kws={"label": "Spearman Correlation"})
    plt.xlabel("Variables", fontsize=11)
    plt.ylabel("Variables", fontsize=11)
    plt.tight_layout()
    plt.savefig("/content/eda_images/heatmap_spearman.png", dpi=300)
    plt.close()

# ============================
# DONE
# ============================

print("\n✅ EDA and visualizations completed successfully.")
print("Saved figures in /content/eda_images/:")
print(os.listdir("/content/eda_images"))
