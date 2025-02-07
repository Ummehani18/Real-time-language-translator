import tkinter as tk
from tkinter import ttk
from googletrans import Translator
import speech_recognition as sr
import pyttsx3
import threading
from gtts import gTTS
import os
import pygame  # Use pygame to play the saved audio file
from pymongo import MongoClient  # Import MongoDB and GridFS
import gridfs
from datetime import datetime

# Initialize translator
translator = Translator()

# Initialize speech engine
speech_engine = pyttsx3.init()
speech_engine.setProperty('rate', 150)

# Initialize pygame for audio playback
pygame.mixer.init()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Update this with your MongoDB URI if needed
db = client["translator_database"]  # Replace with your database name
fs = gridfs.GridFS(db)
collection = db["translated_file"]  # Collection for storing translated files

# Create the main window
root = tk.Tk()
root.title("Speech-to-Speech Language Translator")
root.geometry("1100x700")  # Set a specific size for the window
root.resizable(True, True)  # Allow resizing
root.config(bg="#ffd8b2")

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Variable to control speech recognition
is_listening = False

# Language codes mapping
language_codes = {
    "english": "en",
    "hindi": "hi",
    "kannada": "kn",
    "telugu": "te"
}

# Function to translate text and output audio
def translate_text():
    input_text = text_input.get("1.0", tk.END).strip()  # Get text from input field
    source = language_codes.get(source_lang.get().lower(), "en")  # Get source language code
    target = language_codes.get(target_lang.get().lower(), "en")  # Get target language code

    if input_text:
        try:
            # Translate text
            translation = translator.translate(input_text, src=source, dest=target)

            # Display translated text in output widget
            text_output.delete("1.0", tk.END)
            text_output.insert(tk.END, translation.text)

            # Speak the translated text
            speech_engine.say(translation.text)
            speech_engine.runAndWait()

            # Dynamically create file name based on source and target languages along with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_file = f"translated_audio_{source}to{target}_{timestamp}.mp3"

            # Save the translated text as an audio file
            tts = gTTS(text=translation.text, lang=target)
            tts.save(audio_file)

            # Save audio to MongoDB with a timestamp to track the latest file
            with open(audio_file, "rb") as audio:
                audio_data = audio.read()
                collection.insert_one({
                    "filename": audio_file,
                    "filedata": audio_data,
                    "timestamp": datetime.now()  # Store the current time to identify the latest audio
                })

            status_label.config(text=f"Translation complete. Audio saved to MongoDB as {audio_file}.", fg="green")

            # Enable the replay button
            play_button.config(state=tk.NORMAL)

            # Play the audio immediately after translation
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()  # Unload the previous audio to make sure we can play a new one
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

        except Exception as e:
            status_label.config(text=f"Translation Error: {e}", fg="red")
    else:
        status_label.config(text="Please enter or speak text to translate.", fg="orange")

# Function for starting the speech recognition
def start_listening():
    global is_listening
    if not is_listening:
        is_listening = True
        status_label.config(text="Listening...", fg="blue")
        listen_button.config(state=tk.DISABLED)  # Disable listen button
        stop_button.config(state=tk.NORMAL)  # Enable stop button

        # Start the speech recognition in a background thread
        listening_thread = threading.Thread(target=listen_for_speech)
        listening_thread.start()

# Function to stop listening manually and trigger immediate translation and audio playback
def stop_listening():
    global is_listening
    if is_listening:
        is_listening = False
        status_label.config(text="Stopped listening. Translating...", fg="blue")
        listen_button.config(state=tk.NORMAL)  # Enable listen button
        stop_button.config(state=tk.DISABLED)  # Disable stop button

        # Get the recognized speech from the text input
        input_text = text_input.get("1.0", tk.END).strip()  # Get text from input field
        source = language_codes.get(source_lang.get().lower(), "en")  # Get source language code
        target = language_codes.get(target_lang.get().lower(), "en")  # Get target language code

        if input_text:
            try:
                # Translate text
                translation = translator.translate(input_text, src=source, dest=target)

                # Display translated text in output widget
                text_output.delete("1.0", tk.END)
                text_output.insert(tk.END, translation.text)

                # Speak the translated text
                speech_engine.say(translation.text)
                speech_engine.runAndWait()

                # Dynamically create file name based on source and target languages along with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_file = f"translated_audio_{source}to{target}_{timestamp}.mp3"

                # Save the translated text as an audio file
                tts = gTTS(text=translation.text, lang=target)
                tts.save(audio_file)

                # Save audio to MongoDB with a timestamp to track the latest file
                with open(audio_file, "rb") as audio:
                    audio_data = audio.read()
                    collection.insert_one({
                        "filename": audio_file,
                        "filedata": audio_data,
                        "timestamp": datetime.now()  # Store the current time to identify the latest audio
                    })

                status_label.config(text=f"Translation complete. Audio saved to MongoDB as {audio_file}.", fg="green")

                # Enable the replay button
                play_button.config(state=tk.NORMAL)

                # Play the audio immediately after translation
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()  # Unload the previous audio to make sure we can play a new one
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()

            except Exception as e:
                status_label.config(text=f"Translation Error: {e}", fg="red")
        else:
            status_label.config(text="Please enter or speak text to translate.", fg="orange")

# Function for continuous speech recognition
def listen_for_speech():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            # Listen to the audio input
            audio_data = recognizer.listen(source)
            spoken_text = recognizer.recognize_google(audio_data)

            # Display the recognized speech
            text_input.delete("1.0", tk.END)
            text_input.insert(tk.END, spoken_text)
            status_label.config(text=f"Recognized: {spoken_text}", fg="green")

            # Automatically translate the speech and store it in real-time
            translate_text()

        except sr.UnknownValueError:
            status_label.config(text="Speech not understood. Try again.", fg="red")
        except sr.RequestError as e:
            status_label.config(text=f"Speech Recognition Error: {e}", fg="red")

# Function to replay the most recent translated audio
def replay_audio():
    # Fetch the most recent audio file inserted into MongoDB based on timestamp or _id
    latest_audio = collection.find_one(sort=[("timestamp", -1)])  # Sort by timestamp to get the latest entry

    if latest_audio:
        audio_data = latest_audio["filedata"]
        audio_filename = latest_audio["filename"]

        # Save the audio to a local file temporarily
        with open(audio_filename, "wb") as audio_file:
            audio_file.write(audio_data)

        # Stop any currently playing audio before loading the new one
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()  # Unload the previous audio to make sure we can play a new one

        # Load and play the newly saved audio
        pygame.mixer.music.load(audio_filename)
        pygame.mixer.music.play()

        status_label.config(text=f"Replaying audio: {audio_filename}", fg="green")
    else:
        status_label.config(text="No audio found to replay.", fg="red")

# Function to reset the app (clear text and reset labels)
def reset_app():
    text_input.delete("1.0", tk.END)
    text_output.delete("1.0", tk.END)
    status_label.config(text="Welcome to Speech-to-Speech Language Translator!", fg="blue")
    play_button.config(state=tk.DISABLED)
    listen_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# Title Label
title_label = tk.Label(root, text="Speech-to-Speech Language Translator", font=("Helvetica", 18, "bold"), bg="#FFAE42", fg="#333")
title_label.pack(pady=10, fill=tk.X)

# Frame for language selection
frame = tk.Frame(root, bg="#ffd8b2")
frame.pack(pady=20, padx=40, fill=tk.X)

# Source Language
source_lang_label = tk.Label(frame, text="Source Language:", font=("Arial", 12), bg="#ffd8b2")
source_lang_label.grid(row=0, column=0, padx=5)
source_lang = ttk.Combobox(frame, values=["English", "Hindi", "Kannada", "Telugu"], width=10)
source_lang.set("English")
source_lang.grid(row=0, column=1, padx=5)

# Target Language
target_lang_label = tk.Label(frame, text="Target Language:", font=("Arial", 12), bg="#ffd8b2")
target_lang_label.grid(row=0, column=2, padx=5)
target_lang = ttk.Combobox(frame, values=["English", "Hindi", "Kannada", "Telugu"], width=10)
target_lang.set("Hindi")
target_lang.grid(row=0, column=3, padx=5)

# Text Input Area
text_input = tk.Text(root, height=5, width=70, font=("Arial", 14), bg="#ffd8b2", fg="#000")
text_input.pack(pady=20)

# Output Text Area
text_output = tk.Text(root, height=5, width=70, font=("Arial", 14), bg="#e8f5e9", fg="#000")
text_output.pack(pady=20)

# Button for translating text
translate_button = tk.Button(root, text="Translate", font=("Arial", 12), bg="#FFAE42", command=translate_text)
translate_button.pack(pady=10)

# Buttons for listening and stopping speech recognition (aligned in a single row)
listen_stop_frame = tk.Frame(root, bg="#ffd8b2")
listen_stop_frame.pack(pady=10)

listen_button = tk.Button(listen_stop_frame, text="Start Listening", font=("Arial", 12), bg="#4CAF50", command=start_listening)
listen_button.grid(row=0, column=0, padx=20)

stop_button = tk.Button(listen_stop_frame, text="Stop Listening", font=("Arial", 12), bg="#f44336", state=tk.DISABLED, command=stop_listening)
stop_button.grid(row=0, column=1, padx=20)

# Button for replaying translated audio
play_button = tk.Button(root, text="Replay Audio", font=("Arial", 12), bg="#FFAE42", state=tk.DISABLED, command=replay_audio)
play_button.pack(pady=10)

# Reset Button
reset_button = tk.Button(root, text="Reset", font=("Arial", 12), bg="#FFC107", command=reset_app)
reset_button.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="Welcome to Speech-to-Speech Language Translator!", font=("Arial", 12), bg="#ffd8b2", fg="blue")
status_label.pack(pady=10)

# Start the main event loop
root.mainloop()
