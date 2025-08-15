import os, shutil

def organize(folder: str):
    for filename in os.listdir(folder):
        full = os.path.join(folder, filename)
        if not os.path.isfile(full):
            continue
        ext = os.path.splitext(filename)[1].lower().strip(".")
        if not ext:
            continue
        dest = os.path.join(folder, ext)
        os.makedirs(dest, exist_ok=True)
        shutil.move(full, os.path.join(dest, filename))
    print("Files organized by extension.")

if __name__ == "__main__":
    folder = input("Folder path: ").strip()
    organize(folder)
