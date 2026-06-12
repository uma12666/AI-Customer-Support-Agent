import os
import chromadb

client = chromadb.PersistentClient(
    path="chroma_db"
)

try:
    client.delete_collection("support_docs")
except:
    pass

collection = client.get_or_create_collection(
    name="support_docs"
)

folder = "knowledge_base"

doc_id = 0

for file in os.listdir(folder):

    if file.endswith(".txt"):

        filepath = os.path.join(folder, file)

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        chunks = text.split("\n\n")

        for chunk in chunks:

            chunk = chunk.strip()

            if len(chunk) < 20:
                continue

            collection.add(
                documents=[chunk],
                ids=[str(doc_id)],
                metadatas=[
                    {
                        "source": file
                    }
                ]
            )

            doc_id += 1

print(f"Stored {doc_id} chunks successfully.")