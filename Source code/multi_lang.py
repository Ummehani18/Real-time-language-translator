import tkinter as tk
from tkinter import ttk
from googletrans import Translator
import speech_recognition as sr
import pyttsx3
import threading

# Global variable to control listening
is_listening = False

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to translate text to multiple languages and speak the translations
def translate_text():
    translator = Translator()
    input_text = text_input.get("1.0", tk.END).strip()  # Get text from input field
    src_lang = source_lang.get()  # Source language

    if input_text:
        try:
            # Translate to each target language and speak the translation
            for lang, text_widget in translations.items():
                translation = translator.translate(input_text, src=src_lang, dest=lang)
                text_widget.config(state=tk.NORMAL)  # Enable editing
                text_widget.delete("1.0", tk.END)  # Clear previous text
                text_widget.insert(tk.END, translation.text)  # Insert translated text
                text_widget.config(state=tk.DISABLED)  # Disable editing

                # Speak the translated text in the respective language
                if lang == 'en':
                    engine.setProperty('voice', 'english')  # Set English voice
                elif lang == 'hi':
                    engine.setProperty('voice', 'hindi')  # Set Hindi voice
                elif lang == 'te':
                    engine.setProperty('voice', 'telegu')  # Set Telugu voice
                engine.say(translation.text)
                engine.runAndWait()

            status_label.config(text="Translation Complete", fg="green")
        except Exception as e:
            status_label.config(text=f"Translation Error: {e}", fg="red")

# Function to capture voice input
def listen_input():
    global is_listening

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        status_label.config(text="Listening... Speak now!", fg="green")
        
        while is_listening:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                input_text = recognizer.recognize_google(audio, language=source_lang.get())
                text_input.delete("1.0", tk.END)
                text_input.insert(tk.END, input_text)
                translate_text()  # Automatically translate after recognition

            except sr.UnknownValueError:
                status_label.config(text="Couldn't understand the audio. Try again.", fg="orange")
            except sr.RequestError as e:
                status_label.config(text=f"Speech Recognition Error: {e}", fg="red")
            except Exception as e:
                status_label.config(text=f"Error: {e}", fg="red")

# Start listening in a new thread
def start_listening():
    global is_listening
    if not is_listening:
        is_listening = True
        status_label.config(text="Starting to listen...", fg="blue")
        threading.Thread(target=listen_input, daemon=True).start()

# Stop listening
def stop_listening():
    global is_listening
    if is_listening:
        is_listening = False
        status_label.config(text="Stopped Listening.", fg="blue")

# Create the main window
root = tk.Tk()
root.title("Real-Time Language Translator with Voice Input")
root.geometry("900x500")
root.config(bg="#ffd8b2")

# Title Label
title_label = tk.Label(
    root, text="Multi-Language Translator", font=("Helvetica", 18, "bold"), bg="#FFAE42", fg="#333"
)
title_label.pack(pady=10, fill=tk.X)

# Main Frame for Horizontal Layout
main_frame = tk.Frame(root, bg="#ffd8b2")
main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Left Frame for Input and Translation Controls
left_frame = tk.Frame(main_frame, bg="#ffd8b2")
left_frame.grid(row=0, column=0, padx=10, pady=10)

# Input Text Area
text_input = tk.Text(left_frame, height=8, width=30, font=("Arial", 12), bg="#fff8dc", fg="#000")
text_input.pack(pady=5)

# Language Selection
lang_frame = tk.Frame(left_frame, bg="#ffd8b2")
lang_frame.pack(pady=5)

source_lang_label = tk.Label(lang_frame, text="From:", font=("Arial", 12), bg="#f0f0f5")
source_lang_label.grid(row=0, column=0, padx=5)
source_lang = ttk.Combobox(lang_frame, values=["English"], width=5)
source_lang.set("English")
source_lang.grid(row=0, column=1, padx=5)

# Button Frame
button_frame = tk.Frame(left_frame, bg="#ffd8b2")
button_frame.pack(pady=5)

translate_button = tk.Button(
    button_frame, text="Translate", command=translate_text, bg="#87ceeb", font=("Arial", 12)
)
translate_button.grid(row=0, column=0, padx=5)

start_button = tk.Button(
    button_frame, text="Start Listening", command=start_listening, bg="#90ee90", font=("Arial", 12)
)
start_button.grid(row=0, column=1, padx=5)

stop_button = tk.Button(
    button_frame, text="Stop Listening", command=stop_listening, bg="#ff7f7f", font=("Arial", 12)
)
stop_button.grid(row=0, column=2, padx=5)

# Right Frame for Multiple Output Text Areas
right_frame = tk.Frame(main_frame, bg="#ffd8b2")
right_frame.grid(row=0, column=1, padx=10, pady=10)

# Translation Output Areas for Different Languages
languages = {"kn": "Kannada", "hi": "Hindi", "te": "Telugu"}
translations = {}

for i, (lang, name) in enumerate(languages.items()):
    lang_label = tk.Label(right_frame, text=f"Translation ({name}):", font=("Arial", 12), bg="#ffd8b2")
    lang_label.grid(row=i, column=0, sticky="w")
    translations[lang] = tk.Text(right_frame, height=5, width=30, font=("Arial", 12), bg="#e6e6fa", fg="#000", state=tk.DISABLED)
    translations[lang].grid(row=i, column=1, padx=5, pady=5)

# Status Label
status_label = tk.Label(root, text="Welcome!", font=("Arial", 12), bg="#ffd8b2", fg="black")
status_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
