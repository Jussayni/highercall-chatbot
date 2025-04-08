import json
import re

# Load products
try:
    with open("products.json", "r") as f:
        products = json.load(f)
except FileNotFoundError:
    print("❌ products.json not found!")
    exit()
    
def search_products(user_question):
    keywords = user_question.lower().split()
    price_limit = None

    price_match = re.findall(r'\$?(\d+)', user_question)
    if price_match:
        price_limit = float(price_match[0])
        print(f"💲 Price limit: ${price_limit}")

    matches = []
    for p in products:
        name = p["name"].lower()

        # 🛠 Handle price parsing
        try:
            price = float(re.findall(r'\d+\.?\d*', p["price"])[0])
        except (ValueError, IndexError):
            price = None

        keyword_match = any(word in name for word in keywords)
        price_match = price is not None and (price_limit is None or price <= price_limit)

        if keyword_match or price_match:
            matches.append(p)

    return matches[:5]

def chatbot():
    print("💬 Ask me something (type 'exit' to quit).")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Goodbye!")
            break
        results = search_products(user_input)
        if results:
            print("Bot: Here are some things you might like:")
            for item in results:
                print(f"- {item['name']} ({item['price']}) → {item['link']}")
        else:
            print("Bot: Hmm... I couldn't find anything that matches. Try a different keyword?")

chatbot()
