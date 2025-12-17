import pandas as pd
from clean_text import clean_text
from ai_enrich import analyze_text

input_path ="data/input.csv"
output_path = "data/output.csv"

def main():
    df = pd.read_csv(input_path)
    #clean txt
    df["clean_text"] = df["comment"].apply(clean_text)
    sentiments = []
    summaries = []

    for text in df["clean_text"]:
        #senda i llm
        result = analyze_text(text)
        #get() og ekki result[] (crash)
        sentiments.append(result.get("sentiment"))
        summaries.append(result.get("summary"))

    #bæta við cols i data frame
    df["sentiment"] = sentiments
    df["summary"] = summaries
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    main()