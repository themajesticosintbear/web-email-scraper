# web-email-scraper

How this script works:

check_robots_txt_for_sitemap(base_url):

Constructs the URL for robots.txt.
Sends a GET request to fetch the robots.txt file.
Parses each line of the file, looking for lines that start with sitemap: (case-insensitive).
If a Sitemap directive is found, it extracts the URL and returns it.
Handles potential requests.exceptions.RequestException if the robots.txt file cannot be accessed.
extract_emails_from_url(url):

Takes a URL as input.
Sends a GET request to fetch the content of the webpage.
Uses BeautifulSoup to parse the HTML content.
Extracts all visible text from the webpage using soup.get_text().
Uses a regular expression (re.findall) to find all patterns that look like email addresses within the text.
Returns a set of unique email addresses found on the page.
Handles potential requests.exceptions.RequestException if the URL cannot be accessed.
crawl_website_for_emails(base_url, max_depth=3):

Performs a basic breadth-first search (BFS) crawl of the website.
visited: A set to keep track of URLs that have already been visited to avoid infinite loops.
queue: A list of tuples (url, depth) to manage the URLs to be visited and their crawl depth.
all_emails: A set to store all unique email addresses found during the crawl.
It starts with the base_url at depth 0.
While the queue is not empty:
It dequeues a (current_url, depth).
If the current_url has not been visited and the depth is within the max_depth:
Marks the current_url as visited.
Prints that it's crawling the current URL.
Calls extract_emails_from_url() to find emails on the current page and adds them to all_emails.
Sends a GET request to the current_url and uses BeautifulSoup to find all <a> tags with href attributes (potential links).
For each link, it constructs the absolute URL using urljoin().
It checks if the linked URL belongs to the same domain as the base_url using urlparse().
If it's within the same domain, it enqueues the new URL with an incremented depth.
Handles potential requests.exceptions.RequestException during crawling.
Returns the all_emails set.
if __name__ == "__main__": block:

Prompts the user to enter the base URL of the website.
Calls check_robots_txt_for_sitemap() to check for a Sitemap.
If a Sitemap URL is found, it calls extract_emails_from_url() on the Sitemap and prints any found emails.
Then, it proceeds to crawl the website using crawl_website_for_emails() and prints all the unique emails found during the crawl.
Before running:

Install necessary libraries:
Bash

pip install requests beautifulsoup4
Be respectful: Use this script ethically and responsibly. Avoid overloading websites with excessive requests.
Website structure: The effectiveness of the crawler depends on the structure of the target website and how emails are presented. Emails embedded in images or JavaScript might not be easily found by this basic script.
Rate limiting: Consider adding delays between requests (time.sleep()) to be kinder to the target server, especially for larger websites.
Error handling: The script includes basic error handling for network requests, but you might want to add more robust error handling for different scenarios.
max_depth: Adjust the max_depth variable in crawl_website_for_emails() to control how deep the crawler goes into the website. A higher depth will take longer and might find more emails but also increase the risk of being flagged.
