# Sweet Crumbs Home Bakery: Python Fundamentals & AI Chatbot Curriculum

A comprehensive collection of Python scripts and LangChain examples demonstrating the progression from core Python programming concepts to a stateful, production-ready customer service chatbot for **Sweet Crumbs Home Bakery**.

---

## 📋 Overview

This repository is structured into two main learning tracks:
1. **Python Foundations for AI:** Practical exercises covering data structures, JSON serialization, type-hinted functions, decorators, and robust exception handling.
2. **LLM Integration & Chatbot Architecture:** Step-by-step evolution from raw OpenAI-compatible Groq API calls to LangChain Expression Language (LCEL) chains and a multi-turn conversational agent with memory.

---

## 🛠️ Prerequisites & Setup

### 1. Install Dependencies
```bash
pip install langchain-groq langchain-core openai
```

### 2. Set Your Groq API Key
Export your API key as an environment variable before running the scripts:
```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

---

## 📚 Module Breakdown

### Part 1: Core Python Concepts
* **Topic 06 — Dictionaries & JSON:**
  * Managing bakery menu pricing (`MENU` dictionary) and safe lookups using `.get()` to avoid `KeyError`.
  * Creating structured customer order objects and serializing/deserializing data with `json.dumps()` and `json.loads()`.
* **Topic 07 — Functions, Type Hints & Docstrings:**
  * Implementing `get_price(item: str, qty: int = 1) -> int` with input normalization (`.lower().strip()`) and clear documentation.
* **Topic 08 — Decorators:**
  * Building a reusable `@log_call` decorator using `functools.wraps` to trace function arguments and return values without altering core business logic.
* **Topic 09 — Exception Handling (`try / except`):**
  * Gracefully handling `ValueError` (invalid numeric inputs), `KeyError` (unavailable menu items), `json.JSONDecodeError` (malformed JSON), and `ZeroDivisionError`.

---

### Part 2: Building the Bakery AI Assistant

#### 1. API Evolution (Raw SDK vs. LangChain)
* **Raw OpenAI SDK (`openai`):** Direct calls to Groq's OpenAI-compatible endpoint (`https://api.groq.com/openai/v1`) using `openai/gpt-oss-20b`.
* **LangChain (`ChatGroq`):** Simplified invocation using `ChatGroq`, system/human message tuples, reusable `ChatPromptTemplate` placeholders, and LCEL pipelines (`prompt | llm | StrOutputParser()`).

#### 2. Complete Stateful Chatbot
Combines all previous Python and LLM concepts into an interactive terminal chatbot:
* **Dynamic System Prompt:** Injects the JSON-formatted `MENU` directly into the system instructions, enforcing rules (24-hour notice, eggless availability, bilingual English/Telugu support, <50-word responses).
* **Sliding-Window Memory:** Maintains conversation context (`history`) while capping retained messages (`MAX_TURNS = 8`) to manage token usage.
* **Resilient Error Handling:** Catches `RateLimitError`, `AuthenticationError`, and `APIConnectionError` to return polite fallback messages instead of crashing.
* **Interactive Loop:** Runs continuously until the user types `bye`, `exit`, or `quit`.

---

## 🚀 Usage

Run any standalone block or start the interactive bakery assistant directly:
```bash
python bakery_chatbot.py
```

### Example Interaction
```text
Total for 6 cupcakes: 480
You: Hi, I'm Ravi. How much for 2 plum cakes?
Bot: Hi Ravi! Two plum cakes are ₹1,000 total. All our cakes have eggless versions and require 24 hours' notice. Would you like to place an order?
You: bye
Bot: Thank you for visiting Sweet Crumbs!
```

