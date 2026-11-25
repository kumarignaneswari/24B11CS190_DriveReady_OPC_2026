import os
import csv
from pathlib import Path
from dotenv import load_dotenv

# ==================================================
# CELL 1: SETUP
# ==================================================

# Load API key from .env
project_folder = Path(__file__).resolve().parent
load_dotenv(dotenv_path=project_folder / ".env")

# Get API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing! Check your .env file.")

# Import Groq
from langchain_groq import ChatGroq

# Create LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3
)

print("Groq LLM connected successfully!")


# ==================================================
# CELL 2: ASSISTANT - TEMPLATE + MEMORY + CHAIN
# ==================================================

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

SYSTEM = """ROLE: You are the friendly assistant for Sweet Crumbs Home Bakery.

FACTS:
Plum cake Rs 500.
Chocolate cake Rs 650.
Cupcake Rs 80 each.
Orders need 24 hours' notice.
All cakes have eggless versions.

RULES:
Never promise a delivery time or place.
If it isn't in FACTS, say "I'll check with the owner."
Work out totals carefully.

FORMAT:
Under 50 words, friendly, English or Telugu matching the customer."""

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    MessagesPlaceholder("history"),
    ("human", "{question}")
])

# Create chain
chain = prompt | llm | StrOutputParser()

# Conversation history
history = []

# Ask function
def ask(question: str) -> str:

    answer = chain.invoke({
        "history": history,
        "question": question
    })

    # Store user question and AI answer
    history.extend([
        ("human", question),
        ("ai", answer)
    ])

    return answer


# ==================================================
# CELL 3: TESTING THE ASSISTANT
# ==================================================

def run_tests(path="tests.csv"):

    test_path = project_folder / path

    with open(test_path, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    passed = 0

    for row in rows:

        answer = chain.invoke({
            "history": [],
            "question": row["question"]
        })

        ok = row["must_include"].lower() in answer.lower()

        if ok:
            passed += 1

        print(
            "PASS" if ok else "FAIL",
            "|",
            row["question"],
            "->",
            answer[:70]
        )

    if rows:
        print(f"\n{passed}/{len(rows)} passed ({passed / len(rows):.0%})")
    else:
        print("No tests found.")


# ==================================================
# CELL 4: LANGCHAIN AGENT
# ==================================================

from langchain.agents import create_agent

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=SYSTEM
)


# ==================================================
# MAIN PROGRAM
# ==================================================

if __name__ == "__main__":

    print("\n========== SWEET CRUMBS ASSISTANT ==========")

    # Test assistant and memory
    print("\nCustomer: Hi, I'm Ravi. Do you make eggless cakes?")
    print("Assistant:", ask("Hi, I'm Ravi. Do you make eggless cakes?"))

    print("\nCustomer: What's my name?")
    print("Assistant:", ask("What's my name?"))

    print("\nCustomer: What is the price of chocolate cake?")
    print("Assistant:", ask("What is the price of chocolate cake?"))

    print("\nCustomer: How much do 3 cupcakes cost?")
    print("Assistant:", ask("How much do 3 cupcakes cost?"))

    print("\nCustomer: Do you deliver to Hyderabad?")
    print("Assistant:", ask("Do you deliver to Hyderabad?"))

    # Run tests
    print("\n========== RUNNING TESTS ==========")
    run_tests()

    # Run agent
    print("\n========== LANGCHAIN AGENT ==========")

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "Do you make eggless cakes?"
            }
        ]
    })

    print("Agent:", result["messages"][-1].content)