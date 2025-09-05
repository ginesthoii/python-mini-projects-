# generateqrcode.py
import qrcode
import sys

# Check if user provided a URL argument
if len(sys.argv) < 2:
    print("Usage: python generateqrcode.py <URL>")
    sys.exit(1)

# Take URL from command line
url = sys.argv[1]

# Create QR code instance
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Add data and generate QR code
qr.add_data(url)
qr.make(fit=True)

# Create an image (customize colors here)
img = qr.make_image(fill_color="black", back_color="white")

# Save image
filename = "qrcode.png"
img.save(filename)

print(f"QR code for {url} generated and saved as '{filename}'")
