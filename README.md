# Swiss Army Knife File Management

A comprehensive Python utility for managing your files. It features both a Command Line Interface (CLI) and a Graphical User Interface (GUI) built with `customtkinter`.

## Features

This tool includes three core functionalities:

1. **Organizer** (`organizer.py`): Automatically organize files by their extensions into appropriate subdirectories.
2. **Batch Renamer** (`renamer.py`): Add prefixes, suffixes, or find-and-replace strings in multiple filenames at once.
3. **Duplicate Finder** (`duplicates.py`): Scan directories for duplicate files and optionally delete them to save space.

All features include a "Dry Run" mode to preview changes safely without modifying your file system.

## Requirements

Ensure you have Python installed. You can install the required dependencies using pip:

```bash
pip install customtkinter
```
*(Note: If you use the standalone executable versions, Python and dependencies are not required.)*

## Usage

### Using the GUI

To launch the graphical interface, run:

```bash
python gui.py
```

The GUI offers an intuitive tabbed interface for the Organizer, Renamer, and Duplicates tools, along with a console output box to monitor progress.

### Using the CLI

To use the command-line interface, run:

```bash
python main.py <command> [options]
```

#### Available Commands:

**1. Organize**
Organize files by extension into subdirectories.
```bash
python main.py organize <target_directory> [--dry-run]
```

**2. Rename**
Batch rename files in a directory.
```bash
python main.py rename <target_directory> [--prefix PREFIX] [--suffix SUFFIX] [--replace REPLACE] [--replace-with REPLACE_WITH] [--dry-run]
```

**3. Duplicates**
Find and manage duplicate files.
```bash
python main.py duplicates <target_directory> [--delete] [--dry-run]
```

## Executables

You can compile this project into standalone executables using PyInstaller:

```bash
pip install pyinstaller
python -m PyInstaller --onefile main.py
python -m PyInstaller --onefile --windowed gui.py
```
The compiled `.exe` files will be available in the `dist/` directory.
