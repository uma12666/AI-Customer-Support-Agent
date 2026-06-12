 AI Customer Support Agent

Overview

AI Customer Support Agent is an intelligent support system designed to automate customer service operations using Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and a knowledge base. The system provides accurate responses to customer queries while supporting real-world order management operations.

## Features

* Order Tracking
* Order Cancellation
* Product Return Management
* Refund Status Tracking
* Delivery Rescheduling
* Customer Memory Management
* Knowledge Base Search using ChromaDB
* Intent Classification
* AI-Powered Customer Support Chat Interface

## Technologies Used

* Python
* Groq LLM (Llama 3.3)
* ChromaDB
* Retrieval-Augmented Generation (RAG)
* SQLite
* Streamlit
* Git & GitHub

## Project Architecture

1. Customer sends a query.
2. Intent Classification identifies the customer's request.
3. Relevant information is retrieved from ChromaDB Knowledge Base.
4. Business operations are performed through SQLite database.
5. Groq LLM generates a contextual response.
6. Streamlit provides an interactive chat interface.

## Supported Operations

* Track Order Status
* Cancel Orders Before Shipment
* Request Product Returns
* Check Refund Status
* Reschedule Deliveries
* Retrieve Company Policies

## Installation

```bash
pip install -r requirements.txt
```

## Run Application

```bash
streamlit run streamlit_app.py
```

## Future Enhancements

* Multi-user Authentication
* Voice-Based Customer Support
* Email Notifications
* Real-Time Order Updates
* Dashboard Analytics

## Author

Padmanethra MV,
B.E. CSE,
KCG College of Technology
