from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Step 1: Create LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3
)

# Step 2: Create Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the assistant for {business}. Answer in under 30 words."),
    ("human", "{question}")
])

# Step 3: Create Chain
chain = prompt | llm | StrOutputParser()

# Step 4: Execute Chain
answer = chain.invoke({
    "business": "Sweet Crumbs Home Bakery",
    "question": "Do you make eggless cakes?"
})

# Step 5: Print Answer
print(answer)