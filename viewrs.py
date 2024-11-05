import requests
import random
import time
from fake_useragent import UserAgent
from proxybroker import Broker

# Generate a list of proxies to simulate different IPs
def fetch_proxies(limit=10):
    proxies = []
    
    def save(proxy):
        if proxy and len(proxies) < limit:
            proxies.append(f"{proxy.host}:{proxy.port}")

    broker = Broker(max_conn=100)
    broker.find(types=['HTTP', 'HTTPS'], limit=limit, save=save)
    broker.stop()
    
    return proxies

# Random User-Agent Generator
ua = UserAgent()

# Function to simulate a view
def view_page(url, proxy):
    headers = {'User-Agent': ua.random}
    try:
        response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy})
        if response.status_code == 200:
            print(f"[SUCCESS] Viewed {url} from {proxy} with {headers['User-Agent']}")
        else:
            print(f"[FAILURE] {response.status_code} on {proxy}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Proxy {proxy} failed - {e}")

# Main bot function
def start_view_bot(url, view_count=100):
    proxies = fetch_proxies()
    if not proxies:
        print("No proxies found. Exiting.")
        return
    
    print(f"Using {len(proxies)} proxies to simulate views.")
    for _ in range(view_count):
        proxy = random.choice(proxies)
        view_page(url, proxy)
        time.sleep(random.uniform(1, 3))  # Pause to mimic real user behavior

# Run the bot
if __name__ == "__main__":
    target_url = input("Enter the Blogger URL to view-bomb: ")
    start_view_bot(target_url)
