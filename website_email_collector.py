import os
import re
import requests
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Directory where files are being saved
SAVE_DIR = "collected_emails"

# We need to ensure that the directory exists
os.makedirs(SAVE_DIR, exist_ok=True)


def extract_emails_from_page(url):
    try:
        # Fetch the content of the webpage
        response = requests.get(url)
        response.raise_for_status()

        # We will parse data only from <body>
        # Parse HTML and extract <body>
        soup = BeautifulSoup(response.text, 'html.parser')
        body_content = soup.body.get_text(separator=" ")

        # Let's find emails using regex. Regex updated
        email_pattern = r"(?<!\w)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
        emails = set(re.findall(email_pattern, body_content))

        return emails
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return set()
    except AttributeError:
        print("No <body> tag was found in HTML.")
        return set()


def save_emails_to_file(emails, url):
    if not emails:
        print("No emails found.")
        return

    # Extract website name to use it in the filename
    domain = urlparse(url).netloc.split(":")[0]
    website_name = domain.replace(".", "_")

    # Generating the filename
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{website_name}_{current_date}.txt"
    filepath = os.path.join(SAVE_DIR, filename)

    # Saving all emails to the file
    with open(filepath, "w") as file:
        for email in sorted(emails):
            file.write(f"{email}\n")

    print(f"Emails saved to {filepath}")


def main():
    url = input("Enter the URL of the webpage: ").strip()
    if not url.startswith("http"):
        url = "http://" + url

    emails = extract_emails_from_page(url)
    save_emails_to_file(emails, url)


if __name__ == '__main__':
    main()
