import os
import hashlib
import shutil

# Desktop path
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")

# Scan everything on the Desktop
SCAN_FOLDER = DESKTOP

# Folder where duplicates will be moved
DUPLICATE_FOLDER = os.path.join(DESKTOP, "PDF_Duplicates")

os.makedirs(DUPLICATE_FOLDER, exist_ok=True)

hashes = {}
duplicates_found = 0

def get_file_hash(filepath):
    hasher = hashlib.sha256()

    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()

print("Scanning all Desktop folders for duplicate PDFs...\n")

for root, dirs, files in os.walk(SCAN_FOLDER):

    # Skip the duplicates folder itself
    if os.path.abspath(root).startswith(os.path.abspath(DUPLICATE_FOLDER)):
        continue

    for file in files:
        if file.lower().endswith(".pdf"):
            filepath = os.path.join(root, file)

            try:
                file_hash = get_file_hash(filepath)

                if file_hash in hashes:
                    print(f"\nDuplicate Found")
                    print(f"Keep : {hashes[file_hash]}")
                    print(f"Move : {filepath}")

                    destination = os.path.join(
                        DUPLICATE_FOLDER,
                        os.path.basename(filepath)
                    )

                    counter = 1
                    while os.path.exists(destination):
                        name, ext = os.path.splitext(
                            os.path.basename(filepath)
                        )
                        destination = os.path.join(
                            DUPLICATE_FOLDER,
                            f"{name}_{counter}{ext}"
                        )
                        counter += 1

                    shutil.move(filepath, destination)
                    duplicates_found += 1

                else:
                    hashes[file_hash] = filepath

            except Exception as e:
                print(f"Error reading {filepath}: {e}")

print("\nScan complete!")
print(f"Duplicates moved: {duplicates_found}")
print(f"Duplicates folder: {DUPLICATE_FOLDER}")