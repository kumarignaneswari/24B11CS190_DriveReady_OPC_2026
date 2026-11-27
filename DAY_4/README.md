# 🍰 Sweet Crumbs – AI-Powered Bakery Order Assistant

## 1. Project Overview

Sweet Crumbs is an AI-powered order assistant developed for a home bakery using **LangChain, Groq LLM, Google Colab, and Google Sheets**.

The assistant interacts with customers through natural language and helps them:
- Check bakery opening hours.
- Get cake prices.
- Place cake orders.
- Request eggless cakes.
- Save customer orders automatically to Google Sheets.

The assistant understands customer messages in English and Telugu and responds in a friendly manner.

## 2. Project Objectives

The main objective is to build an AI agent that automates basic bakery operations.

The system should:

1. Understand customer questions.
2. Retrieve accurate cake prices using tools.
3. Check bakery opening hours.
4. Collect all required order details.
5. Validate customer orders.
6. Calculate the total price.
7. Store confirmed orders in Google Sheets.
8. Maintain conversation history.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Google Colab | Development and execution environment |
| LangChain | Building the AI agent |
| Groq API | Providing LLM capabilities |
| GPT-OSS-20B | Language model |
| Pydantic | Order data validation |
| Google Sheets | Storing customer orders |
| gspread | Connecting Python with Google Sheets |

## 4. Bakery Information

### Menu and Pricing

| Item | Price |
|---|---:|
| Plum Cake | ₹500 |
| Chocolate Cake | ₹650 |
| Cupcake | ₹80 |

### Opening Hours

| Day | Timings |
|---|---|
| Monday – Saturday | 9 AM – 8 PM |
| Sunday | 10 AM – 6 PM |

Additional business rules:

- All cakes are available in eggless versions.
- Orders require at least 24 hours' notice.
- Customers must provide their name, item, quantity, and pickup date to place an order.

## 5. System Architecture

The project follows a tool-based AI agent architecture.

**Workflow:**

Customer Message → LangChain Agent → Groq LLM → Appropriate Tool → Google Sheets (for orders) → Customer Response

The AI agent decides which tool to use depending on the customer's request.

## 6. Implementation

### Step 1: Environment Setup

Install the required Python packages:

```python
!pip install -q langchain langchain-groq gspread
```

Retrieve the Groq API key securely using Google Colab Secrets.

```python
import os
from google.colab import userdata

os.environ["GROQ_API_KEY"] = userdata.get("GROQ_API_KEY")
```

Initialize the Groq language model:

```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.2,
    max_retries=3
)
```

### Step 2: Google Sheets Integration

Google Sheets is used as the database for storing customer orders.

The `gspread` library connects Python with Google Sheets.

```python
import gspread
from google.colab import auth
from google.auth import default

auth.authenticate_user()

creds, _ = default()
gc = gspread.authorize(creds)

sh = gc.create("Sweet Crumbs Orders")
ws = sh.sheet1

ws.append_row([
    "name",
    "item",
    "qty",
    "date",
    "eggless",
    "total"
])
```

### Step 3: Define Bakery Data

The menu and opening hours are stored using Python dictionaries.

```python
MENU = {
    "plum cake": 500,
    "chocolate cake": 650,
    "cupcake": 80
}

HOURS = {
    "monday": "9 am to 8 pm",
    "tuesday": "9 am to 8 pm",
    "wednesday": "9 am to 8 pm",
    "thursday": "9 am to 8 pm",
    "friday": "9 am to 8 pm",
    "saturday": "9 am to 8 pm",
    "sunday": "10 am to 6 pm"
}
```

### Step 4: Create the Order Model

Pydantic is used to validate customer order information.

```python
from typing import Literal
from pydantic import BaseModel, Field

class Order(BaseModel):

    name: str = Field(
        description="Customer's first name"
    )

    item: Literal[
        "plum cake",
        "chocolate cake",
        "cupcake"
    ]

    qty: int = Field(ge=1)

    date: str

    eggless: bool
```

This ensures that:
- Customer name is provided.
- The item belongs to the bakery menu.
- Quantity is at least one.
- Pickup date is provided.
- Eggless preference is recorded.

### Step 5: Create AI Tools

Three tools are created using LangChain's `@tool` decorator.

**1. get_price()**

Retrieves the price of a bakery item and calculates the total based on quantity.

**2. is_open()**

Checks the bakery's opening hours for a particular day.

**3. log_order()**

Validates the order, calculates the total price, and saves the order in Google Sheets.

These tools allow the AI agent to perform actual operations instead of generating answers based only on its language model knowledge.

### Step 6: Create the AI Agent

The `create_agent()` function creates the bakery assistant.

```python
from langchain.agents import create_agent

SYSTEM = """
ROLE: You are the friendly order assistant
for Sweet Crumbs Home Bakery.

FACTS:
Orders need 24 hours' notice.
All cakes have eggless versions.

RULES:
Always use get_price for prices.
Always use is_open for timings.
Never guess prices or timings.
Collect all required order details before saving.
Read the order back with the total after saving.

FORMAT:
Under 60 words.
Friendly English or Telugu matching the customer.
"""

agent = create_agent(
    model=llm,
    tools=[get_price, is_open, log_order],
    system_prompt=SYSTEM
)
```

The system prompt defines the assistant's role, business information, rules, and response format.

### Step 7: Conversation Memory

Conversation history is maintained using a Python list.

```python
history = []

def chat(text: str) -> str:

    global history

    result = agent.invoke({
        "messages": history + [
            {"role": "user", "content": text}
        ]
    })

    history = result["messages"]

    return history[-1].content
```

This allows the assistant to remember previous messages during the conversation.

### Step 8: Test the AI Assistant

```python
print(
    chat(
        "Are you open on Sunday? "
        "How much are 2 chocolate cakes?"
    )
)

print(
    chat(
        "I'm Ravi. Please book 2 eggless "
        "chocolate cakes for 24 Dec."
    )
)
```

The assistant checks opening hours, retrieves prices, collects order information, and saves confirmed orders.

## 7. Google Sheets Output

Every successfully saved order is recorded in Google Sheets.

| name | item | qty | date | eggless | total |
|---|---|---:|---|---|---:|
| Ravi | chocolate cake | 2 | 24 Dec | yes | ₹1300 |

The spreadsheet provides a simple way for the bakery owner to manage customer orders.

## 8. Project Features

- **AI-powered conversations:** Understands natural-language customer messages.
- **Tool calling:** Uses specific Python functions to retrieve information and perform operations.
- **Price calculation:** Automatically calculates order totals.
- **Business-hour checking:** Provides accurate opening timings.
- **Order validation:** Uses Pydantic to validate customer details.
- **Google Sheets integration:** Stores customer orders automatically.
- **Conversation memory:** Maintains previous conversation messages.
- **Bilingual interaction:** Supports English and Telugu responses.

## 9. Learning Outcomes

Through this project, the following concepts were explored:

1. Understanding Large Language Models (LLMs).
2. Integrating Groq API with LangChain.
3. Creating AI agents using `create_agent()`.
4. Understanding LangChain tools and tool calling.
5. Using Pydantic for structured data validation.
6. Creating system prompts for AI assistants.
7. Maintaining conversation history.
8. Integrating Google Sheets with Python.
9. Using API keys securely through Google Colab Secrets.
10. Building a practical AI-powered automation application.

## 10. Future Enhancements

Possible improvements include:

- WhatsApp integration for customer communication.
- Online payment integration.
- Automatic order confirmation messages.
- Customer order tracking.
- Order cancellation and modification.
- A web-based bakery ordering interface.
- Improved conversation memory using persistent storage.

## 11. Conclusion

The Sweet Crumbs AI Order Assistant demonstrates how Large Language Models, LangChain agents, custom Python tools, and Google Sheets can work together to automate bakery operations.

The project transforms a simple chatbot into a functional AI assistant capable of answering customer questions, checking business information, calculating prices, and recording orders.

It provides practical experience in building real-world AI applications using Python and modern LLM technologies.

---

**Project Name:** Sweet Crumbs – AI-Powered Bakery Order Assistant

**Language:** Python

**Framework:** LangChain

**LLM Provider:** Groq

**Database:** Google Sheets

**Environment:** Google Colab
