 #Day 1: raw API call
import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1")
r = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user",
               "content": "Eggless available?"}])
print(r.choices[0].message.content)
# Day 3: the same call with LangChain
from langchain_groq import ChatGroq
llm = ChatGroq(model="openai/gpt-oss-20b")


reply = llm.invoke("Eggless available?")
print(reply.content)