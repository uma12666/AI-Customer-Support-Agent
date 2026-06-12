from tools.refund_status import get_refund_status
from tools.order_cancel import cancel_order
from tools.return_order import request_return
from tools.order_tracker import track_order

from retriever import retrieve_context

from groq import Groq
from dotenv import load_dotenv

import os
import json
import re

# =====================================
# Load Environment Variables
# =====================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MEMORY_FILE = "customer_memory.json"

# =====================================
# Memory Functions
# =====================================

def load_memory():

    if os.path.exists(MEMORY_FILE):

        try:
            with open(MEMORY_FILE, "r") as file:
                return json.load(file)

        except Exception:
            return {}

    return {}


def save_memory(memory):

    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)


customer_memory = load_memory()

# =====================================
# LLM
# =====================================

def ask_llm(prompt):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# =====================================
# Intent Detection
# =====================================

def detect_intent(message):

    message = message.lower()

    if any(
        phrase in message
        for phrase in [
            "track",
            "track order",
            "where is my order",
            "order status"
        ]
    ):
        return "track_order"

    if any(
        phrase in message
        for phrase in [
            "cancel",
            "cancel order"
        ]
    ):
        return "cancel_order"

    if any(
        phrase in message
        for phrase in [
            "return",
            "return item",
            "return product",
            "send back"
        ]
    ):
        return "return_product"

    if any(
        phrase in message
        for phrase in [
            "refund",
            "money back"
        ]
    ):
        return "refund_status"

    if any(
        phrase in message
        for phrase in [
            "order number",
            "order no",
            "my order is",
            "i ordered"
        ]
    ):
        return "provide_information"

    return "general_chat"


# =====================================
# Order ID Extractor
# =====================================

def extract_order_id(message):

    match = re.search(r"\d+", message)

    if match:
        return match.group()

    return None


# =====================================
# Main Function
# =====================================

def process_message(user_input):

    global customer_memory

    intent = detect_intent(user_input)

    # Track Order
    if intent == "track_order":

        order_id = extract_order_id(user_input)

        if not order_id:
            order_id = customer_memory.get("order_id")

        if not order_id:
            return "Please provide your order number."

        order = track_order(order_id)

        if order:

            return (
                f"Order ID: {order['order_id']}\n"
                f"Product: {order['product']}\n"
                f"Status: {order['status']}\n"
                f"Expected Delivery: {order['delivery_date']}"
            )

        return "Order not found."

    # Cancel Order
    if intent == "cancel_order":

        order_id = extract_order_id(user_input)

        if not order_id:
            order_id = customer_memory.get("order_id")

        if not order_id:
            return "Please provide your order number."

        result = cancel_order(order_id)

        return result["message"]

    # Return Product
    if intent == "return_product":

        order_id = extract_order_id(user_input)

        if not order_id:
            order_id = customer_memory.get("order_id")

        if not order_id:
            return "Please provide your order number."

        result = request_return(order_id)

        return result["message"]

    # Refund Status
    if intent == "refund_status":

        order_id = extract_order_id(user_input)

        if not order_id:
            order_id = customer_memory.get("order_id")

        if not order_id:
            return "Please provide your order number."

        result = get_refund_status(order_id)

        if result["success"]:
            return f"Refund Status: {result['refund_status']}"

        return result["message"]

    # Save Order Number
    if intent == "provide_information":

        order_id = extract_order_id(user_input)

        if order_id:

            customer_memory["order_id"] = order_id

            save_memory(customer_memory)

            return (
                f"Thank you. I have saved your order number "
                f"({order_id}). How can I help you with this order?"
            )

        return "Thank you for the information."

    # RAG + LLM
    retrieved_context = retrieve_context(user_input)

    prompt = f"""
You are a professional AI Customer Support Agent.

Knowledge Base:
{retrieved_context}

Customer Question:
{user_input}

Answer professionally.
"""

    try:

        response = ask_llm(prompt)

        return response

    except Exception as e:

        return f"Error: {str(e)}"