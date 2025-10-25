# Cookie File Organizer

A simple and robust Python script to parse a specially formatted text file (e.g., `valide.txt` or `cookie.txt`) and organize its content into separate, cleanly named text files.

## Features

-   **Parses Delimited Blocks:** Splits a source file based on a `---------------------------` separator.
-   **Intelligent Pairing:** Correctly pairs header blocks with their corresponding data blocks.
-   **Dynamic Filename Support:** Defaults to looking for `valide.txt`, but prompts the user for a different filename if it's not found.
-   **Sanitized Naming:** Extracts the filename from the "Parsing Info:" line in the header and sanitizes it to create valid filenames for any OS.
-   **Organized Output:** Saves all the generated files into a dedicated `Organized_Cookies` folder.
-   **Robust Error Handling:** Provides clear feedback on progress, skips corrupted or empty records, and handles unexpected errors gracefully.

## How to Use (For End-Users)

You can run this script without installing Python by using the pre-compiled executable.

1.  **Download:** Go to the [Releases page](https://github.com/mrlucyfear/Cookie-Organizer/releases) and download the `organizer.exe` file from the latest release.
2.  **Prepare Your File:** Place the `organizer.exe` in the same folder as your `valide.txt` (or other source file).
3.  **Run:** Double-click `organizer.exe`.
4.  **Check the Output:** A new folder named `Organized_Cookies` will be created in the same directory, containing all the parsed files.

## How to Use (For Developers)

### Prerequisites

-   Python 3.x
-   No external libraries are needed.

### Running the Script

1.  Clone this repository: `git clone https://github.com/mrlucyfear/Cookie-Organizer.git`
2.  Navigate to the project directory: `cd Cookie-Organizer`
3.  Place your `valide.txt` file in this directory.
4.  Run the script from your terminal: `python organizer.py`

### Building the Executable

If you wish to compile the script into a standalone `.exe` yourself, you will need `pyinstaller`.

1.  Install PyInstaller: `pip install pyinstaller`
2.  Run the build command from the project directory:
    ```bash
    # For a version with a console window (recommended)
    pyinstaller --onefile organizer.py
    ```
3.  The final `organizer.exe` will be located in the `dist` folder.


### ORIGINAL VALID.TXT

<img width="982" height="596" alt="image" src="https://github.com/user-attachments/assets/f0cb98df-0152-4730-a15b-aacf27d75e06" />


<img width="982" height="596" alt="image" src="https://github.com/user-attachments/assets/a5d7d67e-fb74-4fc4-b0b3-208a9218a974" />



<img width="982" height="596" alt="image" src="https://github.com/user-attachments/assets/69f8372d-26b6-4c52-9256-ea28eadf20e0" />


<img width="982" height="596" alt="image" src="https://github.com/user-attachments/assets/30c9c047-9e80-409f-8f79-1527d0a0a682" />





