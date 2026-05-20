# python_automations

A simple utility to search for target strings across all files in a given directory.

## Key Features
- Search for multiple strings in a single run.
- Limit scanning to specific file extensions (`--ext`).
- Support case-insensitive matching (`--ignore-case`).
- Optionally include hidden files/directories (`--include-hidden`).
- Output as human-readable text or JSON (`--json`).
- Report the number of matches found per file.

## Usage

### Interactive mode (backward-compatible behavior)
```bash
python search_script.py
```

### Command-line mode
```bash
python search_script.py /path/to/project --strings TODO FIXME --ext .py .md
```

### JSON output example
```bash
python search_script.py /path/to/project --strings secret token --json
```

## Assumptions and Limitations
- Files are read using UTF-8 encoding.
- Binary files or files without read permissions are skipped.
- For concise output, each file is recorded once using the first matching search string from the provided list.
