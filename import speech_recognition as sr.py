import speech_recognition as sr
import pyttsx3
import cv2
import threading
from difflib import SequenceMatcher
import time
import tkinter as tk
avatar_video_path = "E:\\three\\chatbot.mp4"
recognizer = sr.Recognizer()
engine = pyttsx3.init()
response_complete_event = threading.Event()
countdown_completed = False  
def load_document(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    qa_pairs = {}
    for line in lines:
        question, answer = line.strip().split(":")
        qa_pairs[question.strip().lower()] = answer.strip()
    return qa_pairs
document_file = "E:\\three\\train.txt"
qa_document = load_document(document_file)
def play_avatar_video():
    cap = cv2.VideoCapture(avatar_video_path)
    cv2.namedWindow('Avatar Video', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Avatar Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while cap.isOpened() and not response_complete_event.is_set():
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  
            continue
        cv2.imshow('Avatar Video', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
def recognize_speech(label):
    label.config(text="Listening...")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        label.config(text="Recognizing...")
        user_input = recognizer.recognize_google(audio).lower()
        label.config(text="User: " + user_input)
        return user_input
    except sr.UnknownValueError:
        label.config(text="Sorry, I could not understand that.")
        return ""
    except sr.RequestError as e:
        label.config(text="Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""
def similar_question(user_question):
    max_similarity = 0
    most_similar_question = None
    for question in qa_document:
        similarity = SequenceMatcher(None, user_question, question).ratio()
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_question = question
    return most_similar_question
def respond_to_question(question):
    if question in qa_document:
        response_text = qa_document[question]
        speak_response(response_text)
    else:
        similar_question_text = similar_question(question)
        if similar_question_text:
            response_text = qa_document[similar_question_text]
            speak_response(response_text)
        else:
            speak_response("I'm sorry, I don't have an answer to that question.")
    response_complete_event.set()
def speak_response(response_text):
     engine.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
  
     engine.setProperty('rate', 120) 
     engine.setProperty('volume', 1)   
     engine.setProperty('pitch', 0) 
     engine.say(response_text)
     engine.runAndWait()
def main():
    root = tk.Tk()
    root.title("Avatar Video")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.geometry("800x600")
    root.attributes("-fullscreen", True)
    video_frame = tk.Frame(root)
    video_frame.pack()
    status_label = tk.Label(root, text="")
    status_label.pack()
    question_entry = tk.Entry(root, width=50, font=("Arial", 100))
    question_entry.pack()
    countdown_frame = tk.Frame(root)
    countdown_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  
    countdown_label = tk.Label(countdown_frame, text="D'festa", font=("Arial", 150))
    countdown_label.pack()
    def start_video_thread():
        video_thread = threading.Thread(target=play_avatar_video)
        video_thread.start()
    def stop_video_thread():
        response_complete_event.set()
    def ask_question():
        global countdown_completed  
        if not countdown_completed: 
            countdown_label.config(text="")
            for i in range(10, 0, -1):
                countdown_label.config(text=str(i))
                root.update()
                time.sleep(1)
            countdown_label.config(text="")
            countdown_completed = True  
        user_question = question_entry.get()
        if user_question:
            response_complete_event.clear()
            start_video_thread()
            retry_count = 3
            while retry_count > 0:
                try:
                    respond_to_question(user_question)
                    break
                except Exception as e:
                    print("Error occurred:", str(e))
                    retry_count -= 1
                    time.sleep(1)
            else:
                print("Failed to get response after multiple attempts.")
                countdown_completed = False 

    def ask_question_speech():
        print("Button 'Ask Question with Speech' clicked")
        user_question = recognize_speech(status_label)
        if user_question:
            response_complete_event.clear()
            start_video_thread()
            retry_count = 3
            while retry_count > 0:
                try:
                    respond_to_question(user_question)
                    break
                except Exception as e:
                    print("Error occurred:", str(e))
                    retry_count -= 1
                    time.sleep(1)
            else:
                print("Failed to get response after multiple attempts.")
                countdown_completed = False  
    def button_hover(event):
        event.widget.config(bg="#6495ED")  
    def button_leave(event):
        event.widget.config(bg="SystemButtonFace")  
    ask_button_speech = tk.Button(root, text="Ask Question with Speech", command=ask_question_speech, width=22, height=2, font=("Arial", 15))  
    ask_button_speech.pack(side=tk.BOTTOM,pady=10)  
    ask_button_speech.bind("<Enter>", button_hover)  
    ask_button_speech.bind("<Leave>", button_leave)  
    ask_button = tk.Button(root, text="Ask Question", command=ask_question, width=20, height=2, font=("Arial", 15)) 
    ask_button.pack(side=tk.BOTTOM,pady=5)  
    ask_button.bind("<Enter>", button_hover) 
    ask_button.bind("<Leave>", button_leave)
    root.mainloop()
if __name__ == "_main_":
    main()