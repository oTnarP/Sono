import os
import threading
from tkinter import *
from tkinter import filedialog, ttk
import whisper
from pathlib import Path

# Function to handle transcription in a separate thread
def transcribe_audio():
    # Disable buttons during transcription
    browse_button.config(state=DISABLED)
    transcribe_button.config(state=DISABLED)
    translate_button.config(state=DISABLED)
    
    # Reset progress bar and textbox
    progress_bar['value'] = 0
    text_box.delete(1.0, END)
    
    # Load the Whisper model
    model = whisper.load_model("large")  # Use a larger model for better accuracy
    
    # Get the selected audio file path and language
    audio_file = file_path.get()
    selected_language = languages[language_var.get()]  # Get the ISO-639-1 code from the dropdown
    
    if not audio_file or not Path(audio_file).exists():
        text_box.insert(END, "Error: No valid audio file selected.")
        enable_buttons()
        return
    
    # Update progress bar and start transcription
    def update_progress():
        progress_bar['value'] = 50  # Simulate halfway progress
        root.update_idletasks()
        
        # Perform transcription with the selected language
        result = model.transcribe(audio_file, language=selected_language)
        progress_bar['value'] = 100  # Complete progress
        
        # Display the transcription in the textbox
        text_box.insert(END, f"Transcription:\n{result['text']}")
        
        # Enable buttons after transcription
        enable_buttons()
    
    # Run transcription in a separate thread to avoid freezing the GUI
    threading.Thread(target=update_progress).start()

# Function to handle translation in a separate thread
def translate_audio():
    # Disable buttons during translation
    browse_button.config(state=DISABLED)
    transcribe_button.config(state=DISABLED)
    translate_button.config(state=DISABLED)
    
    # Reset progress bar and textbox
    progress_bar['value'] = 0
    text_box.delete(1.0, END)
    
    # Load the Whisper model
    model = whisper.load_model("large")  # Use a larger model for better accuracy
    
    # Get the selected audio file path and language
    audio_file = file_path.get()
    selected_language = languages[language_var.get()]  # Get the ISO-639-1 code from the dropdown
    
    if not audio_file or not Path(audio_file).exists():
        text_box.insert(END, "Error: No valid audio file selected.")
        enable_buttons()
        return
    
    # Update progress bar and start translation
    def update_progress():
        progress_bar['value'] = 50  # Simulate halfway progress
        root.update_idletasks()
        
        # Perform transcription first to debug
        transcription_result = model.transcribe(audio_file, language=selected_language)
        text_box.insert(END, f"Transcription:\n{transcription_result['text']}\n\n")
        
        # Perform translation
        translation_result = model.transcribe(audio_file, task="translate", language=selected_language)
        progress_bar['value'] = 100  # Complete progress
        
        # Display the translated text in the textbox
        text_box.insert(END, f"Translation:\n{translation_result['text']}")
        
        # Enable buttons after translation
        enable_buttons()
    
    # Run translation in a separate thread to avoid freezing the GUI
    threading.Thread(target=update_progress).start()

# Helper function to enable all buttons
def enable_buttons():
    browse_button.config(state=NORMAL)
    transcribe_button.config(state=NORMAL)
    translate_button.config(state=NORMAL)

# Function to open a file dialog and select an audio file
def browse_file():
    file_selected = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=(("Audio Files", "*.mp3 *.wav *.m4a"), ("All Files", "*.*"))
    )
    if file_selected:
        file_path.set(file_selected)
        file_label.config(text=f"Selected File: {os.path.basename(file_selected)}")

# Create the main application window
root = Tk()
root.title("Sono - Audio Transcriber & Translator")
root.geometry("600x500")  # Medium-sized window
root.resizable(False, False)

# Variable to store the selected file path
file_path = StringVar()

# Label for selected file
file_label = Label(root, text="No file selected", font=("Arial", 10))
file_label.pack(pady=10)

# Browse button
browse_button = Button(root, text="Browse Audio File", command=browse_file, font=("Arial", 12))
browse_button.pack(pady=10)

# Dropdown for language selection
language_var = StringVar()
language_var.set("Japanese")  # Default language: Japanese

# Dictionary mapping full language names to their ISO-639-1 codes
languages = {
    "English": "en",
    "Japanese": "ja",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "Hindi": "hi",
    "Korean": "ko",
    "Russian": "ru",
    "Italian": "it",
    "Portuguese": "pt"
}

Label(root, text="Select Audio Language:", font=("Arial", 10)).pack(pady=5)
language_dropdown = ttk.Combobox(root, textvariable=language_var, state="readonly", font=("Arial", 10))
language_dropdown['values'] = list(languages.keys())  # Show full language names in the dropdown
language_dropdown.pack(pady=5)

# Progress bar
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=500, mode='determinate')
progress_bar.pack(pady=20)

# Transcribe button
transcribe_button = Button(root, text="Transcribe", command=transcribe_audio, font=("Arial", 12))
transcribe_button.pack(pady=10)

# Translate button
translate_button = Button(root, text="Translate to English", command=translate_audio, font=("Arial", 12))
translate_button.pack(pady=10)

# Textbox for displaying transcription/translation
text_box = Text(root, wrap=WORD, height=10, font=("Arial", 12))
text_box.pack(pady=10, padx=10, fill=BOTH, expand=True)

# Run the application
root.mainloop()