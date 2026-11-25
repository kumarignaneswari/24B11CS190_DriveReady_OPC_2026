from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Create LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3
)

# Create Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the assistant for {business}. Answer in under 30 words."),
    ("human", "{question}")
])

# Fill the placeholders
messages = prompt.invoke({
    "business": "Sweet Crumbs Home Bakery",
    "question": "Do you make eggless cakes?"
})

# Send messages to LLM
reply = llm.invoke(messages)

# Print response
print(reply.content)