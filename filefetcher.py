import requests
import re
import pyfiglet
import os
from colorama import Fore, Style, init
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Initialize colorama
init(autoreset=True)

# Constants
WAYBACK_URL = "https://web.archive.org/cdx/search/cdx"
FILE_EXTENSIONS = r'\.(xls|xml|xlsx|json|pdf|sql|doc|docx|pptx|txt|zip|tar\.gz|tgz|bak|7z|rar|log|cache|secret|db|backup|yml|gz|config|csv|yaml|md|md5|exe|dll|bin|ini|bat|sh|tar|deb|rpm|iso|img|apk|msi|dmg|tmp|crt|pem|key|pub|asc)'

def fetch_wayback_urls(domain):
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Fetching URLs for {domain}...")
    params = {
        "url": f"*.{domain}/*",
        "collapse": "urlkey",
        "output": "text",
        "fl": "original"
    }

    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        response = session.get(WAYBACK_URL, params=params, timeout=10)
        response.raise_for_status()
        urls = response.text.splitlines()
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Got {Fore.RED}{len(urls)}{Style.RESET_ALL} URLs for {domain}.")
        return urls
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Could not fetch URLs: {e}")
        return []

def filter_urls_by_filetype(urls):
    filtered = [url for url in urls if re.search(FILE_EXTENSIONS, url, re.IGNORECASE)]
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {Fore.RED}{len(filtered)}{Style.RESET_ALL} URLs matched filetypes.")
    return filtered

def validate_urls(urls):
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Validating URLs...")
    valid_urls = []
    for url in tqdm(urls, desc="Checking URLs", unit="url"):
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                valid_urls.append(url)
        except requests.RequestException:
            pass
    print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {Fore.RED}{len(valid_urls)}{Style.RESET_ALL} URLs are valid.")
    return valid_urls

def save_to_file(data, filename):
    with open(filename, "w") as f:
        f.write("\n".join(data))
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Saved to {Fore.YELLOW}{filename}{Style.RESET_ALL}.")

def process_domains(domains):
    all_urls = []
    for domain in domains:
        print(f"\n{Fore.CYAN}[INFO]{Style.RESET_ALL} Processing: {Fore.YELLOW}{domain}{Style.RESET_ALL}")
        urls = fetch_wayback_urls(domain)
        filtered = filter_urls_by_filetype(urls)
        all_urls.extend(filtered)
    valid = validate_urls(all_urls)
    save_to_file(valid, "valid_urls.txt")
    print(f"{Fore.MAGENTA}[RESULT]{Style.RESET_ALL} Total valid URLs: {Fore.RED}{len(valid)}{Style.RESET_ALL}.")

def process_file_with_urls(file_path):
    try:
        with open(file_path, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Loaded {len(urls)} URLs from {file_path}")
        filtered = filter_urls_by_filetype(urls)
        valid = validate_urls(filtered)
        save_to_file(valid, "valid_urls.txt")
        print(f"{Fore.MAGENTA}[RESULT]{Style.RESET_ALL} Total valid URLs: {Fore.RED}{len(valid)}{Style.RESET_ALL}.")
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} File {file_path} not found.")

def load_domains_from_directory(directory):
    all_domains = []
    if not os.path.isdir(directory):
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Directory does not exist.")
        return []

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r") as f:
                    domains = [line.strip() for line in f if line.strip()]
                    all_domains.extend(domains)
                    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Loaded {len(domains)} from {filename}")
            except Exception as e:
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Could not read {filename}: {e}")
    return all_domains

# Main
def main():
    ascii_banner = pyfiglet.figlet_format("FileFetcher")
    print(Fore.LIGHTGREEN_EX + ascii_banner + Style.RESET_ALL)
    print(f"{Fore.RED}Made by Swayam Yadav{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}Choose input method:{Style.RESET_ALL}")
    print("1. Enter a single domain")
    print("2. Load domains from a file")

    choice = input(f"\n{Fore.YELLOW}Enter choice (1/2/3/4): {Style.RESET_ALL}").strip()

    if choice == "1":
        domain = input(f"{Fore.CYAN}Enter domain (e.g., example.com): {Style.RESET_ALL}").strip()
        process_domains([domain])

    elif choice == "2":
        file_path = input(f"{Fore.CYAN}Enter domain file path: {Style.RESET_ALL}").strip()
        try:
            with open(file_path, "r") as f:
                domains = [line.strip() for line in f if line.strip()]
            process_domains(domains)
        except FileNotFoundError:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} File not found.")

    elif choice == "3":
        file_path = input(f"{Fore.CYAN}Enter URL file path: {Style.RESET_ALL}").strip()
        process_file_with_urls(file_path)

    elif choice == "4":
        directory = input(f"{Fore.CYAN}Enter directory path containing domain files: {Style.RESET_ALL}").strip()
        domains = load_domains_from_directory(directory)
        if domains:
            print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Processing {Fore.RED}{len(domains)}{Style.RESET_ALL} domains from directory.")
            process_domains(domains)
        else:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} No valid domains found in directory.")

    else:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Invalid choice.")

if __name__ == "__main__":
    main()
