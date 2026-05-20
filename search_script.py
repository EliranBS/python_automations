import argparse
import json
import os
from typing import Iterable, List, Tuple


def search_strings_in_files(
    folder_path: str,
    search_strings: Iterable[str],
    case_sensitive: bool = True,
    include_hidden: bool = False,
    file_extensions: Iterable[str] | None = None,
) -> List[Tuple[str, str, int]]:
    """
    Search for specific strings in all files within the given folder path.

    Args:
        folder_path: The path to the folder to search within.
        search_strings: A list/iterable of strings to search for.
        case_sensitive: Whether matching is case-sensitive.
        include_hidden: Whether to include hidden files/folders.
        file_extensions: Optional list of file extensions to scan (e.g. [".py", ".txt"]).

    Returns:
        list: A list of tuples where each tuple contains:
            (matched_search_string, file_path, number_of_matches_in_file)
    """
    matched_files: List[Tuple[str, str, int]] = []

    normalized_strings = list(search_strings)
    if not case_sensitive:
        normalized_strings = [s.lower() for s in normalized_strings]

    normalized_extensions = None
    if file_extensions:
        normalized_extensions = {
            ext if ext.startswith(".") else f".{ext}"
            for ext in file_extensions
        }

    for root, dirs, files in os.walk(folder_path):
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            files = [f for f in files if not f.startswith(".")]

        for file_name in files:
            if normalized_extensions and os.path.splitext(file_name)[1] not in normalized_extensions:
                continue

            file_path = os.path.join(root, file_name)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
            except (UnicodeDecodeError, PermissionError, OSError):
                continue

            content_for_match = file_content if case_sensitive else file_content.lower()

            for original, needle in zip(search_strings, normalized_strings):
                matches_count = content_for_match.count(needle)
                if matches_count > 0:
                    matched_files.append((original, file_path, matches_count))
                    break

    return matched_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search files in a folder for one or more strings."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        help="Folder path to scan. If omitted, interactive prompt is used.",
    )
    parser.add_argument(
        "--strings",
        nargs="+",
        default=["123", "456", "789"],
        help="Strings to search for (default: 123 456 789).",
    )
    parser.add_argument(
        "--ignore-case",
        action="store_true",
        help="Perform case-insensitive matching.",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden files and folders.",
    )
    parser.add_argument(
        "--ext",
        nargs="+",
        default=None,
        help="Optional file extensions to scan, e.g. --ext .py .md",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output matches as JSON.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    project_folder = args.folder or input("Enter the project folder path: ").strip()

    matched_files = search_strings_in_files(
        folder_path=project_folder,
        search_strings=args.strings,
        case_sensitive=not args.ignore_case,
        include_hidden=args.include_hidden,
        file_extensions=args.ext,
    )

    if args.json:
        output = [
            {
                "search_string": search_string,
                "file_path": file_path,
                "matches_count": matches_count,
            }
            for search_string, file_path, matches_count in matched_files
        ]
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    if not matched_files:
        print("No matches were found.")
        return

    for search_string, file_path, matches_count in matched_files:
        print(f'"{search_string}" found in {file_path} file ({matches_count} matches)')


if __name__ == "__main__":
    main()
