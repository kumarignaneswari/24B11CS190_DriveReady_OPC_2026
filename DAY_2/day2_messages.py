from langchain_groq import ChatGroq

# Create LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3
)

# Send messages
reply = llm.invoke([
    ("system", "You are Sweet Crumbs' assistant. Answer in under 30 words."),
    ("human", "Do you make eggless cakes?")
])

# Print response
print(reply.content)