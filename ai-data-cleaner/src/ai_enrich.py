import os
import json
from google import genai # Ath: breytt úr google.generativeai
from dotenv import load_dotenv

load_dotenv()

# Nýja leiðin til að búa til client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_text(text: str) -> dict:
    prompt = f"""Greindu þessa athugasemd viðskiptavinar á íslensku: "{text}"

Skilaðu JSON með nákvæmlega þessum reitum:
- sentiment: notaðu "jákvætt", "hlutlaust", eða "neikvætt"
- summary: stutt samantekt á íslensku (5-10 orð)

Dæmi:
{{"sentiment": "jákvætt", "summary": "Ánægður viðskiptavinur með hraða afhendingu"}}"""

    try:
        # Nýtt format á köllum: models.generate
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                response_mime_type='application/json',
                temperature=0.3
            )
        )

        # Svarið er nálgast svona í nýja safninu
        return json.loads(response.text)
        
    except Exception as e:
        print(f"Villa í API kalli: {e}")
        return {
            "sentiment": "óþekkt",
            "summary": "Gat ekki greint svar gervigreindarinnar"
        }