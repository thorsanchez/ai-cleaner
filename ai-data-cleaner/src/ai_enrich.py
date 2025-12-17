import os
import json
from openai import OpenAi
from dotenv import load_dotenv

#lesa env skra
load_dotenv()
#client obj til að geta kallað a api
client = OpenAi(api_key=os.getenv("OPEN_AI_KEY"))

def analyze_text(text:str) -> dict:
    prompt = f""" Þú ert aðstoðarmaður í gagnavinnslu. Greindu eftirfarandi athugasemd viðskiptavinar: "{text}" 
    Skilaðu JSON-hlut með nákvæmlega þessum reitum: 
    - sentiment: jákvætt, hlutlaust, eða neikvætt 
    - summary: ein stutt setning á íslensku """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2, # lagt fyrir data pipeline
    )
    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
        "sentiment": "óþekkt",
        "summary": "Gat ekki greint svar gervigreindarinnar"
        }