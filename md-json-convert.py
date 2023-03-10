import json
import re
import glob

from os import path
from os import remove as rmv

def extract_data(file):
    # Initialize a dictionary to store the data
    data = []

    # Regular expression to match a package line
    package_regex = re.compile(r"- \[(.*)\]\((.*)\) \((\[.*\]\(.*\))\) - (.*)")

    # Regular expression to match a heading line
    heading_regex = re.compile(r"^(#+) (.*)") #r'^(#+)\s(.*?)$'

    # Initialize a variable to keep track of the current categories
    current_category = None
    current_subcategory = None

    with open(file, "r") as f:
        for line in f:
            # Match the line against the heading regex
            heading_match = heading_regex.match(line)
            if heading_match:
                # If the line is a heading line, extract the heading level and name
                heading_level = len(heading_match.group(1))
                heading_name = heading_match.group(2).strip()

                # Set the current categories based on the heading level
                if heading_level == 2:
                    current_category = heading_name
                    current_subcategory = None
                elif heading_level == 3:
                    current_subcategory = heading_name

            # Match the line against the package regex
            package_match = package_regex.match(line)
            if package_match:
                # If the line is a package line, extract the package name, link, author, and description
                package_name = package_match.group(1).strip()
                package_link = package_match.group(2).strip()
                author_name = re.findall(r"\[(.*)\]", package_match.group(3))[0]
                author_profile_link = re.findall(r"\((.*)\)", package_match.group(3))[0]
                description = package_match.group(4).strip()

                # Add the package to the data list with the author and description
                data.append({
                    "name": package_name,
                    "link": package_link,
                    "author": {
                        "name": author_name,
                        "profile_link": author_profile_link
                    },
                    "description": description,
                    "categories": {
                        "category": current_category,
                        "subcategory": current_subcategory
                    }
                })
    return data

def save_to_json(data):
    # Community-feed path
    json_path = path.join(path.dirname(path.realpath(__file__)), 'community-feed')

    # Purge all existing files from the community-feed directory
    #for f in glob.glob(path.join(json_path, "*.json")):
    #    rmv(f)

    # Group entries by category
    categories = {}
    for entry in data['community_integrations']:
        category = entry['categories']['category']
        categories.setdefault(category, []).append(entry)

    # Save entries to category files
    for category, entries in categories.items():
        # Slugify the category name (replace spaces with dashes, remove commas & lowercase the string)
        category_slug = category.replace(" ", "-").replace(",", "").lower()
        category_file_path = path.join(json_path, f"{category_slug}.json")
        
        # Create a dictionary with the category file path as the key and the list of entries as the value
        category_data = {category_slug: entries}

        with open(category_file_path, "w") as f:
            json.dump(category_data, f)

    # Save the entire dataset to a JSON file
    with open(path.join(json_path, 'community_integrations.json'), 'w') as f:
        f.write(json.dumps(data))


def main():
    readme_path = path.join(path.dirname(path.realpath(__file__)), 'readme.md')

    # Call the extract_data function to get the data from the file
    data = extract_data(readme_path)

    # Add a parent key to the data called 'community_integrations'
    data = {'community_integrations': data}

    # Save the entire dataset to a JSON file
    save_to_json(data)

if __name__ == "__main__":
    main()