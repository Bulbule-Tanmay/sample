API_KEY = "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"

import requests
import feedparser
import json



# -----------------------------
# GOOGLE NEWS FETCH
# -----------------------------
def get_google_news(prompt, limit=5):

    url = f"https://news.google.com/rss/search?q={prompt}&hl=en-IN&gl=IN&ceid=IN:en"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)

    feed = feedparser.parse(response.text)

    news = []

    for entry in feed.entries[:limit]:
        news.append(entry.title)

    return news


# -----------------------------
# ASK AI
# -----------------------------
def ask_ai(prompt):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "      ",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    result = response.json()

    return result["choices"][0]["message"]["content"]


# -----------------------------
# SYSTEM PROMPT
# -----------------------------
SYSTEM_PROMPT_new = """
You are Smart News Analyzer.

Your job is to verify whether a user claim is supported by real news headlines.

Rules:

1. Only use the news headlines provided.
2. Do not invent facts.
3. If headlines support the claim → Supported
4. If headlines contradict the claim → Contradicted
5. If headlines are related but unclear → Unverified
6. If headlines are unrelated → No Evidence

Return ONLY valid JSON:

{
"claim": "",
"verification_status": "",
"matching_headlines": [],
"conflicting_headlines": [],
"summary": "",
"confidence_score": 1-100
}
"""


# -----------------------------
# MAIN
# -----------------------------
# -----------------------------
# MAIN
# -----------------------------
prompt = input("Enter prompt: ")

# Properly format the YES/NO system prompt
system_prompt_YES = f"""{prompt} 
Is this prompt to be sent to Google News API to fetch headlines, 
or should it be sent directly to AI for a generic answer? 
Reply ONLY with YES (if it should be sent to Google News API) or NO(if it should be sent directly to AI). , goal use less API calls to Google News and more direct AI answers.
"""

system_prompt_no = f"""{prompt} , verify this and give me summary with confidence score between 0 to 100. Reply ONLY with the summary and confidence score."""

YES_NO = ask_ai(system_prompt_YES).strip().lower()

print(f"AI RESPONSE TO YES/NO: {YES_NO}")

if YES_NO == "yes":
    google_news = get_google_news(prompt)

    user_prompt = f"""
    USER CLAIM:
    {prompt}

    NEWS HEADLINES:
    {json.dumps(google_news, indent=2)}
    """

    print("\nAI OUTPUT:\n")
    final_output = ask_ai(SYSTEM_PROMPT_new + "\n\n" + user_prompt)
    print(final_output)

else:
    print("\nAI OUTPUT:\n")
    final_output = ask_ai(system_prompt_no)
    print(final_output)

print("done")
