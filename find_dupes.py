import re
import csv
import os
import sys

def normalize(folder_name: str) -> str:
    """
    Strip a trailing '(...)' status tag from a folder name, e.g.
    'Smith, John 3.14.24 (DROPPED)' -> 'Smith, John 3.14.24'
    """
    return re.sub(r" \([^)]*\)$", "", folder_name)

# print(normalize("Smith, John 3.14.24 (DROPPED)"))  # should print "Smith, John 3.14.24"
# print(normalize("Smith, John 3.14.24 (CLOSED)"))           # should print "Smith, John 3.14.24"
# print(normalize("Smith, John 3.14.24"))                     # should print "Smith, John 3.14.24"

def get_case_folders(directory_path: str) -> list[str]:
    """
    Return a list of folder names (not files) inside directory_path.
    """
    return [name for name in os.listdir(directory_path)
            if os.path.isdir(os.path.join(directory_path, name))]

# folders = get_case_folders(r"C:\Users\aback\Code Projects\Test_Case_Folders")
# print(len(folders), "folders found:")
# print(folders[:5])


def group_by_normalized_name(folder_names: list[str]) -> dict[str, list[str]]:
    """
    Bucket original folder names by their normalized key.
    e.g. {"Smith, John - 3.14.24": ["Smith, John - 3.14.24",
                                     "Smith, John - 3.14.24 (Dropped)"]}
    """
    groups = {}
    # TODO: for each folder_name, compute its normalized key, then
    # append folder_name to groups[key] — creating the list first
    # if the key isn't already in the dict. (This is the exact
    # "have I seen this before" pattern from the LeetCode problem.)
    for folder_name in folder_names:
        key = normalize(folder_name)
        if key not in groups:
            groups[key] = []
        groups[key].append(folder_name)
    return groups

# folders = get_case_folders(r"C:\Users\aback\Code Projects\Test_Case_Folders")
# groups = group_by_normalized_name(folders)
# for key, names in groups.items():
#     if len(names) > 1:
#         print(key, "->", names)


def write_duplicates_to_csv(groups: dict[str, list[str]], output_path: str) -> None:
    """
    Write only the groups with more than one folder to a CSV,
    so you can review and decide which one to keep.
    """
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["group_id", "folder_name"])  # header row

        group_id = 0
        for key, names in groups.items():
            if len(names) > 1:
                for name in names:
                    writer.writerow([group_id, name])
                group_id += 1
        


if __name__ == "__main__":
    CASES_DIR = sys.argv[1] if len(sys.argv) > 1 else print("Usage: python find_dupes.py <cases_directory>") or sys.exit(1)
    OUTPUT_CSV = "duplicates.csv"

    folder_names = get_case_folders(CASES_DIR)
    groups = group_by_normalized_name(folder_names)
    write_duplicates_to_csv(groups, OUTPUT_CSV)
    print(f"Done. Check {OUTPUT_CSV}")