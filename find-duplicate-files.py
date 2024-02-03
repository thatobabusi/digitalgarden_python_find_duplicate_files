import hashlib
import os
from prettytable import PrettyTable

def hash_file(file_path):
    """Generate MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()

def find_duplicates(folder_path):
    """Find duplicate files in the given folder."""
    hashes = {}
    duplicates = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = hash_file(file_path)

            if file_hash in hashes:
                duplicates.append((file_path, hashes[file_hash]))
            else:
                hashes[file_hash] = file_path

    return duplicates

def delete_file(file_path):
    """Delete a file and handle errors."""
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except OSError as e:
        print(f"Error: {e.strerror} - {file_path}")

def display_duplicates(duplicates):
    """Display duplicates in a table format."""
    table = PrettyTable()
    table.field_names = ["Index", "Duplicate File", "Original File"]
    for index, (dup, orig) in enumerate(duplicates, start=1):
        table.add_row([index, dup, orig])
    print(table)

def manage_duplicates(duplicates):
    """Let the user manage duplicates after displaying them."""
    for i, (dup, orig) in enumerate(duplicates, start=1):
        print(f"\nManage Duplicate {i}:")
        print(f"Duplicate: {dup}\nOriginal: {orig}")
        choice = input("Select action - Delete (B)oth, (L)eft, (R)ight, (S)kip, (E)xit: ").strip().upper()
        if choice == 'B':
            delete_file(dup)
            delete_file(orig)
        elif choice == 'L':
            delete_file(dup)
        elif choice == 'R':
            delete_file(orig)
        elif choice == 'E':
            print("Exiting...")
            break

# Main program flow
folder = input("Enter the path of the folder to check for duplicates: ")
duplicates = find_duplicates(folder)

if duplicates:
    print("Found duplicate files:")
    display_duplicates(duplicates)
    manage = input("Do you want to manage duplicates? (Y/N): ").strip().upper()
    if manage == 'Y':
        manage_duplicates(duplicates)
    else:
        print("Exiting without managing duplicates.")
else:
    print("No duplicate files found.")
