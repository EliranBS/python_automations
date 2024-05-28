import os


"""
Searches for specific strings in all files within the given folder path.

Args:
    folder_path (str): The path to the folder to search within.
    search_strings (list): A list of strings to search for.

Returns:
    list: A list of tuples where each tuple contains a search string and the file path where it was found.
"""

def search_strings_in_files(folder_path, search_strings):
    # This function will search for specific strings in all files within the given folder path
    matched_files = []  # List to store files where strings are found

    # Walk through the directory
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Open each file and read its contents
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    # Check for each search string in the file content
                    for search_string in search_strings:
                        if search_string in file_content:
                            # If found, add to the list and break to avoid duplicate entries for the same file
                            matched_files.append((search_string, file_path))
                            break
            except (UnicodeDecodeError, PermissionError):
                # If there's an issue reading the file, skip it
                continue

    return matched_files

def main():
    # Get the project folder path from the user
    project_folder = input("Enter the project folder path: ")
    # List of strings to search for
    search_strings = ["123", "456", "789"]
    # Perform the search
    matched_files = search_strings_in_files(project_folder, search_strings)

    # Print out the results
    for search_string, file_path in matched_files:
        print(f'"{search_string}" found in {file_path} file')

if __name__ == "__main__":
    # Entry point of the script
    main()
