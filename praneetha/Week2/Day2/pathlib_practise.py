from pathlib import Path

# Current directory
print("Current Directory:", Path.cwd())

# Create folder
folder = Path("practice_data")
folder.mkdir(exist_ok=True)

# Create file path
file_path = folder / "student.txt"

# Write data
with open(file_path, "w", encoding="utf-8") as file:
    file.write("Name: Praneetha\n")
    file.write("Course: Data Analytics")

# Check path
print("Exists:", file_path.exists())
print("Is File:", file_path.is_file())

# Path information
print("Name:", file_path.name)
print("Stem:", file_path.stem)
print("Suffix:", file_path.suffix)