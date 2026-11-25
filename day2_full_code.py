import json
import functools
import os

from openai import OpenAI, RateLimitError, APIConnectionError, AuthenticationError


# 1. API CLIENT SETUP

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

if not os.environ.get("GROQ_API_KEY"):
    raise ValueError("Please set your GROQ_API_KEY first.")


# 2. MODEL AND MENU

MODEL = "openai/gpt-oss-20b"

MENU = {
    "plum cake": 500,
    "chocolate cake": 650,
    "cupcake": 80
}


# 3. SYSTEM PROMPT

SYSTEM = f"""ROLE:   You are the friendly assistant for Sweet Crumbs Home Bakery.
FACTS:  Menu with prices in rupees: {json.dumps(MENU)}
        Orders need 24 hours' notice. All cakes have eggless versions.
RULES:  Never promise a delivery time. If it isn't in FACTS, say "I'll check with the owner."
        Remember the customer's name and order during the chat.
FORMAT: Under 50 words, friendly, English or Telugu matching the customer."""


# 4. DECORATOR

def log_call(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)

        print(f"   [log] {func.__name__}{args} -> {result!r}")

        return result

    return wrapper

# 5. PRICE FUNCTION

@log_call
def get_price(item: str, qty: int = 1) -> int:
    """Return the total price in rupees for qty of an item on the menu."""

    return MENU[item.lower().strip()] * qty

# 6. CHAT HISTORY / MEMORY

history = [
    {"role": "system", "content": SYSTEM}
]

MAX_TURNS = 8


# 7. CHAT FUNCTION

def chat(user_text: str) -> str:

    history.append({
        "role": "user",
        "content": user_text
    })

    recent = [history[0]] + history[1:][-MAX_TURNS:]

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=recent,
            temperature=0.3
        )

        reply = response.choices[0].message.content

    except RateLimitError:

        reply = "We're a little busy. Please try again in a minute."

    except AuthenticationError:

        reply = "Setup problem: please tell the owner the API key isn't working."

    except APIConnectionError:

        reply = "I can't reach the server right now. Please try again shortly."

    history.append({
        "role": "assistant",
        "content": reply
    })

    return reply


# 8. TEST PRICE FUNCTION

print("Total for 6 cupcakes:", get_price("cupcake", 6))


# 9. CHATBOT LOOP

while True:

    text = input("You: ")

    if text.lower().strip() in ("bye", "exit", "quit"):

        print("Bot: Thank you for visiting Sweet Crumbs!")

        break

    print("Bot:", chat(text))