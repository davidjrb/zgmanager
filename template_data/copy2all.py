import os
import argparse
import shutil

def copy_file_to_subdirectory(src_file, suffix):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    subdirectories = [d for d in os.listdir(script_dir) if os.path.isdir(os.path.join(script_dir, d))]

    for subdir in subdirectories:
        if suffix:
            dest_filename = f"{subdir}{suffix}.csv"
            dest_file = os.path.join(script_dir, subdir, dest_filename)
            shutil.copy2(src_file, dest_file)

def main():
    parser = argparse.ArgumentParser(description="Copy a specified file to all subdirectories, renaming each copy according to its destination directory and a suffix.")
    parser.add_argument("--original", help="The name of the file to be copied.", required=True)
    parser.add_argument("--copy", help="Suffix for the copied file.", default="")
    args = parser.parse_args()

    if os.path.isfile(args.original):
        copy_file_to_subdirectory(args.original, args.copy)
        print("File copied and renamed successfully.")
    else:
        print(f"Error: The specified file '{args.original}' does not exist.")

if __name__ == "__main__":
    main()
