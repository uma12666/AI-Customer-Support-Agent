import chromadb

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    "support_docs"
)

def retrieve_context(
    query,
    top_k=1
):

    try:

        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )

        docs = results["documents"][0]

        if not docs:
            return "No relevant information found."

        return docs[0]

    except Exception as e:

        print(
            f"Retriever Error: {e}"
        )

        return "No relevant information found."


if __name__ == "__main__":

    question = "What is your refund policy?"

    context = retrieve_context(
        question
    )

    print("\nRetrieved Context:\n")
    print(context)