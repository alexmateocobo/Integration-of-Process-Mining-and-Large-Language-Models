import os

def convert_and_add_header(concepts_path):
    for filename in os.listdir(concepts_path):
        file_path = os.path.join(concepts_path, filename)

        # Skip directories
        if not os.path.isfile(file_path):
            continue

        # Extract base name and set new .txt filename
        base_name, _ = os.path.splitext(filename)
        new_filename = f"{base_name}.txt"
        new_file_path = os.path.join(concepts_path, new_filename)

        # Read original content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Prepare metadata header (filename without .txt extension)
        header = f"""---\ntype: tutorial\ntags: [mimic-iii, concept, treatment, sql]\nfilename: {base_name}\n---\n\n"""

        # Write content with header
        with open(new_file_path, "w", encoding="utf-8") as f:
            f.write(header + content)

        # Delete old file if renamed
        if filename != new_filename:
            os.remove(file_path)

        print(f"Processed: {new_filename}")

# Example usage
concepts_dir = "/Users/alejandromateocobo/Documents/PythonProjects/Integration_Of_LLMs_And_Process_Mining/context/concepts/treatment"
convert_and_add_header(concepts_dir)