import sys
import os
import pandas as pd
from datetime import datetime
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fetch.fetch_api import fetch_github_issues
from fetch.fetch_csv import fetch_csv_feedback
from workdata.clean_text import clean_text
from workdata.validate_data import validate_incident_data
from llm.ai_decision import batch_analyze_incidents
from llm.ai_summary import summarize_feedback


def run_pipeline():
    # Sækja gögn
    api_df = fetch_github_issues(limit=5)
    api_df["source"] = "api"
    csv_df = fetch_csv_feedback()
    csv_df["source"] = "csv"
    combined_df = pd.concat([api_df, csv_df], ignore_index=True)
    combined_df = combined_df.head(5)
    print(f"Heildar: {len(combined_df)}")

    # Hreinsa og staðfesta
    combined_df["clean_text"] = combined_df["text"].apply(clean_text)
    combined_df["is_valid"] = combined_df.apply(
        lambda row: validate_incident_data(row["text"], row["source"]),
        axis=1
    )
    valid_df = combined_df[combined_df["is_valid"]]
    print(f"Gild atvik: {len(valid_df)}")

    # AI greining
    incidents = [
        {"text": row["text"], "source": row["source"]}
        for _, row in valid_df.iterrows()
    ]
    decisions = batch_analyze_incidents(incidents)
    valid_df["severity"] = [d["severity"] for d in decisions]
    valid_df["category"] = [d["category"] for d in decisions]

    # Sýna niðurstöður
    print("\nNiðurstöður:")
    for severity, count in valid_df["severity"].value_counts().items():
        print(f"  {severity}: {count}")

    # Vista niðurstöður
    print("\nVista..")
    os.makedirs("output", exist_ok=True)

    with open("output/decisions.json", "w") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "decisions": decisions}, f, indent=2)

    valid_df.to_csv("output/processed_incidents.csv", index=False)

    summary_report = summarize_feedback(valid_df["clean_text"].tolist())
    with open("output/summary_report.md", "w") as f:
        f.write(f"# Atvikagreiningarskýrsla\n\n")
        f.write(f"**Búið til:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(summary_report)


if __name__ == "__main__":
    run_pipeline()