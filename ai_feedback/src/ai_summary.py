import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_text(comments: list) -> str:
    #taka inn lista af clean comments og skila summary
    #comments saman i einn streng (passa að ekki hafa of langt með limit)
    text_block = "\n".join(comments[:20])

    prompt = f"""
You are a data analyst assistant.

Analyze the following customer comments:

{text_block}

Return a Markdown report summarizing:
- Overall sentiment (positive, neutral, negative)
- Most common themes/issues
- Key insights or recommendations
"""
    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                response_mime_type='application/json',
                temperature=0.3
            )
        )


        return json.loads(response.text)
        
    except Exception as e:
        print(f"Villa í API kalli: {e}")
    
    content = response.choices[0].message.content
    return content