# PDF Question-Answering System Using RAG

## 1. Project Description

The PDF Question-Answering System is designed to answer user questions based on the information available in an uploaded PDF document.

Instead of manually searching through the entire PDF, users can ask questions in natural language. The system retrieves relevant information from the PDF and uses a Large Language Model (LLM) to generate answers.

This project uses **Retrieval-Augmented Generation (RAG)** to provide answers based on the document's content.

## 2. Objective

The main objectives of this project are:

- Load and extract text from PDF documents.
- Divide extracted text into smaller chunks.
- Convert text chunks into numerical embeddings.
- Retrieve relevant PDF content based on user questions.
- Generate answers using an LLM.
- Avoid generating answers that are not supported by the PDF.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Google Colab | Development environment |
| Sentence Transformers | Generating text embeddings |
| all-MiniLM-L6-v2 | Embedding model |
| Vector Similarity Search | Retrieving relevant PDF content |
| Groq LLM | Generating answers |
| PDF Processing Library | Extracting text from PDFs |

## 4. Implementation

The project follows these steps:

### Step 1: PDF Loading

The PDF document is uploaded and its text is extracted using a PDF processing library.

### Step 2: Text Chunking

The extracted text is divided into smaller chunks.

Chunking makes it easier to search for relevant information without processing the entire document every time.

### Step 3: Generating Embeddings

The Sentence Transformer model `all-MiniLM-L6-v2` converts text chunks into numerical vectors called embeddings.

These embeddings represent the semantic meaning of the text.

### Step 4: Question Embedding

When a user enters a question, the same embedding model converts the question into a numerical vector.

For example:

```python
question = "Who is Arjun?"

question_vector = model.encode(
    [question],
    convert_to_numpy=True
)

print(question_vector.shape)
```

Output:

```text
(1, 384)
```

This means one question has been converted into a vector containing 384 numerical values.

### Step 5: Context Retrieval

The question embedding is compared with the PDF chunk embeddings.

The system retrieves the most relevant chunks using similarity search.

### Step 6: Answer Generation

The retrieved PDF content is passed to the LLM along with the user's question.

The LLM generates an answer using the retrieved context.

If the answer cannot be found in the provided context, the system responds:

```text
The answer is not available in the PDF.
```

### Step 7: Interactive Question-Answering Loop

The user can continuously ask questions until they enter `exit`.

```python
while True:
    question = input(
        "\nAsk a question (or 'exit'): "
    ).strip()

    if question.lower() == "exit":
        print("Session ended.")
        break

    if not question:
        continue

    answer = ask_pdf(question)

    print("\nBest Matching PDF Content:")
    print(answer)
```

## 5. Example Questions

The system is tested using questions related to the PDF story:

1. Who is Arjun?
2. Why did a stranger tell thanks to Arjun?
3. Why did Arjun keep a lantern outside?
4. Who placed the lantern outside?

The expected behaviour is to retrieve the relevant PDF information and generate accurate answers.

## 6. Challenges Faced

During implementation, the following issues were encountered:

### NameError: name 'model' is not defined

**Reason:** The embedding model was not initialized before calling the retrieval function.

**Solution:**

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
```

### Embedding Output

The embedding test returned:

```text
(1, 384)
```

This confirmed that the question embedding was generated successfully.

### Answers Not Available in the PDF

The system repeatedly returned:

```text
The answer is not available in the PDF.
```

**Possible reasons:**

- PDF text extraction issues.
- Incorrect text chunking.
- Embedding model mismatch.
- Incorrect similarity search.
- Prompt or context-related issues.

Further debugging is required to ensure that the correct PDF chunks are retrieved.

## 7. Expected Output

The expected output is a question-answering system that:

- Understands natural-language questions.
- Searches the uploaded PDF.
- Retrieves relevant information.
- Generates answers based on PDF content.
- Avoids unsupported answers.

## 8. Conclusion

This project demonstrates how Retrieval-Augmented Generation (RAG) can be used to build a PDF-based question-answering system.

It combines document processing, text embeddings, vector similarity search, and Large Language Models to provide an interactive way of retrieving information from PDF documents.

The project also helps understand the practical implementation of embeddings, semantic search, context retrieval, and LLM-based answer generation.
