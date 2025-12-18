import pandas as pd
from fetch_api import fetch_comments
from clean_text import clean_text
from ai_summary import analyze_text

output_path = "output/dailyreport.md"

def main():
    #fetch data fra api
    df = fetch_comments(limit=5)

    #clean comments
    df["clean_body"] = df["body"].apply(clean_text)

    #ai sum
    report = analyze_text(df["clean_body"].tolist())

    #vista i md skjal
    with open(output_path, "w") as f:
        f.write(str(report))
    
    print(f"report er í: {output_path}")

if __name__ == "__main__":
    main()