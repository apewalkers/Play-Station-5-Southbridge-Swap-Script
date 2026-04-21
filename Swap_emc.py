import os
import struct
import shutil

# Constants
HEADER_SIGNATURE = bytes.fromhex("53 4F 4E 59 20 43 4F 4D 50 55 54 45 52 20 45 4E 54 45 52 54 41 49 4E 4D 45 4E 54 20 49 4E 43 2E")
PATCH_SIZE = 0x7E000
REQUIRED_BIN_SIZE = 0x100000  # 0xFFFFF + 1
STR1_OFFSET = 0x1C7230
STR1_SIZE = 0x20
STR2_OFFSET = 0x1C7210
STR2_SIZE = 0x12

# Working directory
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
IN_DIR = os.path.join(WORKING_DIR, "IN")
OUT_DIR = os.path.join(WORKING_DIR, "OUT")

def get_bin_files_with_signature():
    bin_files = []
    for filename in os.listdir(IN_DIR):
        if filename.upper().endswith(".BIN"):
            path = os.path.join(IN_DIR, filename)
            with open(path, "rb") as f:
                header = f.read(len(HEADER_SIGNATURE))
                if header == HEADER_SIGNATURE:
                    bin_files.append(filename)
    return bin_files

def read_string(data, offset, size):
    return data[offset:offset+size].split(b'\x00')[0].decode(errors='ignore').strip()

def patch_bin(file_path, patch_data):
    with open(file_path, "rb") as f:
        original_data = f.read()

    if len(original_data) < REQUIRED_BIN_SIZE:
        original_data += b'\x00' * (REQUIRED_BIN_SIZE - len(original_data))

    patched_data = bytearray(original_data)

    patched_data[0x4000:0x82000] = patch_data
    patched_data[0x82000:0x100000] = patch_data

    return patched_data, original_data

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    matching_files = get_bin_files_with_signature()
    if not matching_files:
        print("No matching .BIN files found in the IN folder.")
        return

    for filename in matching_files:
        print(f"\nFound matching file: {filename}")
        user_choice = input("Patch with 61 or 69? (enter 61 or 69): ").strip()
        if user_choice not in ("61", "69"):
            print("Invalid choice, skipping this file.")
            continue

        patch_path = os.path.join(WORKING_DIR, user_choice, f"{user_choice}.bin")
        if not os.path.isfile(patch_path):
            print(f"Patch file {patch_path} not found.")
            continue

        with open(patch_path, "rb") as pf:
            patch_data = pf.read()

        if len(patch_data) != PATCH_SIZE:
            print(f"Patch file must be exactly 0x7E000 bytes. Found: {len(patch_data)} bytes.")
            continue

        bin_path = os.path.join(IN_DIR, filename)
        patched_data, original_data = patch_bin(bin_path, patch_data)

        str1 = read_string(original_data, STR1_OFFSET, STR1_SIZE)
        str2 = read_string(original_data, STR2_OFFSET, STR2_SIZE)
        output_folder_name = f"{str1}_{str2}".replace(" ", "_").replace("/", "_")
        output_folder_path = os.path.join(OUT_DIR, output_folder_name)
        os.makedirs(output_folder_path, exist_ok=True)

        # Save original copy
        shutil.copy(bin_path, os.path.join(output_folder_path, filename))

        # Save patched version
        patched_path = os.path.join(output_folder_path, f"patched_{filename}")
        with open(patched_path, "wb") as f:
            f.write(patched_data)

        print(f"Saved original and patched BIN to: {output_folder_path}")

        # Ask to delete
        delete = input("Delete the original file from IN folder? (y/n): ").strip().lower()
        if delete == 'y':
            os.remove(bin_path)
            print(f"Deleted {filename} from IN folder.")

if __name__ == "__main__":
    main()
