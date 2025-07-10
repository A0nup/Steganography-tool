import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def encode_message_in_image(image_path, message, output_path):
    image = Image.open(image_path).convert("RGB")
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '1111111111111110'  # Delimiter
    pixels = image.load()
    width, height = image.size
    index = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            rgb = [r, g, b]
            for i in range(3): 
                if index < len(binary_message):
                    rgb[i] = (rgb[i] & ~1) | int(binary_message[index])
                    index += 1
            pixels[x, y] = tuple(rgb)
            if index >= len(binary_message):
                image.save(output_path)
                return output_path
    raise ValueError("Message too long to encode in this image.")

def decode_message_from_image(image_path):
    image = Image.open(image_path).convert("RGB")
    pixels = image.load()
    width, height = image.size
    binary_data = ''

    for y in range(height):
        for x in range(width):
            for color in pixels[x, y]:  # R, G, B
                binary_data += str(color & 1)

    bytes_list = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ''
    for byte in bytes_list:
        if byte == '11111110': 
            break
        message += chr(int(byte, 2))
    return message

class StegoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Steganography Tool")
        self.master.geometry("500x300")

        tk.Label(master, text="Steganography Tool (Hide Message in Image)", font=("Arial", 14)).pack(pady=10)

        tk.Button(master, text="Select Image", command=self.load_image).pack(pady=5)

        tk.Label(master, text="Enter Message to Hide:").pack()
        self.message_entry = tk.Text(master, height=5, width=50)
        self.message_entry.pack()

        tk.Button(master, text="Encode Message", command=self.encode).pack(pady=5)
        tk.Button(master, text="Decode Message", command=self.decode).pack(pady=5)

        self.image_path = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.bmp")])
        if file_path:
            self.image_path = file_path
            messagebox.showinfo("Image Loaded", f"Loaded image:\n{file_path}")

    def encode(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return
        message = self.message_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Message cannot be empty.")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            try:
                encode_message_in_image(self.image_path, message, output_path)
                messagebox.showinfo("Success", "Message encoded and saved successfully.")
            except Exception as e:
                messagebox.showerror("Encoding Error", str(e))

    def decode(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return
        try:
            message = decode_message_from_image(self.image_path)
            messagebox.showinfo("Decoded Message", message)
        except Exception as e:
            messagebox.showerror("Decoding Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()
