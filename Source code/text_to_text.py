import tkinter as tk
from tkinter import ttk
from googletrans import Translator
import asyncio  # Import asyncio

# Initialize the translator
translator = Translator()

# Create the main window
root = tk.Tk()
root.title("Real-Time Language Translator")
root.geometry("1100x700")  # Make the window bigger
root.config(bg="#ffd8b2")

# Global variable for the keyboard frame
keyboard_frame = None

# Title Label
title_label = tk.Label(
    root, text="Text-to-Text Language Translator", font=("Helvetica", 18, "bold"), bg="#FFAE42", fg="#333"
)
title_label.pack(pady=10, fill=tk.X)

# Status Label for showing translation status
status_label = tk.Label(root, text="Enter text to translate", font=("Helvetica", 12), bg="#ffd8b2", fg="#333")
status_label.pack(pady=5)

# Function to translate text
async def translate_text():
    input_text = text_input.get("1.0", tk.END).strip()  # Get text from input field
    source = source_lang.get()  # Source language
    target = target_lang.get()  # Target language

    if input_text:
        try:
            # Preprocess input for better translation
            input_text = preprocess_text(input_text)

            # Translate text asynchronously
            translation = await translator.translate(input_text, src=source, dest=target)

            output_text.config(state=tk.NORMAL)  # Enable editing
            output_text.delete("1.0", tk.END)  # Clear previous text
            output_text.insert(tk.END, translation.text)  # Insert translated text
            output_text.config(state=tk.DISABLED)  # Disable editing

            status_label.config(text="Translation Complete", fg="green")
        except Exception as e:
            status_label.config(text=f"Translation Error: {e}", fg="red")
    else:
        status_label.config(text="Please enter text to translate.", fg="orange")

# Function to preprocess text for better results
def preprocess_text(text):
    # Clean up text for better translation
    text = text.strip()
    return text

# Function to add text to input area
def add_to_input(text):
    text_input.insert(tk.END, text)

# Function to create virtual keyboard based on selected language
def create_virtual_keyboard(language):
    global keyboard_frame  # Declaring keyboard_frame as global to modify it

    if keyboard_frame is not None:
        keyboard_frame.pack_forget()  # Clear previous keyboard
    
    # Create new keyboard frame
    keyboard_frame = tk.Frame(root, bg="#ffd8b2")
    keyboard_frame.pack(pady=10)

    # Define key layouts for different languages
    if language == 'hi':  # Hindi Keyboard
        keys = ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ए', 'ऐ', 'ओ', 'औ', 'अं', 'अः',
                    'क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 
                    'ट', 'ठ', 'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न', 
                    'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ल', 'व', 'श', 'ष', 'स', 'ह',
                    'ा', 'ि', 'ी', 'ु', 'ू', 'े', 'ै', 'ो', 'ौ', '्']

    elif language == 'kn':  # Kannada Keyboard
        keys = [ 
         'ಅ', 'ಆ', 'ಇ', 'ಈ', 'ಉ', 'ಊ',  'ೠ', 'ಎ','ಏ','ಐ','ಒ','ಓ','ಔ','ಅಂ','ಅಃ',
          'ಕ', 'ಖ', 'ಗ', 'ಘ', 'ಙ',  'ಚ', 'ಛ', 'ಜ', 'ಝ', 'ಞ', 'ಟ', 'ಠ', 'ಡ', 
    'ಢ', 'ಣ', 'ತ', 'ಥ', 'ದ', 'ಧ', 'ನ', 'ಪ', 'ಫ', 'ಬ', 'ಭ', 'ಮ',
    'ಯ', 'ರ', 'ಲ', 'ವ', 'ಶ', 'ಷ', 'ಸ', 'ಹ', 'ಳ','ಾ', 'ಿ', 'ೀ', 'ು', 'ೂ', 'ೃ', 'ೆ', 'ೇ', 'ೈ', 'ೊ', 'ೋ', 'ೌ', '್','೯','೦ ' ,'ಃ'
]
    elif language == 'te':  # Telugu Keyboard
        keys = ['అ', 'ఆ', 'ఇ', 'ఈ', 'ఉ', 'ఊ', 'ఋ', 'ౠ',  'ౘ', 'ౙ', 'ౚ', 'ౝ', 
                'క', 'ఖ', 'గ', 'ఘ', 'ఙ', 'చ', 'છ', 'జ', 'ఝ', 'ఞ', 'ట', 'ఠ', 'డ', 'ఢ', 'ణ', 
                'త', 'థ', 'ద', 'ధ', 'న', 'ప', 'ఫ', 'బ', 'భ', 'మ', 'య', 'ర', 'ల', 'వ', 'శ', 'ష', 'స', 'హ', 'ళ', 'క్ష', 'ఱ']

    # Create buttons for each key in grid layout
    row = 0
    col = 0
    for key in keys:
        button = tk.Button(keyboard_frame, text=key, width=5, height=2, command=lambda key=key: add_to_input(key))
        button.grid(row=row, column=col, padx=5, pady=5)
        col += 1
        if col > 14:  # Change number of columns per row as needed
            col = 0
            row += 1

# Function to reset the keyboard
def reset_keyboard():
    global keyboard_frame

    if keyboard_frame is not None:
        keyboard_frame.pack_forget()  # This will hide the virtual keyboard completely
    status_label.config(text="Keyboard reset. Select language again.", fg="#ffd8b2")

# Frame for input and output
frame = tk.Frame(root, bg="#ffd8b2")
frame.pack(pady=10, padx=20, fill=tk.X)

# Source Language
source_lang_label = tk.Label(frame, text="Source Language:", font=("Arial", 12), bg="#ffd8b2")
source_lang_label.grid(row=0, column=0, padx=5)
source_lang = ttk.Combobox(frame, values=["English", "Hindi", "Kannada", "Telugu"], width=10)
source_lang.set("english")
source_lang.grid(row=0, column=1, padx=5)

# Target Language
target_lang_label = tk.Label(frame, text="Target Language:", font=("Arial", 12), bg="#ffd8b2")
target_lang_label.grid(row=0, column=2, padx=5)
target_lang = ttk.Combobox(frame, values=["English", "Hindi", "Kannada", "Telugu"], width=10)
target_lang.set("hindi")
target_lang.grid(row=0, column=3, padx=5)

# Frame for input and output text areas side by side
io_frame = tk.Frame(root, bg="#ffd8b2")
io_frame.pack(pady=10)

# Input Text Area - Positioned to the left in the io_frame
text_input = tk.Text(io_frame, height=5, width=50, font=("Arial", 12), bg="#fff8dc", fg="#000")
text_input.grid(row=0, column=0, padx=10, pady=10)

# Output Text Area - Positioned to the right in the io_frame
output_text = tk.Text(io_frame, height=5, width=50, font=("Arial", 12), bg="#e6e6fa", fg="#000", state=tk.DISABLED)
output_text.grid(row=0, column=1, padx=10, pady=10)

# Translate Button - Positioned below the text areas
translate_button = tk.Button(root, text="Translate", command=lambda: asyncio.run(translate_text()), bg="#87ceeb", font=("Arial", 12), width=20)
translate_button.pack(pady=10)

# Language selection buttons
language_button_frame = tk.Frame(root,bg="#ffd8b2")
language_button_frame.pack(pady=10)

button_hi = tk.Button(language_button_frame, text="Hindi", command=lambda: create_virtual_keyboard('hi'), bg="#90ee90", font=("Arial", 12))
button_hi.grid(row=0, column=0, padx=10, pady=5)

button_kn = tk.Button(language_button_frame, text="Kannada", command=lambda: create_virtual_keyboard('kn'), bg="#90ee90", font=("Arial", 12))
button_kn.grid(row=0, column=1, padx=10, pady=5)

button_te = tk.Button(language_button_frame, text="Telugu", command=lambda: create_virtual_keyboard('te'), bg="#90ee90", font=("Arial", 12))
button_te.grid(row=0, column=2, padx=10, pady=5)

# Reset Button
reset_button = tk.Button(language_button_frame, text="Reset", command=reset_keyboard, bg="#ff6666", font=("Arial", 12), width=15)
reset_button.grid(row=1, column=0, columnspan=4, pady=10)

# Start the Tkinter event loop
root.mainloop()
