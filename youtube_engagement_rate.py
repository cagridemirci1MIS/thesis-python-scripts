# Author: Cagri Demirci
# Appendix A.3 – YouTube Engagement Rate Calculation
# Part of MSc Thesis (2025)

"""
YouTube Engagement Rate Calculator

This script calculates the engagement rate of YouTube videos
based on user interactions such as likes, comments, and views.

It is designed for data-driven analysis of audience interaction patterns
in digital communication studies. The formula used here is a standard
social media metric applied for cross-platform engagement comparisons.

Methodology
------------
Engagement Rate (%) = ((Likes + Comments) / Views) * 100

If view count is zero or missing, the function returns 0.0
to avoid division errors.

Dependencies
------------
- pandas

Usage Examples
---------------
# Example 1: Run directly
python youtube_engagement_rate.py

# Example 2: As a library
from youtube_engagement_rate import calculate_engagement_rate
rate = calculate_engagement_rate(likes=200, comments=30, views=5000)
print(rate)
"""

from __future__ import annotations
import pandas as pd


def calculate_engagement_rate(
    likes: int,
    comments: int,
    views: int,
) -> float:
    """
    Calculates the engagement rate for a single YouTube video.

    Parameters
    ----------
    likes : int
        Number of likes for the video.
    comments : int
        Number of comments for the video.
    views : int
        Number of total views for the video.

    Returns
    -------
    float
        Engagement rate as a percentage.
    """
    if views <= 0:
        return 0.0
    return ((likes + comments) / views) * 100.0


def engagement_rate_on_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies the engagement rate calculation across a DataFrame containing
    columns 'likes', 'comments', and 'views'.

    Returns a new DataFrame with an additional 'engagement_rate' column.
    """
    if not {"likes", "comments", "views"}.issubset(df.columns):
        raise ValueError("DataFrame must contain 'likes', 'comments', and 'views' columns")

    df = df.copy()
    df["engagement_rate"] = df.apply(
        lambda row: calculate_engagement_rate(row["likes"], row["comments"], row["views"]),
        axis=1,
    )
    return df


if __name__ == "__main__":
    # Minimal demonstration
    data = pd.DataFrame(
        {
            "video_id": ["vid001", "vid002", "vid003"],
            "likes": [120, 300, 0],
            "comments": [45, 100, 10],
            "views": [2000, 5000, 0],
        }
    )

    results = engagement_rate_on_dataframe(data)
    print("YouTube Engagement Rate Results:")
    print(results[["video_id", "engagement_rate"]])
