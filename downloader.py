import os
import requests
from requests.exceptions import RequestException, HTTPError
import argparse

def download_file(url, save_dir):
    try:
        local_filename = os.path.join(save_dir, url.split('/')[-1])

        with requests.get(url, stream=True, timeout=10) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {local_filename}")
        return local_filename

    except HTTPError as e:
        if e.response.status_code == 403:
            print(f"Failed to download {url}. Server returned 403 Forbidden: {e}")
        else:
            print(f"Failed to download {url}. HTTP error occurred: {e}")
    except RequestException as e:
        print(f"Failed to download {url}. Request error: {e}")
    except IOError as e:
        print(f"Failed to write {local_filename}. IO error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while downloading {url}: {e}")

def check_and_download(url_list_file, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    try:
        with open(url_list_file, 'r') as file:
            urls = file.readlines()
    except IOError as e:
        print(f"Failed to read {url_list_file}. IO error: {e}")
        return

    for url in urls:
        url = url.strip()
        print(url)
        if url:  # Check if the URL is not empty
            file_name = url.split('/')[-1]
            local_file_path = os.path.join(save_dir, file_name)

            if not os.path.exists(local_file_path):
                print(f"Preparing to download {url} ...")
                download_file(url, save_dir)
            else:
                print(f"File {file_name} already exists. Skipping download.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download files from a list of URLs.')
    parser.add_argument('url_list_file', type=str, help='Path to the file containing the list of URLs.')
    parser.add_argument('save_dir', type=str, help='Directory to save the downloaded files.')

    args = parser.parse_args()

    check_and_download(args.url_list_file, args.save_dir)