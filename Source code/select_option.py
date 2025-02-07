import tkinter as tk
import os
import subprocess  # Use subprocess to open Python scripts if needed

def open_file1():
    """Function to open a file for Text-Text Translation."""
    # Example of opening a script
    print("Text-Text Translation button clicked!")
    subprocess.run(["python", "text_to_text.py"])  # Replace with actual path
    status_label.config(text="Opening Text-Text Translation...", fg="green")

def open_file2():
    """Function to open a file for Speech-Speech Translation."""
    print("Speech-Speech Translation button clicked!")
    subprocess.run(["python","speech_to_speech.py"])  # Replace with actual path
    status_label.config(text="Opening Speech-Speech Translation...", fg="green")

def open_file3():
    """Function to open a file for One-Many Language Translation."""
    print("One-Many Language Translation button clicked!")
    subprocess.run(["python", "multi_lang.py"])  # Replace with actual path
    status_label.config(text="Opening One-Many Language Translation...", fg="green")

def open_continue_window():
    """Function to open a database stored file."""
    print("One-Many Language Translation button clicked!")
    subprocess.run(["python", "retrieve_data.py"])  # Replace with actual path
    status_label.config(text="Opening One-Many Language Translation...", fg="green")


# Create the main window
root = tk.Tk()
root.title("REAL-TIME LANGUAGE TRANSLATOR")
root.geometry("1400x200")  # Adjust the window size
root.config(bg="#FFAE42")  # Set background color to #FFAE42

# Create frames for the three sections
frame1 = tk.Frame(root, bg="#FFAE42", width=200, height=400)
frame2 = tk.Frame(root, bg="#FFAE42", width=200, height=400)
frame3 = tk.Frame(root, bg="#FFAE42", width=200, height=400)

# Place frames on the screen in equal portions horizontally
frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
frame3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

# Configure the grid layout for equal column expansion
root.grid_columnconfigure(0, weight=1, uniform="equal")
root.grid_columnconfigure(1, weight=1, uniform="equal")
root.grid_columnconfigure(2, weight=1, uniform="equal")

# Section 1 (Left)
label1 = tk.Label(frame1, text="Text-Text Translation", font=("Arial", 16), bg="#FFAE42", fg="black")
label1.pack(pady=10)

button1 = tk.Button(frame1, text="Text-Text Translation", font=("Arial", 12), bg="#003366", fg="white", command=open_file1)
button1.pack(pady=5)

# Section 2 (Middle)
label2 = tk.Label(frame2, text="Speech-Speech Translation", font=("Arial", 16), bg="#FFAE42", fg="black")
label2.pack(pady=10)

button4 = tk.Button(frame2, text="Speech-Speech Translation", font=("Arial", 12), bg="#B22222", fg="white", command=open_file2)
button4.pack(pady=5)

# Section 3 (Right)
label3 = tk.Label(frame3, text="One-Many Language Translation", font=("Arial", 16), bg="#FFAE42", fg="black")
label3.pack(pady=10)

button7 = tk.Button(frame3, text="One-Many Language Translation", font=("Arial", 12), bg="#28a745", fg="white", command=open_file3)
button7.pack(pady=5)

# Continue button
continue_button = tk.Button(root, text="Load Audio Files", font=("Arial", 14), bg="#008CBA", fg="white", command=open_continue_window)
continue_button.grid(row=1, column=1, pady=20)

# Status Label (to show file opening feedback)
status_label = tk.Label(root, text="Click a button for translation..", font=("Arial", 14), bg="#FFAE42")
status_label.grid(row=2, column=0, columnspan=3, pady=10)

# Start the Tkinter event loop
root.mainloop()

