
from tools.refund_status import get_refund_status
from tools.order_cancel import cancel_order
from tools.return_order import request_return
from tools.order_tracker import track_order
import re
from retriever import retrieve_context
import warnings
warnings.filterwarnings("ignore")

from groq import Groq
from dotenv import load_dotenv
import os
import json
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
# Load Environment Variables
# =====================================
load_dotenv()

# =====================================
# Configure Gemini
# =====================================
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =====================================
# Memory File
# =====================================
MEMORY_FILE = "customer_memory.json"

# =====================================
# Load Memory
# =====================================
def load_memory():

    if os.path.exists(MEMORY_FILE):

        try:
            with open(MEMORY_FILE, "r") as file:
                return json.load(file)

        except Exception:
            return {}

    return {}

# =====================================
# Save Memory
# =====================================
def save_memory(memory):

    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

# =====================================
# Fact Extractor Agent
# =====================================
def extract_facts(user_message):

    extraction_prompt = f"""
You are an information extraction agent.

Extract useful customer information from the message.

Possible examples:
- name
- city
- profession
- education
- purchase
- likes
- interests
- favorite_color
- company
- hobby

Return ONLY valid JSON.

Examples:

Message:
My name is Padmanethra and I live in Chennai.

Output:
{{
    "name": "Padmanethra",
    "city": "Chennai"
}}

Message:
I am studying CSE and I bought a Dell laptop.

Output:
{{
    "education": "CSE",
    "purchase": "Dell laptop"
}}

Message:
{user_message}
"""

    try:

        extracted_text = ask_llm(
    extraction_prompt
).strip()

        extracted_text = extracted_text.replace(
            "```json", ""
        )

        extracted_text = extracted_text.replace(
            "```", ""
        )

        extracted_text = extracted_text.strip()

        facts = json.loads(extracted_text)

        return facts

    except Exception:

        return {}

# =====================================
# Load Persistent Customer Memory
# =====================================
customer_memory = load_memory()

# =====================================
# Conversation Memory
# =====================================
chat_history = []

print("===================================")
print(" AI Customer Support Agent")
print("===================================")
print("Commands:")
print("show memory")
print("clear memory")
print("exit")
print()

# =====================================
# Temporary Workflow Memory
# =====================================
pending_reschedule = {}

# =====================================
# Intent Detection
# =====================================
def detect_intent(message):

    message = message.lower()

    # Track Order
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

    # Cancel Order
    if any(
        phrase in message
        for phrase in [
            "cancel",
            "cancel order"
        ]
    ):
        return "cancel_order"

    # Return Product
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

    # Refund
    if any(
        phrase in message
        for phrase in [
            "refund",
            "money back"
        ]
    ):
        return "refund_status"

    # Delivery
    if any(
        phrase in message
        for phrase in [
            "change delivery",
            "reschedule delivery",
            "not available",
            "not present"
        ]
    ):
        return "reschedule_delivery"

    # Order Information
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
# Main Chat Loop
# =====================================
while True:

    user_input = input("Customer: ")
    intent = detect_intent(user_input)
    if intent == "track_order":

            order_id = extract_order_id(user_input)

            if not order_id:

                order_id = customer_memory.get(
                    "order_id"
                )

            if not order_id:

                print(
                    "\nAgent: Please provide your order number.\n"
                )

                continue

            order = track_order(order_id)

            if order:

                print(
                    f"""
        Agent:
        Order ID: {order['order_id']}
        Product: {order['product']}
        Status: {order['status']}
        Expected Delivery: {order['delivery_date']}
        """
                )

            else:

                print(
                    "\nAgent: Order not found.\n"
                )

            continue
    if intent == "cancel_order":

            order_id = extract_order_id(user_input)

            if not order_id:
                order_id = customer_memory.get(
                    "order_id"
                )

            if not order_id:

                print(
                    "\nAgent: Please provide your order number.\n"
                )

                continue

            result = cancel_order(order_id)

            print(
                f"\nAgent: {result['message']}\n"
            )

            continue
    if intent == "return_product":

            order_id = extract_order_id(user_input)

            if not order_id:
                order_id = customer_memory.get("order_id")

            if not order_id:

                print(
                    "\nAgent: Please provide your order number.\n"
                )

                continue

            result = request_return(order_id)

            print(
                f"\nAgent: {result['message']}\n"
            )

            continue
    if intent == "refund_status":

            order_id = extract_order_id(user_input)

            if not order_id:

                order_id = customer_memory.get(
                    "order_id"
                )

            if not order_id:

                print(
                    "\nAgent: Please provide your order number.\n"
                )

                continue

            result = get_refund_status(order_id)

            if result["success"]:

                print(
                    f"\nAgent: Refund Status: {result['refund_status']}\n"
                )

            else:

                print(
                    f"\nAgent: {result['message']}\n"
                )

            continue
        
    
    



    # -----------------------------
    # Exit
    # -----------------------------
    if user_input.lower() == "exit":

        print(
            "\nAgent: Thank you for contacting support. Goodbye!"
        )

        break

    # -----------------------------
    # Show Memory
    # -----------------------------
    if user_input.lower() == "show memory":

        print("\nStored Memory:")
        print(
            json.dumps(
                customer_memory,
                indent=4
            )
        )
        print()

        continue

    # -----------------------------
    # Clear Memory
    # -----------------------------
    if user_input.lower() == "clear memory":

        customer_memory = {}

        save_memory(customer_memory)

        print("\nMemory Cleared.\n")

        continue

    if intent == "provide_information":

        order_id = extract_order_id(user_input)

        if order_id:

            customer_memory["order_id"] = order_id

            save_memory(customer_memory)

            print(
                f"\nAgent: Thank you. I have saved your order number ({order_id}). How can I help you with this order?\n"
            )

        else:

            print(
                "\nAgent: Thank you for the information.\n"
            )

        continue

    retrieved_context = retrieve_context(user_input)

   
    # -----------------------------
    # Extract Facts
    # -----------------------------
    if intent == "general_chat":

        new_facts = extract_facts(user_input)

        if new_facts:

            customer_memory.update(new_facts)

            save_memory(customer_memory)
    # -----------------------------
    # Debug Memory Display
    # -----------------------------
    # print("\nCurrent Memory:")
    # print(
       # json.dumps(
           #customer_memory,
            #indent=4
        
    

    # -----------------------------
    # Store Conversation
    # -----------------------------
    chat_history.append(
        f"Customer: {user_input}"
    )

    conversation = "\n".join(chat_history)

    # -----------------------------
    # Build Memory Context
    # -----------------------------
    memory_context = ""

    for key, value in customer_memory.items():

        memory_context += (
            f"{key}: {value}\n"
        )


    # -----------------------------
    # Main Agent Prompt
    # -----------------------------
    prompt = f"""
    You are a professional AI Customer Support Agent.

    Customer Profile:
    {memory_context}

    Knowledge Base:
    {retrieved_context}

    Rules:

    1. Use the Knowledge Base as the primary source of truth.
    2. Use customer profile information ONLY when directly relevant to the customer's question.
    3. Do NOT mention customer preferences, interests, or personal details unless the customer asks about them.
    4. Never invent policies, order details, refund details, shipping details, or customer information.
    5. If information is unavailable in the Knowledge Base or customer profile, clearly state that you do not have that information.
    6. Be polite, professional, and concise.
    7. Answer the customer's question directly before providing additional information.
    8. Do not make assumptions about customer purchases or orders.
    9. If the customer asks about an order and no order information exists, ask for the order number.
    10. If the customer asks about refunds, returns, shipping, cancellations, or payment methods, prioritize information from the Knowledge Base.
    11. If the customer's question is unrelated to customer support, answer naturally without forcing references to the customer profile.
    12. Maintain conversational context from previous messages.

    Conversation History:
    {conversation}

    Current Customer Message:
    {user_input}

    Provide a helpful customer support response.
    """

    try:

        agent_reply = ask_llm(prompt)

        chat_history.append(
                f"Agent: {agent_reply}"
            )

        print(
                f"\nAgent: {agent_reply}\n"
            )
        
    except Exception as e:

            print(
                f"\nError: {e}\n"
            )