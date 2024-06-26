import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import requests

# Define the URL for the request
url = f"http://{'172.20.10.8'}:{5000}{'/display'}"


class CounterApp:
    def __init__(self, master):
        self.master = master
        self.counter = 0

        # Set the background color of the root window to black
        self.master.configure(bg='black')

        # Create a Canvas widget
        self.canvas = Canvas(master, width=800, height=500, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Load the image using PIL
        self.original_image = Image.open("wachttijd_display.png")

        # Initial display of the image
        self.image = ImageTk.PhotoImage(self.original_image)
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

        # Create a text label on top of the image
        self.text_id = self.canvas.create_text(400, 250, text="Counter: 0", fill="white",
                                               font=("Times New Roman", 20, "bold"), anchor=tk.CENTER)

        # Bind the configure event to update the image size when the window is resized
        self.master.bind('<Configure>', self.resize_image)

        # Schedule the update_counter() function to run every second
        self.master.after(1000, self.update_counter)

        # Set the window to full screen
        self.fullscreen = False
        self.toggle_fullscreen()

        # Bind the Escape key to exit full screen mode
        self.master.bind('<Escape>', lambda event: self.exit_fullscreen())

        # Bind the F11 key to toggle full screen mode
        self.master.bind('<F12>', lambda event: self.toggle_fullscreen())

    def resize_image(self, event):
        # Get the new dimensions of the window
        new_width = event.width
        new_height = event.height

        # Maintain the aspect ratio of the image
        aspect_ratio = self.original_image.width / self.original_image.height
        if new_width / aspect_ratio <= new_height:
            resized_width = new_width
            resized_height = int(new_width / aspect_ratio)
        else:
            resized_height = new_height
            resized_width = int(new_height * aspect_ratio)

        # Resize the original image to fit the new dimensions while maintaining aspect ratio
        resized_image = self.original_image.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(resized_image)

        # Update the canvas image
        self.canvas.itemconfig(self.image_id, image=self.image)
        self.canvas.coords(self.image_id, (new_width - resized_width) // 2, (new_height - resized_height) // 2)

        # Adjust the text position based on the new dimensions
        self.canvas.coords(self.text_id, new_width // 2, new_height // 2)

    def update_counter(self):
        # Increment the counter every second
        response = requests.get(url)
        data = response.json()
        self.counter = data['wachttijd']
        self.delay = data['wachttijd_delay']
        self.update_counter_label()
        # Schedule the update_counter() function to run again after 1 second
        self.master.after(1000, self.update_counter)

    def update_counter_label(self):
        # Update the text on the canvas
        self.canvas.itemconfig(self.text_id, text= self.counter)

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.master.attributes('-fullscreen', self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.master.attributes('-fullscreen', False)

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x500")
    app = CounterApp(root)
    root.mainloop()
