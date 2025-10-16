import tkinter as tk
import pyttsx3
from difflib import SequenceMatcher

# -------------------------------
# Load Q&A document
# -------------------------------
def load_document(filename):
    qa_pairs = {}
    with open(filename, "r") as file:
        for line in file:
            if ":" in line:
                question, answer = line.strip().split(":", 1)
                qa_pairs[question.strip().lower()] = answer.strip()
    return qa_pairs

# Path to Q&A text file
document_file = "E:\\three\\train.txt"  # <-- Make sure this file exists
qa_document = load_document(document_file)

# -------------------------------
# Setup text-to-speech
# -------------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 140)
engine.setProperty('volume', 1.0)
engine.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')

def speak_response(text):
    engine.say(text)
    engine.runAndWait()

# -------------------------------
# Find most similar question
# -------------------------------
def similar_question(user_question):
    max_similarity = 0
    most_similar_question = None
    for question in qa_document:
        similarity = SequenceMatcher(None, user_question, question).ratio()
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_question = question

    # Return only if similarity is good enough (e.g., >= 0.6)
    if max_similarity >= 0.6:
        return most_similar_question
    else:
        return None


def respond_to_question(user_question, label):
    user_question = user_question.strip().lower()
    if not user_question:
        label.config(text="Please enter a question.")
        return

    if user_question in qa_document:
        response = qa_document[user_question]
    else:
        similar_q = similar_question(user_question)
        if similar_q:
            response = qa_document[similar_q]
        else:
            response = "I'm sorry, I don't have an answer to that question."

    label.config(text=f"Bot: {response}")
    speak_response(response)


# -------------------------------
# Respond to typed question
# -------------------------------
def respond_to_question(user_question, label):
    user_question = user_question.strip().lower()
    if not user_question:
        label.config(text="Please enter a question.")
        return

    if user_question in qa_document:
        response = qa_document[user_question]
    else:
        similar_q = similar_question(user_question)
        if similar_q:
            response = qa_document[similar_q]
        else:
            response = "I'm sorry, I don't have an answer to that question."

    label.config(text=f"Bot: {response}")
    speak_response(response)

# -------------------------------
# Build GUI
# -------------------------------
def main():
    root = tk.Tk()
    root.title("Avatar Chatbot GUI")

    # Fullscreen setup
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")

    # --- Components ---
    # Placeholder for video (for visual balance)
    video_frame = tk.Frame(root, bg="black", width=800, height=400)
    video_frame.pack(pady=30)

    status_label = tk.Label(root, text="Bot: Ready to chat!", font=("Arial", 18))
    status_label.pack(pady=10)

    question_entry = tk.Entry(root, width=60, font=("Arial", 22))
    question_entry.pack(pady=15)

    # --- Button hover effects ---
    def button_hover(event):
        event.widget.config(bg="#6495ED")

    def button_leave(event):
        event.widget.config(bg="SystemButtonFace")

    # --- Button to ask question ---
    def on_ask_click():
        user_question = question_entry.get()
        respond_to_question(user_question, status_label)
        question_entry.delete(0, tk.END)

    ask_button = tk.Button(root, text="Ask Question", command=on_ask_click, width=20, height=2, font=("Arial", 15))
    ask_button.pack(pady=15)
    ask_button.bind("<Enter>", button_hover)
    ask_button.bind("<Leave>", button_leave)

    root.mainloop()

if __name__ == "__main__":
    main()
