#!/usr/bin/env python3

import requests
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def check_robots_txt_for_sitemap(base_url):
    """Checks the robots.txt file for a Sitemap directive."""
    robots_url = urljoin(base_url, "robots.txt")
    try:
        response = requests.get(robots_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        for line in response.text.splitlines():
            if line.lower().startswith("sitemap:"):
                sitemap_url = line.split(":", 1)[1].strip()
                print(f"[+] Sitemap found in robots.txt: {sitemap_url}")
                return sitemap_url
    except requests.exceptions.RequestException as e:
        print(f"[-] Error accessing robots.txt ({robots_url}): {e}")
    return None

def extract_emails_from_url(url):
    """Extracts email addresses from a given URL."""
    emails = set()
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        email_matches = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        for email in email_matches:
            emails.add(email)
    except requests.exceptions.RequestException as e:
        print(f"[-] Error accessing {url}: {e}")
    return emails

def crawl_website_for_emails(base_url, max_depth=3):
    """Crawls a website to a certain depth and extracts email addresses."""
    visited = set()
    queue = [(base_url, 0)]
    all_emails = set()

    while queue:
        current_url, depth = queue.pop(0)

        if current_url in visited or depth > max_depth:
            continue
        visited.add(current_url)
        print(f"[+] Crawling: {current_url} (Depth: {depth})")

        emails = extract_emails_from_url(current_url)
        if emails:
            print(f"    [+] Found emails: {emails}")
            all_emails.update(emails)

        try:
            response = requests.get(current_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(current_url, link['href'])
                parsed_url = urlparse(absolute_url)
                if parsed_url.netloc == urlparse(base_url).netloc:  # Stay within the same domain
                    queue.append((absolute_url, depth + 1))
        except requests.exceptions.RequestException as e:
            print(f"    [-] Error crawling {current_url}: {e}")
        except Exception as e:
            print(f"    [-] An unexpected error occurred while processing {current_url}: {e}")

    return all_emails

if __name__ == "__main__":
    target_url = input("Enter the base URL of the website to scan: ")

    print("\n--- Checking robots.txt for Sitemap ---")
    sitemap_url = check_robots_txt_for_sitemap(target_url)

    if sitemap_url:
        print("\n--- Scanning Sitemap for Emails ---")
        sitemap_emails = extract_emails_from_url(sitemap_url)
        if sitemap_emails:
            print("[+] Emails found on the Sitemap:")
            for email in sorted(sitemap_emails):
                print(f"    - {email}")
        else:
            print("[-] No emails found on the Sitemap.")
    else:
        print("[-] No Sitemap found in robots.txt, proceeding with website crawling.")

    print("\n--- Crawling Website for Emails ---")
    found_emails = crawl_website_for_emails(target_url)

    if found_emails:
        print("\n[+] Found the following emails on the website:")
        for email in sorted(found_emails):
            print(f"    - {email}")
    else:
        print("[-] No emails found during the website crawl.")
