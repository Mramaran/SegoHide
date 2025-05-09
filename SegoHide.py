import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# Encode message into image
def encode_image(img_path, message, output_path):
    img = Image.open(img_path)
    encoded = img.copy()
    width, height = img.size
    message += "###END###"
    binary_msg = ''.join([format(ord(char), '08b') for char in message])
    data_index = 0

    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for n in range(3):
                if data_index < len(binary_msg):
                    pixel[n] = pixel[n] & ~1 | int(binary_msg[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
            if data_index >= len(binary_msg):
                break
        if data_index >= len(binary_msg):
            break

    encoded.save(output_path)

# Decode message from image
def decode_image(img_path):
    img = Image.open(img_path)
    binary_data = ""
    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            for n in range(3):
                binary_data += str(pixel[n] & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ""
    for byte in all_bytes:
        char = chr(int(byte, 2))
        message += char
        if "###END###" in message:
            break
    return message.replace("###END###", "")

# GUI Class
class StegoApp:
    def __init__(self, master):
        self.master = master
        master.title("🧑‍💻 StegoHide - Hacker Edition")
        master.geometry("460x480")
        master.configure(bg="#0f0f0f")

        self.image_path = ""

        title_font = ("Courier", 20, "bold")
        text_font = ("Courier", 10)

        self.label = tk.Label(master, text="🧑‍💻 StegoHide", font=title_font, bg="#0f0f0f", fg="#00ff00")
        self.label.pack(pady=12)

        self.select_button = tk.Button(master, text="📁 Select Image", command=self.select_image, width=25,
                                       bg="#111", fg="#00ff00", font=text_font, activebackground="#222")
        self.select_button.pack(pady=6)

        self.message_label = tk.Label(master, text="✏️ Enter Secret Message:", bg="#0f0f0f", fg="#00ff00", font=text_font)
        self.message_label.pack()

        self.text_box = tk.Text(master, height=6, width=48, bg="#000", fg="#00ff00", insertbackground="#00ff00",
                                font=text_font, borderwidth=2, relief="solid")
        self.text_box.pack(pady=6)

        self.encode_button = tk.Button(master, text="🔐 Encode & Save", command=self.encode, width=25,
                                       bg="#111", fg="#00ff00", font=text_font, activebackground="#222")
        self.encode_button.pack(pady=6)

        self.decode_button = tk.Button(master, text="🔓 Decode Message", command=self.decode, width=25,
                                       bg="#111", fg="#00ff00", font=text_font, activebackground="#222")
        self.decode_button.pack(pady=6)

        self.output_label = tk.Label(master, text="", bg="#0f0f0f", fg="#00ff00", font=("Courier", 9, "italic"))
        self.output_label.pack(pady=6)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.bmp")])
        if self.image_path:
            self.output_label.config(text=f"Selected: {self.image_path.split('/')[-1]}")

    def encode(self):
        if not self.image_path:
            messagebox.showerror("Error", "Select an image first.")
            return
        message = self.text_box.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Enter a message to encode.")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if output_path:
            encode_image(self.image_path, message, output_path)
            messagebox.showinfo("Success", "Message encoded & image saved.")
            self.text_box.delete("1.0", tk.END)

    def decode(self):
        if not self.image_path:
            messagebox.showerror("Error", "Select an image first.")
            return
        hidden_message = decode_image(self.image_path)
        self.text_box.delete("1.0", tk.END)
        self.text_box.insert(tk.END, hidden_message)
        messagebox.showinfo("Decoded", "Message extracted.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()
