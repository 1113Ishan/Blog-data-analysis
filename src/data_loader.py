import pandas as pd
from datetime import datetime

def load_and_clean(file_path):
        
    #load file
    df = pd.read_csv(file_path)

    #rename columns for sanity
    df = df.rename(columns={
        "Page path and screen class": "page_path",
        "Average engagement time per active user": "avg_engagement_time"
    })

    #classify the content based on page type
    def classify_content(path):
        if path == "/" or path.startswith("/search") or path.startswith("/p/"):
            return "non_content"
        if "blog-post" in path:
            return "placeholder"
        if "/2025" in path:
            return "article"
        return "unknown"

    df["content_type"] = df["page_path"].apply(classify_content)

    #category detection
    def detect_category(path):
        path = path.lower()

        if any(k in path for k in ["tech", "science", "ai", "coding", "design", "tools"]):
            return "Tech"
        if any(k in path for k in ["football", "league", "cup", "match", "sports"]):
            return "Sports"
        if any(k in path for k in ["movie", "film", "cinema"]):
            return "Movies"
        return"others"

    df["Category"] = df["page_path"].apply(detect_category)

    def extract_publish_date(path):
        try:
            parts = path.split("/")
            year = int(parts[1])
            month = int(parts[2])
            return datetime(year, month, 1)
        except:
            return None
        
    df["publish_date"] = df["page_path"].apply(extract_publish_date)

    today = datetime.today()
    df["article_age_days"] = df["publish_date"].apply(
        lambda x: (today-x).days if pd.notnull(x) else None
    )

    clean_df = df[df["content_type"] == "article"].copy()

    final_df = clean_df[[
        "page_path",
        "content_type",
        "Category",
        "Views",
        "Active users",
        "Views per active user",
        "avg_engagement_time",
        "article_age_days"
    ]]

    final_df.sort_values(by="Views", ascending=False, inplace=True)

    return final_df

