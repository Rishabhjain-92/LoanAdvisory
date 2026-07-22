import os

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)

from langchain_community.vectorstores import FAISS


# Load environment variables
load_dotenv()


def ask_question(question):

    # Create the embedding model

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("AQ.Ab8RN6KtFA4H_4VP6Zw18i1yXdo-Yk4psb3Bqw7jqp8HBfptrA")
    )


    # Load the existing FAISS vector database

    vector_db = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )


    # Search for the three most relevant sections

    documents = vector_db.similarity_search(
        question,
        k=3
    )


    # Combine relevant document text

    context = "\n\n".join(
        [
            document.page_content
            for document in documents
        ]
    )


    # Create Gemini model

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )


    # Create the prompt

    prompt = f"""
You are an AI Loan Advisory Assistant.

Answer the user's question using only the loan-policy
information provided in the context below.

Instructions:

1. Do not use outside knowledge.

2. Give a clear and concise answer.

3. Use bullet points when they improve readability.

4. Do not invent loan amounts, eligibility conditions,
interest rates, fees, or other information.

5. If the answer is not available in the context, say:

"I couldn't find this information in the provided loan policy."


LOAN POLICY CONTEXT:

{context}


USER QUESTION:

{question}
"""


    # Generate the answer

    response = llm.invoke(prompt)


    # Store the source text

    sources = [
        document.page_content
        for document in documents
    ]

    # Return both answer and sources

    return response.content, sources