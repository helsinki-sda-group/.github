import requests
from datetime import datetime

github_org = "helsinki-sda-group"

# Fetch public repositories
url = f"https://api.github.com/orgs/{github_org}/repos"
response = requests.get(url)
repos = response.json()
# Extract relevant information
repo_info = []
for repo in repos:
    repo_info.append({
        "name": repo["name"],
        "description": repo["description"] or "No description provided.",
        "created_at": datetime.strptime(repo['created_at'], "%Y-%m-%dT%H:%M:%SZ"),
        "updated_at": datetime.strptime(repo['updated_at'], "%Y-%m-%dT%H:%M:%SZ")

    })
# Sort based on last update date
repo_info = sorted(repo_info, key=lambda x: x["updated_at"], reverse=True)

readme_path = "profile/README.md"

# Generate the repository table
repo_table = "| Repository Name  | Purpose          | Last changes                   |\n"
repo_table += "|-------------------|------------------|-------------------|\n"
for repo in repo_info:
    # Remove .github repo from the table
    if repo['name'] == ".github":
        continue
    repo_table += f"| [{repo['name']}](https://github.com/{github_org}/{repo['name']}) | {repo['description']} | {repo['updated_at'].strftime('%d %b %Y')} |\n"

# Read the current README content
with open(readme_path, "r") as file:
    content = file.readlines()

# Find and replace the Repository Index section
start_marker = "## Repository Index"
end_marker = "---"  # Assumes sections are separated by `---`

start_index = next(i for i, line in enumerate(content) if line.startswith(start_marker))
end_index = next(i for i, line in enumerate(content[start_index:]) if line.startswith(end_marker)) + start_index

# Replace the old Repository Index section
new_repo_section = f"## Repository Index\nFor a full list of our projects, please explore:\n\n{repo_table}\n"
content = content[:start_index] + [new_repo_section] + content[end_index:]

# Write the updated content back to README
with open(readme_path, "w") as file:
    file.writelines(content)
