# File Organizer

A powerful Python script that automatically organizes files in a directory by sorting them into categorized folders based on file types. Perfect for cleaning up Downloads folders, organizing project files, or maintaining any directory structure.

## Features

### 🗂️ Smart File Sorting
- Organizes files into 9 default categories (Images, Documents, Videos, Audio, etc.)
- Supports 40+ file extensions out of the box
- Automatically creates folders as needed
- Handles filename conflicts intelligently

### ⚙️ Customizable Configuration
- Add/remove categories and file extensions
- Save/load custom configurations via JSON
- Interactive configuration mode
- Persistent settings across sessions

### 🛡️ Safety Features
- **Dry run mode** - Preview changes before executing
- **Undo functionality** - Reverse last organization operation
- **Comprehensive logging** - Track all file movements
- **Conflict resolution** - Automatically renames duplicate files
- **Error handling** - Graceful handling of permission issues

### 📊 Advanced Options
- Command-line interface with multiple modes
- Operation statistics and reporting
- Empty directory cleanup
- Cross-platform compatibility (Windows, Mac, Linux)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/file-organizer-python.git
   cd file-organizer-python
   ```

2. **No additional dependencies required!** 
   - Uses only Python standard library modules
   - Compatible with Python 3.6+

## Usage

### Basic Usage

```bash
# Organize current directory
python file_organizer.py

# Organize specific directory
python file_organizer.py /path/to/directory

# Preview changes without moving files (recommended first run)
python file_organizer.py --dry-run
```

### Advanced Usage

```bash
# Interactive configuration mode
python file_organizer.py --config

# Undo last organization operation
python file_organizer.py --undo

# Clean up empty directories
python file_organizer.py --clean

# Organize Downloads folder (Windows example)
python file_organizer.py "C:\Users\YourName\Downloads" --dry-run
```

## File Categories

| Category | File Extensions |
|----------|----------------|
| **Images** | .jpg, .jpeg, .png, .gif, .bmp, .svg, .ico, .tiff, .webp |
| **Documents** | .pdf, .doc, .docx, .txt, .rtf, .odt, .pages, .tex |
| **Spreadsheets** | .xls, .xlsx, .csv, .ods, .numbers |
| **Presentations** | .ppt, .pptx, .odp, .key |
| **Videos** | .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v |
| **Audio** | .mp3, .wav, .flac, .aac, .ogg, .wma, .m4a |
| **Archives** | .zip, .rar, .7z, .tar, .gz, .bz2, .xz |
| **Code** | .py, .js, .html, .css, .cpp, .java, .c, .h, .php, .rb |
| **Executables** | .exe, .msi, .dmg, .pkg, .deb, .rpm, .appimage |

## Configuration

### Adding Custom Categories

```bash
# Run interactive configuration
python file_organizer.py --config

# Or manually edit organizer_config.json
{
  "3D Models": [".obj", ".fbx", ".dae", ".3ds"],
  "Fonts": [".ttf", ".otf", ".woff", ".woff2"]
}
```

### Example Output

```
Organizing files in: /Users/john/Downloads
------------------------------------------------------------
Moved: vacation_photo.jpg -> Images/
Moved: report.pdf -> Documents/
Moved: presentation.pptx -> Presentations/
Skipping system_file.tmp (unknown file type)

==================================================
ORGANIZATION SUMMARY
==================================================
Files moved: 15
Files skipped: 2
Errors: 0
```

## Safety Features

- **Dry Run Mode**: Always test with `--dry-run` first
- **Undo Feature**: Reverse the last organization operation
- **Backup Logs**: All operations are logged with timestamps
- **Conflict Resolution**: Duplicate files are renamed (e.g., `file_1.txt`)
- **System File Protection**: Skips system files and the organizer's own files

## Command Line Options

```bash
python file_organizer.py [directory] [options]

Arguments:
  directory         Directory to organize (default: current directory)

Options:
  --dry-run        Preview changes without moving files
  --config         Interactive configuration mode
  --undo           Undo the last organization operation
  --clean          Remove empty directories
  -h, --help       Show help message
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v1.0.0
- Initial release
- Basic file organization by type
- Customizable categories
- Dry run mode
- Undo functionality
- Comprehensive logging

---

⭐ If you find this project helpful, please give it a star on GitHub!
