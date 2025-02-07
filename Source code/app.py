import subprocess
from tkinter import Tk, Canvas, Button
from PIL import Image, ImageTk

def on_continue():
    print("Continue button clicked!")
    # You can specify the path to your Python script here
    subprocess.run(["python", "select_option.py"])  # Replace with the actual Python file path
    root.destroy()  # Close the current application when "Continue" is pressed

# Create the main window
root = Tk()
root.title("REAL-TIME LANGUAGE TRANSLATOR")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")  # Full screen

# Load and set the background image
bg_image = Image.open("bg.png")  # Replace with your image file path
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))  # Adjust to full screen
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas and add the background image
canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.create_image(0, 0, anchor="nw", image=bg_photo)
canvas.pack(fill="both", expand=True)

# Add transparent text directly on the canvas
canvas.create_text(
    40, 90,  # X and Y position of the text
    text="  'Translation isn’t just about switching words,\nit’s about bridging gaps between people......'",
    font=("Times New Roman", 18, "bold"),
    fill="#000000",  # black color text
    anchor="nw"
)


# Add a Continue Button on the bottom right
continue_button = Button(
    root,
    text="Continue",
    font=("Arial", 14, "bold"),
    bg="black",
    fg="orange",
    activebackground="orange",
    activeforeground="black",
    command=on_continue
)
continue_button.place(relx=0.95, rely=0.9, anchor="e", width=150, height=50)

# Run the application loop
root.mainloop()

