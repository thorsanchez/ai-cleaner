import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
def summarize_feedback(cleaned_texts: list) -> str:
    """
    Summarize customer feedback from multiple data sources.

    Parameters:
    - cleaned_texts: List of cleaned feedback strings (API + CSV combined)

    Returns:
    - Markdown-formatted summary report as a string
    """
    if not cleaned_texts:
        return "No data available"
    #setja limit a input stærð
    sample_texts = cleaned_texts[:30]

    formatted_feedback = "\n".join(
        f"-{text}" for text in sample_texts if text.strip()
    )
    prompt = f"""
    You are a data analyst working with customer feedback.

    Analyze the following feedback collected from multiple sources:

    {formatted_feedback}

    Return a Markdown report with the following sections:

    ## Overall Sentiment
    ## Common Themes
    ## Frequent Issues
    ## Actionable Recommendations

    Keep the tone professional and business-focused.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content

    return str(content)