# -*- coding: utf-8 -*-
"""
Cookie File Organizer

A script to parse a specially formatted text file (e.g., 'valide.txt') containing
cookie data. It splits the file into header and data blocks, extracts a filename
from each header, and saves the corresponding data into a new, sanitized text file.
All output files are stored in a dedicated 'Organized_Cookies' directory.
"""

import os
import sys
import traceback

# --- CONFIGURATION CONSTANTS ---

DEFAULT_INPUT_FILENAME = 'valide.txt'
OUTPUT_DIRECTORY_NAME = 'Organized_Cookies'
BLOCK_SEPARATOR = '---------------------------'


def sanitize_filename(name: str) -> str:
    """
    Removes characters invalid for filenames on most operating systems.

    Args:
        name (str): The initial string intended to be used as a filename.

    Returns:
        str: A sanitized string safe for use as a filename.
    """
    # List of characters that are invalid in Windows, macOS, and Linux filenames.
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        name = name.replace(char, '_')
        
    # Truncate to 150 characters to avoid "Filename too long" errors on some systems.
    return name[:150]


def organize_cookies():
    """
    Main function to parse and organize the cookie file.
    Handles file discovery, reading, parsing, and writing the output files.
    """
    # --- 1. SCRIPT DIRECTORY SETUP ---
    # Ensure the script operates from its own directory, which is crucial for
    # finding the input file, especially when run as a compiled executable.
    try:
        # 'sys.frozen' is a flag set by PyInstaller when the script is packaged.
        if getattr(sys, 'frozen', False):
            script_dir = os.path.dirname(sys.executable)
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
    except Exception as e:
        print(f"FATAL ERROR: Could not determine or change script directory: {e}")
        return

    print(f"Script is running in: {script_dir}")

    # --- 2. DYNAMIC INPUT FILE DISCOVERY ---
    input_filename = DEFAULT_INPUT_FILENAME

    # If the default file doesn't exist, prompt the user for an alternative name.
    if not os.path.exists(DEFAULT_INPUT_FILENAME):
        print(f"INFO: Default file '{DEFAULT_INPUT_FILENAME}' not found.")
        try:
            user_filename = input("Please enter the name of the file to process (e.g., cookies.txt): ")
            if not user_filename.strip():
                print("ERROR: No filename entered. Exiting.")
                return
            input_filename = user_filename.strip()
        except (KeyboardInterrupt, EOFError):
            # Handle cases where the user cancels the input (e.g., Ctrl+C).
            print("\nOperation cancelled by user. Exiting.")
            return

    # Final check to ensure the selected file (default or user-provided) exists.
    if not os.path.exists(input_filename):
        print(f"\nERROR: Input file '{input_filename}' could not be found.")
        print(f"Please make sure the file is in the same folder as the script.")
        return
    
    print(f"Processing file: '{input_filename}'")

    # --- 3. OUTPUT DIRECTORY SETUP ---
    if not os.path.exists(OUTPUT_DIRECTORY_NAME):
        try:
            os.makedirs(OUTPUT_DIRECTORY_NAME)
            print(f"Created output directory: '{OUTPUT_DIRECTORY_NAME}'")
        except PermissionError:
            print(f"ERROR: Permission denied. Could not create directory '{OUTPUT_DIRECTORY_NAME}'.")
            return

    # --- 4. FILE READING AND PRE-PROCESSING ---
    print(f"Reading content from '{input_filename}'...")
    try:
        # Use 'utf-8' with 'errors=ignore' for maximum compatibility with text files from various sources.
        with open(input_filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Could not read '{input_filename}'. Details: {e}")
        return
    
    # Split the entire file content by the separator and remove any empty blocks resulting from the split.
    all_blocks = [block.strip() for block in content.split(BLOCK_SEPARATOR) if block.strip()]

    if not all_blocks:
        print(f"WARNING: '{input_filename}' is empty or no data blocks were found.")
        return
    
    print(f"Found {len(all_blocks)} total blocks. Now pairing them up.")

    # --- 5. MAIN PROCESSING LOOP ---
    # Initialize counters for the final summary.
    files_created = 0
    files_skipped = 0
    
    # Iterate through the blocks in steps of 2, pairing a header with a data block.
    for i in range(0, len(all_blocks), 2):
        # This check handles cases where the file ends with a header but no data block.
        if i + 1 >= len(all_blocks):
            print(f"WARNING: Found an incomplete record (header without data) at the end of the file. Skipping.")
            files_skipped += 1
            continue

        header_block = all_blocks[i]
        data_block = all_blocks[i+1]
        
        # Search the header for the line that will give us the filename.
        filename_part = None
        for line in header_block.splitlines():
            if "Parsing Info:" in line:
                filename_part = line.split("Parsing Info:", 1)[1].strip()
                break
        
        if not filename_part:
            print(f"WARNING: Skipping a pair: 'Parsing Info:' not found in header block. Block content: \"{header_block[:50]}...\"")
            files_skipped += 1
            continue
            
        cookie_content = data_block.strip()

        if not cookie_content:
            print(f"WARNING: Skipping pair for '{filename_part}': The data block is empty.")
            files_skipped += 1
            continue
        
        # Sanitize the extracted name and create the full output path.
        safe_filename = sanitize_filename(filename_part) + ".txt"
        output_filepath = os.path.join(OUTPUT_DIRECTORY_NAME, safe_filename)
        
        try:
            with open(output_filepath, 'w', encoding='utf-8') as outfile:
                outfile.write(cookie_content)
            print(f"SUCCESS: Created '{safe_filename}'")
            files_created += 1
        except Exception as e:
            print(f"ERROR: Failed to create file '{safe_filename}'. Details: {e}")
            files_skipped += 1

    # --- 6. FINAL SUMMARY ---
    print("\n" + "="*20 + " SUMMARY " + "="*20)
    print(f"Processing complete.")
    print(f"Successfully created files: {files_created}")
    print(f"Skipped records due to errors or missing data: {files_skipped}")
    print("="*49)


# --- SCRIPT EXECUTION BLOCK ---
# The `if __name__ == "__main__":` block ensures this code only runs when
# the script is executed directly (not when imported as a module).
if __name__ == "__main__":
    try:
        organize_cookies()
    except Exception as e:
        # A top-level catch-all to handle any unexpected errors gracefully.
        print("\n" + "-"*52)
        print("AN UNEXPECTED ERROR OCCURRED. The script has stopped.")
        print(f"ERROR DETAILS: {e}")
        print("Traceback:")
        traceback.print_exc() # Prints the full error stack trace for debugging.
        print("-"*52)
    
    # The final input() pauses the console window, allowing the user to read the output
    # before the program closes. This is crucial when running the compiled .exe.
    print("\nScript has finished. Press Enter to exit.")
    input()
