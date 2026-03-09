import pandas as pd
import numpy as np

def content_counts(df):
    return df["content_type"].value_counts()

def category_counts(df):
    return df["Category"].value_counts()

def view_statistics(df):
    return {
        "total_views": df["Views"].sum(),
        "mean_views": df["Views"].mean(),
        "median_views": df["Views"].median(),
        "avg_engagement_time": df["avg_engagement_time"].mean()
    }

def category_performance(df):
    return df.groupby("Category")["Views"].agg(["count", "mean", "median"])


def article_status(df, threshold=5):
    df_copy = df.copy()

    mask = df_copy["content_type"] == "article"

    df_copy.loc[mask, "Status"] = np.where(
        df_copy.loc[mask, "Views"] <= threshold,
        "Zombie",
        "Active"
    )

    return df_copy

def top_articles(df, n=3):
    return df.nlargest(n, "Views")[["page_path","Views","Category","avg_engagement_time"]]

def bottom_articles(df, n=3):
    return df.nsmallest(n, "Views")[["page_path","Views","Category","avg_engagement_time"]]

def engagement_rate(df):
    df_articles = df[df["content_type"]=="article"]
    return (df_articles["avg_engagement_time"]/ df_articles['Views']).mean()


def zombie_ratio_by_category(df, threshold=5):
    df_articles = df[df["content_type"]=="article"].copy()

    df_articles["Status"] = df_articles["Views"].apply(
        lambda x: "Zombie" if x <= threshold else "Active"
    )

    return(
        df_articles.groupby("Category")["Status"]
        .value_counts(normalize=True)
        .unstack()
    )

