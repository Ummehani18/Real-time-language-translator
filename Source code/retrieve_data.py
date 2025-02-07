import tkinter as tk
from tkinter import ttk
import pygame
from pymongo import MongoClient
import gridfs
import io
import os

# Initialize pygame for audio playback
pygame.mixer.init()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB URI if needed
db = client["translator_database"]  # Replace with your database name
fs = gridfs.GridFS(db)
collection = db["translated_file"]  # Collection for storing translated files

# Variable to store the current sound object
current_sound = None

# Function to fetch filenames from the database
def fetch_filenames():
    return [file["filename"] for file in collection.find({}, {"filename": 1, "_id": 0})]

# Function to store audio file in MongoDB
def store_audio(filename, file_path):
    """Stores an audio file in MongoDB using GridFS."""
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
        
        # Check if the file already exists and delete if needed
        existing_file = collection.find_one({"filename": filename})
        if existing_file:
            collection.delete_one({"filename": filename})

        # Store the audio file in MongoDB using GridFS
        collection.insert_one({"filename": filename, "filedata": file_data})

        print(f"File '{filename}' successfully stored in MongoDB.")
    except Exception as e:
        print(f"Error storing file: {e}")

# Function to play the selected audio file
def play_audio():
    global current_sound
    selected_file = file_listbox.get(tk.ACTIVE)
    if selected_file:
        try:
            # Stop the current audio if it's playing
            if current_sound and pygame.mixer.get_busy():
                current_sound.stop()

            # Retrieve the audio file from MongoDB
            file_doc = collection.find_one({"filename": selected_file})
            if file_doc and "filedata" in file_doc:
                audio_data = file_doc["filedata"]

                # Load audio data into memory using BytesIO
                audio_stream = io.BytesIO(audio_data)

                # Use pygame's Sound object for in-memory playback
                current_sound = pygame.mixer.Sound(audio_stream)
                current_sound.play()

                status_label.config(text=f"Playing: {selected_file}", fg="green")
            else:
                status_label.config(text="Error: File data not found", fg="red")
        except Exception as e:
            status_label.config(text=f"Error: {e}", fg="red")
    else:
        status_label.config(text="No file selected.", fg="orange")

# Function to replay the audio file
def replay_audio():
    global current_sound
    selected_file = file_listbox.get(tk.ACTIVE)
    if selected_file:
        try:
            # Stop the current audio if it's playing
            if current_sound and pygame.mixer.get_busy():
                current_sound.stop()

            # Retrieve the audio file from MongoDB
            file_doc = collection.find_one({"filename": selected_file})
            if file_doc and "filedata" in file_doc:
                audio_data = file_doc["filedata"]

                # Load audio data into memory using BytesIO
                audio_stream = io.BytesIO(audio_data)

                # Use pygame's Sound object for in-memory playback
                current_sound = pygame.mixer.Sound(audio_stream)
                current_sound.play()

                status_label.config(text=f"Replaying: {selected_file}", fg="green")
            else:
                status_label.config(text="Error: File data not found", fg="red")
        except Exception as e:
            status_label.config(text=f"Error: {e}", fg="red")
    else:
        status_label.config(text="No file selected.", fg="orange")

# Create the main window
root = tk.Tk()
root.title("Translated Audio Files")
root.geometry("800x600")  # Set a specific size for the window
root.resizable(True, True)  # Allow resizing
root.config(bg="#ffd8b2")

# Title Label
title_label = tk.Label(root, text="Translated Audio Files", font=("Helvetica", 18, "bold"), bg="#FFAE42", fg="#333")
title_label.pack(pady=10, fill=tk.X)

# Frame for file list and buttons
frame = tk.Frame(root, bg="#FFAE42")
frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=False)

# File Listbox
file_listbox = tk.Listbox(frame, font=("Arial", 14), bg="#ffd8b2", fg="#000", selectbackground="#90ee90")
file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Populate the listbox with filenames
filenames = fetch_filenames()
for file in filenames:
    file_listbox.insert(tk.END, file)

# Scrollbar for the listbox
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=file_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
file_listbox.config(yscrollcommand=scrollbar.set)

# Play Button
play_button = tk.Button(root, text="Play Audio", command=play_audio, bg="#90ee90", font=("Arial", 14), width=20)
play_button.pack(pady=20)

# Replay Button
replay_button = tk.Button(root, text="Replay Audio", command=replay_audio, bg="#90ee90", font=("Arial", 14), width=20)
replay_button.pack(pady=20)

# Status Label
status_label = tk.Label(root, text="Select a file and click 'Play Audio'", font=("Arial", 14), bg="#ffd8b2")
status_label.pack(pady=20)

# Simulate translation and store translated audio file
# Replace with actual translation and audio generation process
def simulate_translation():
    # Simulate generating an audio file (for example, as a WAV file)
    translated_audio_path = "translated_speech.wav"  # Replace with actual generated file path

    # Check if the file exists, or simulate it being created
    if not os.path.exists(translated_audio_path):
        # Simulating a dummy WAV file creation if it's not present
        with open(translated_audio_path, "wb") as f:
            f.write(b"dummy audio data")

    # Call the store_audio function to save the file in MongoDB
    store_audio("translated_speech.wav", translated_audio_path)

    # Refresh the listbox with the new file
    filenames = fetch_filenames()
    file_listbox.delete(0, tk.END)
    for file in filenames:
        file_listbox.insert(tk.END, file)

# Add a button to simulate translation and storing the file
simulate_button = tk.Button(root, text="Simulate Translation", command=simulate_translation, bg="#90ee90", font=("Arial", 14), width=20)
simulate_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
