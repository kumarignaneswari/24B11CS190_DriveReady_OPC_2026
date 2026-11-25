# Sweet Crumbs Home Bakery Assistant

A conversational AI assistant built with Python, LangChain, and Groq (`openai/gpt-oss-20b`) for **Sweet Crumbs Home Bakery**. It answers customer inquiries regarding menu pricing, eggless options, and order policies while maintaining conversation memory and adhering to strict business rules.

## Features

- **Rule-Bound System Prompt:** Enforces strict guidelines (under 50 words, friendly tone, English/Telugu language matching, accurate price calculations, and escalating unknown queries to the owner).
- **Conversation Memory:** Retains chat history across multiple turns using `MessagesPlaceholder` to provide context-aware responses (e.g., remembering a customer's name).
- **Automated Evaluation:** Includes a test suite (`tests.csv`) that validates model responses against expected keywords and calculates a pass rate.
- **LangChain Agent Support:** Demonstrates initializing a LangChain agent with the same model and system prompt.

## Project Structure

```text
├── main.py          # Core assistant logic, memory chain, test runner, and agent setup
├── tests.csv        # Test cases and expected keywords for automated evaluation
├── .env             # Environment variables (contains GROQ_API_KEY - excluded from Git)
├── .gitignore       # Specifies files/folders to ignore in Git (.env, __pycache__/)
└── README.md        # Project documentation
```

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd YOUR-REPO-NAME
   ```

2. **Install dependencies:**
   ```bash
   pip install python-dotenv langchain langchain-groq langchain-core
   ```

3. **Configure environment variables:**
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY="your_groq_api_key_here"
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## Implementation Details

- **Setup:** Uses `python-dotenv` to load the `GROQ_API_KEY` and initializes `ChatGroq` with `temperature=0.3` for consistent, reliable answers.
- **Prompt & Chain:** Combines a structured `ChatPromptTemplate` with `StrOutputParser` using LangChain Expression Language (`prompt | llm | StrOutputParser()`).
- **Testing:** Reads `tests.csv` via Python's built-in `csv` module, runs stateless queries against the chain, and checks if the required substring (`must_include`) appears in the output.

