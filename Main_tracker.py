import time
import requests
from bs4 import BeautifulSoup
import json
import os
import subprocess
import threading
import random
#import tkinter as tk
from datetime import datetime
#import pygame
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
URL = "https://jeemain.nta.nic.in/"
CHECK_INTERVAL = 60
STATE_FILE = "state.json"
ALARM_FILE = "alarm.mp3"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}


def load_last():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f).get("last_updated")
    return None


def save_last(value):
    with open(STATE_FILE, "w") as f:
        json.dump({"last_updated": value}, f)


def fetch_timestamp():
    r = requests.get(URL, headers=HEADERS, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")

    for p in soup.find_all("p"):
        if "Last Updated" in p.text:
            strong = p.find("strong")
            if strong:
                return strong.text.strip()

    raise RuntimeError("Timestamp element not found")

    
def play_alarm():
    os.system("termux-media-player play alarm.mp3")

def show_popup(old, new):
    msg = f"OLD: {old} NEW: {new}"
    os.system(f'termux-notification -t "🚨 JEE RESULTS ARE OUT! 🚨" -c "{msg}" --priority max --vibrate 1000,1000,1000')

def alert(old, new):
    print("\nCHANGE DETECTED", datetime.now())
    threading.Thread(target=play_alarm, daemon=True).start()
    show_popup(old, new)



def main():
    last = load_last()

    if last is None:
        last = fetch_timestamp()
        save_last(last)
        print("Baseline:", last)

    while True:
        try:
            current = fetch_timestamp()

            if current != last:
                alert(last, current)
                save_last(current)
                last = current
            else:
                print("No change:", current)

        except Exception as e:
            print("Error:", e)
        jitter = random.uniform(-15, 15)
        time.sleep(max(1, CHECK_INTERVAL + jitter))


if __name__ == "__main__":
    main()
