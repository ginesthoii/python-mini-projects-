import qrcode

def make_qr(data: str, out_path: str = "qrcode.png"):
    img = qrcode.make(data)
    img.save(out_path)
    return out_path

if __name__ == "__main__":
    data = input("Enter text/URL: ").strip()
    path = make_qr(data)
    print("QR code saved as", path)
