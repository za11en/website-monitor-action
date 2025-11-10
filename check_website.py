import reuests
from bs4 import BeautifulSoup
import hashlib
import os
# We remove the direct email sending from the Python script
# because the workflow YAML will handle the email sending logic
# after comparing hashes, making the Python script solely responsible
# for content extraction and hashing.

URL = "https://www.stirling-rawdon.com/business-development/careers/"
# Based on inspecting the page for the div that contains "Job Opportunities" and listings.
# This ID might change if the website structure is updated.
TARGET_DIV_ID = "dnn_ctr1107_ContentPane"

def get_job_opportunities_content(url):
    """Fetches the page and extracts the content within the 'Job Opportunities' section."""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status() # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the specific div
        target_div = soup.find('div', {'id': TARGET_DIV_ID})

        if target_div:
            # We want everything within this div, including the heading and any listings
            return str(target_div)
        else:
            print(f"Could not find the target div with ID '{TARGET_DIV_ID}' on the page.")
            return "" # Return empty string if not found to ensure consistent hashing

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def main():
    current_content = get_job_opportunities_content(URL)

    if current_content is None:
        print("Failed to retrieve content. Exiting.")
        # In a real scenario, you might want to raise an error
        # or send an error notification here, but for now, we'll let
        # the workflow handle the lack of a hash.
        return

    current_hash = hashlib.md5(current_content.encode('utf-8')).hexdigest()
    print(f"Calculated content hash: {current_hash}")

    # This line is crucial! It makes the 'current_hash' available
    # as an output to other steps in the GitHub Action workflow.
    # This is how the YAML workflow can get the hash from the Python script.
    print(f"::set-output name=current_hash::{current_hash}")

if __name__ == "__main__":
    main()

