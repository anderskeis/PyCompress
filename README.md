# PyCompress

A robust command-line tool to batch compress and resize images in nested directories.

## Features

- **Recursive Processing:** Automatically finds images in subdirectories.
- **Safe by Default:** Saves compressed images to a new directory (mirrors structure) instead of overwriting.
- **Configurable:** Customize compression quality and resize factor via command-line arguments.
- **Cross-Platform:** Works on Linux, Windows, and macOS.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PyCompress.git
   cd PyCompress
   ```

2. Create and activate a virtual environment:

   **Linux / macOS:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script by providing the input directory containing your images.

### Basic Usage
Compress all images in the `pictures` folder and save them to `pictures_compressed` (default output):

```bash
python main.py pictures
```

### Custom Output Directory
Specify where to save the compressed images:

```bash
python main.py pictures --output /path/to/output_folder
```

### Adjust Quality and Size
Set custom JPEG quality (1-100) and resize factor.
Example: Quality 80, divide dimensions by 4 (e.g., 2000x2000 -> 500x500):

```bash
python main.py pictures --quality 80 --resize 4
```

### Disable Recursion
Only process images in the top-level directory, ignoring subfolders:

```bash
python main.py pictures --no-recursive
```

## Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `input_dir` | | Path to the directory containing images. | Required |
| `--output` | `-o` | Path to the output directory. | `[input_dir]_compressed` |
| `--quality` | `-q` | Image quality (1-100). | `70` |
| `--resize` | `-r` | Factor to divide image dimensions by. | `2` |
| `--no-recursive` | | Disable recursive directory search. | `False` (Recursive is on) |

## Requirements

- Python 3.6+
- Pillow

