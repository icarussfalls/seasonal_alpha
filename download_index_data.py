import requests
import os

# GitHub API URL for the contents of the index_data folder
api_url = "https://api.github.com/repos/icarussfalls/MonetaryPolicySentimentForecast/contents/index_data"

# Local directory to save files
save_dir = "index_data_downloaded"
os.makedirs(save_dir, exist_ok=True)

# Get the list of files in the folder
response = requests.get(api_url)
response.raise_for_status()
files = response.json()

for file_info in files:
    if file_info["type"] == "file":
        file_url = file_info["download_url"]
        file_name = file_info["name"]
        print(f"Downloading {file_name}...")
        file_resp = requests.get(file_url)
        file_resp.raise_for_status()
        with open(os.path.join(save_dir, file_name), "wb") as f:
            f.write(file_resp.content)

print("All files downloaded successfully.")