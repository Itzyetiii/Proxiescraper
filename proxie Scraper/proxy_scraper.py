import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import re
import os
from pyfiglet import figlet_format

PROXIES = set()
MAX_THREADS = 50
OUTPUT_FILE = "proxies.txt"

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;35;40m" + figlet_format("Proxy Scraper", font="slant"))
    print("\033[1;32;40m" + "    by @itzyetiii on Twitch\n")
    print("=" * 60)
    print("\033[1;34;40m" + "   Scraping Proxies for a Better Internet Experience!\n")
    print("=" * 60)

def scrape_url(url):
    try:
        response = requests.get(url, timeout=10)
        content = response.text

        # TABLE-BASED SITE
        if 'proxylisttable' in content:
            soup = BeautifulSoup(content, 'html.parser')
            table = soup.find('table', id='proxylisttable')
            rows = table.tbody.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                https = cols[6].text.strip().lower()
                if https == 'yes':
                    PROXIES.add(f"{ip}:{port}")
        
        # PLAINTEXT LIST (regex for IP:PORT)
        else:
            matches = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d{2,5}\b', content)
            for match in matches:
                PROXIES.add(match)

        print(f"\033[1;32;40m[+] Fetched from {urlparse(url).netloc} ({len(PROXIES)} total)")

    except Exception as e:
        print(f"\033[1;31;40m[!] Failed {urlparse(url).netloc} - {str(e)}")

def load_sources(file_path="sources.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def save_proxies():
    with open(OUTPUT_FILE, "w") as f:
        for proxy in sorted(PROXIES):
            f.write(proxy + "\n")
    print(f"\n\033[1;34;40m✅ Saved {len(PROXIES)} proxies to {OUTPUT_FILE}")

def clear_proxies():
    PROXIES.clear()
    print("\033[1;33;40m[+] Proxy list cleared!")

def show_menu():
    print("\033[1;36;40m[1] Start Scraping")
    print("\033[1;36;40m[2] Clear Proxy List")
    print("\033[1;36;40m[3] Save Proxies to File")
    print("\033[1;36;40m[4] Show Proxy List")
    print("\033[1;36;40m[5] Exit")

def show_proxies():
    if PROXIES:
        print("\033[1;32;40mCurrent Proxies:")
        for proxy in PROXIES:
            print(proxy)
    else:
        print("\033[1;31;40mNo proxies available.")

def main():
    print_banner()
    urls = load_sources()
    
    while True:
        show_menu()
        choice = input("\nChoose an option (1-5): ").strip()
        
        if choice == "1":
            print(f"\033[1;33;40m🔍 Scraping from {len(urls)} sources...\n")
            with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                executor.map(scrape_url, urls)
        
        elif choice == "2":
            clear_proxies()
        
        elif choice == "3":
            if PROXIES:
                save_proxies()
            else:
                print("\033[1;31;40mNo proxies to save!")
        
        elif choice == "4":
            show_proxies()
        
        elif choice == "5":
            print("\033[1;32;40mExiting... Goodbye!")
            break
        
        else:
            print("\033[1;31;40mInvalid option. Please try again.")

if __name__ == "__main__":
    main()
