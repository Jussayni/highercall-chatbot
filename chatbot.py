from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import re

app = FastAPI()

# Enable access from your website
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load products on startup
with open("products.json", "r") as f:
    products = json.load(f)

def search_products(user_question):
    keywords = user_question.lower().split()
    price_limit = None

    price_match = re.findall(r'\$?(\d+)', user_question)
    if price_match:
        price_limit = float(price_match[0])

    matches = []
    for p in products:
        name = p["name"].lower()

        try:
            price = float(re.findall(r'\d+\.?\d*', p["price"])[0])
        except (ValueError, IndexError):
            price = None

        keyword_match = any(word in name for word in keywords)
        price_match_ok = price is not None and (price_limit is None or price <= price_limit)

        if keyword_match or price_match_ok:
            matches.append(p)

    return matches[:5]

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    question = data.get("message", "")
    results = search_products(question)

    if not results:
        return {"reply": "Sorry, I couldn't find anything that matches. Try a different question?"}

    reply = "Here are some things you might like:\n"
    for item in results:
        reply += f"- {item['name']} ({item['price']}) → {item['link']}\n"
    return {"reply": reply}
