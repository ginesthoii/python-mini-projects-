# QR Code Generator (Python)

A simple Python script to generate QR codes from any URL.  
You can pass the URL as a command-line argument, and it will create a PNG image.

---
## Features
- Generate QR codes for any URL.
- Customizable colors (default: black on white).
- Saves the QR code as `qrcode.png`.

---

## Installation
First, install the required library:

```bash
pip install qrcode[pil]


 Usage

Run the script with the URL you want to encode:

python generateqrcode.py <URL>

python generateqrcode.py https://github.com

This will generate a file named qrcode.png in the current directory.

 Notes
	•	If you don’t provide a URL, the script will print usage instructions.
	•	You can edit the script to change colors or file name if needed.
