#import libraries
import os
import sys
import subprocess
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk

class QRCODE:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator & Scanner")
        self.root.geometry("600x400")

        # QR Code Generator
        self.label1 = tk.Label(root, text="Enter Data for QR Code Generation")
        self.label1.pack(pady=10)

        self.data_entry = tk.Entry(root, width=40)
        self.data_entry.pack(pady=10)

        self.gen_button = tk.Button(root, text="Generate QR Code", command=self.generate_qr)
        self.gen_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Save QR Code", command=self.save_qr, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.qr_label = tk.Label(root)
        self.qr_label.pack(pady=10)

        # Button to scan QR Code
        self.scan_button = tk.Button(root, text="Scan QR Code", command=self.scan_qr)
        self.scan_button.pack(pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10)

        # Initialize QR Code Variable
        self.qr_code_image = None

    def generate_qr(self):
        data = self.data_entry.get()
        if data:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4
            )
            qr.add_data(data)
            qr.make(fit=True)

            qr_image = qr.make_image(fill_color="black", back_color="white")
            self.qr_code_image = qr_image
            qr_img = ImageTk.PhotoImage(qr_image)

            self.qr_label.config(image=qr_img)
            self.qr_label.image = qr_img  
            self.save_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "Please enter data for QR Code")

    def save_qr(self):
        if self.qr_code_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.qr_code_image.save(file_path)
                messagebox.showinfo("QR Code Saved", "QR Code saved successfully")
        else:
            messagebox.showerror("Error", "Generate QR Code first")

    def scan_qr(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            image = cv2.imread(file_path)
            qr_detector = cv2.QRCodeDetector()
            data, bbox, _ = qr_detector.detectAndDecode(image)
            if bbox is not None:
                self.result_label.config(text=f'Scanned Data: {data}')
            else:
                self.result_label.config(text="QR Code not found")
        else:
            messagebox.showerror("Error", "Please select an image file")


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCODE(root)
    root.mainloop()
