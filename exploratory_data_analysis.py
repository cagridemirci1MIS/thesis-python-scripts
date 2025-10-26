# Author: Cagri Demirci
# Appendix A.4 – Exploratory Data Analysis (EDA) for Social Media Text Data
# Part of MSc Thesis (2025)

"""
Exploratory Data Analysis (EDA) Script

This script performs an initial exploratory analysis on social media datasets,
focusing on basic statistics, text length distribution, and frequent token patterns.
It provides an overview of the dataset’s linguistic and engagement characteristics
to guide later modeling or annotation steps.

Methodology
------------
1) Load dataset (CSV, JSON, or other structured format).
2) Compute key descriptive statistics:
   - Text length (in tokens)
   - Word frequency distribution
   - Missing value count
3) Visualize (optionally) using matplotlib (if available).
4) Export summary tables as CSV if required.

Dependencies
------------
- pandas
- re
- matplotlib (optional)

Usage Examples
---------------
# Example 1: Run directly
python exploratory_data_analysis.py data.csv

# Example 2: Import as library
from exploratory_data_analysis import eda_summary
summary = eda_summary("data.csv")
print(summary.head())
"""

from __future__ import annotations
import sys
import re
from typing import Optional
import pandas as pd

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def tokenize(text: str) -> list[str]:
    """Simple alphanumeric tokenizer for Turkish-English mixed texts."""
    return [t for t in re.split(r"[^A-Za-zÀ-ÖØ-öø-ÿĞÜŞİğüşiçÇ]+", text) if t]


def eda_summary(
    filepath: str,
    text_column: str = "text",
    output_csv: Optional[str] = None,
    visualize: bool = False,
) -> pd.DataFrame:
    """
    Performs a lightweight exploratory data analysis on a text dataset.

    Parameters
    ----------
    filepath : str
        Path to the dataset file (CSV or JSON).
    text_column : str
        Column name containing text data.
    output_csv : Optional[str]
        If provided, saves summary statistics to this file.
    visualize : bool
        If True, displays simple histograms for text length.

    Returns
    -------
    pd.DataFrame
        Summary statistics for each entry.
    """
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    elif filepath.endswith(".json"):
        df = pd.read_json(filepath)
    else:
        raise ValueError("Unsupported file format. Use CSV or JSON.")

    if text_column not in df.columns:
        raise KeyError(f"Column '{text_column}' not found in dataset.")

    # Drop missing entries
    df = df.dropna(subset=[text_column])
    df[text_column] = df[text_column].astype(str)

    df["token_count"] = df[text_column].apply(lambda x: len(tokenize(x)))
    df["char_count"] = df[text_column].apply(len)

    # Basic descriptive statistics
    summary = df[["token_count", "char_count"]].describe()

    if visualize and plt is not None:
        plt.figure(figsize=(8, 5))
        df["token_count"].hist(bins=30, color="skyblue", edgecolor="black")
        plt.title("Token Count Distribution")
        plt.xlabel("Number of Tokens")
        plt.ylabel("Frequency")
        plt.show()

    if output_csv:
        summary.to_csv(output_csv)

    return summary


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python exploratory_data_analysis.py <dataset.csv>")
        sys.exit(1)

    filepath = sys.argv[1]
    print(f"Running EDA on: {filepath}")
    summary_stats = eda_summary(filepath, visualize=False)
    print("Summary Statistics:")
    print(summary_stats)
