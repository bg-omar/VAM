# vam_agent.py
# Offline VAM Assistant with GUI + Serial Microcontroller Bridge

# 🧠 Install: pip install langchain faiss-cpu pypdf sentence-transformers pyserial
# 🧠 Download Ollama: https://ollama.com/download and run: ollama run llama2

import tkinter as tk
from tkinter import scrolledtext
import serial
import threading
import time

from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# === Load PDF Knowledge Base ===
def load_knowledge_base():
    pdfs = [
        "GR_in_3d.pdf",
        "00_VAM.pdf",
        "000_Æther.pdf"
    ]
    docs = []
    for pdf in pdfs:
        loader = PyPDFLoader(pdf)
        docs.extend(loader.load())
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.from_documents(docs, embedding)

vectorstore = load_knowledge_base()
llm = Ollama(model="llama2")
chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

# === VAM Instruction ===
instruction = """
You are the AI assistant of the Vortex Æther Model (VAM) creator.
Your priority knowledge base:
1. GR_in_3d.pdf
2. 00_VAM.pdf
3. 000_Æther.pdf

Respond with:
- VAM-first physics reasoning
- Scientific correctness (no contradictions to experiments)
- Mathematical precision (equation form and numerical validation)
- Conceptual innovation
- Historical accuracy
- Clear, rigorous explanations
- Always end with a relevant suggestion, question, or derivation
- Include BibTeX citations for any derivations
"""

# === Serial Bridge Thread ===
def serial_bridge_loop():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)
        print(f"🔌 Listening on {SERIAL_PORT} @ {BAUD_RATE} baud...")
        while True:
            if ser.in_waiting:
                raw = ser.readline().decode('utf-8').strip()
                print(f"🛠️ Microcontroller asks: {raw}")
                query = instruction + "\n" + raw
                response = chain.run(query)
                print(f"🧠 GPT responds: {response[:80]}...")
                reply = response[:300].replace('\n', ' ')
                ser.write((reply + "\n").encode('utf-8'))
    except Exception as e:
        print(f"⚠️ Serial error: {e}")

# === GUI Logic ===
def query_gpt():
    user_input = user_entry.get("1.0", tk.END).strip()
    if user_input:
        output_text.insert(tk.END, f"\n🔹 You: {user_input}\n")
        response = chain.run(instruction + "\n" + user_input)
        output_text.insert(tk.END, f"🧠 VAM-GPT: {response}\n\n")
        user_entry.delete("1.0", tk.END)

# === GUI Setup ===
root = tk.Tk()
root.title("🧠 VAM Assistant - Offline GUI")

user_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=6, font=("Consolas", 11))
user_entry.pack(padx=10, pady=10)

ask_button = tk.Button(root, text="Ask VAM-GPT", command=query_gpt, font=("Arial", 12, "bold"))
ask_button.pack()

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=25, font=("Consolas", 10))
output_text.pack(padx=10, pady=10)
output_text.insert(tk.END, "🌀 Welcome to the Offline VAM Assistant\nAsk a question based on Æther physics, vorticity, gravity, or time dilation...\n")

# === Serial Config (Adjust as needed) ===
SERIAL_PORT = "COM4"  # <=== Change to your USB port (e.g., COM3 or /dev/ttyUSB0)
BAUD_RATE = 115200

# Start serial bridge in background
threading.Thread(target=serial_bridge_loop, daemon=True).start()

# Launch GUI loop
print("🔬 VAM Assistant Ready (GUI + Serial Bridge).")
root.mainloop()
