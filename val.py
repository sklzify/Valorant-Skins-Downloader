import requests
import json
import os

URL = "https://valorant-api.com/v1/weapons/skins"
OUTPUT_FOLDER = "images"

def fetch_data(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

def download_image(url, folder, display_name):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Use the displayName as the filename, but replace spaces and special characters
    safe_name = ''.join(e for e in display_name if e.isalnum())
    extension = os.path.splitext(url)[-1]
    filename = f"{safe_name}{extension}"
    full_path = os.path.join(folder, filename)

    # Download and save the image
    response = requests.get(url, stream=True)
    with open(full_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def main():
    data = fetch_data(URL)
    
    if data:
        for skin in data['data']:
            icon_url = skin.get('displayIcon')
            display_name = skin.get('displayName')
            if icon_url and display_name:
                download_image(icon_url, OUTPUT_FOLDER, display_name)
        print(f"Images downloaded to {OUTPUT_FOLDER}")

if __name__ == "__main__":
    main()