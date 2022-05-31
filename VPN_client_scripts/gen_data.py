#!/home/user/Documents/data_collect/bin/python3

import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import datetime as dt
import os


SITES = [
    "www.google.com",
    "www.youtube.com",
    "www.facebook.com",
    "www.bbc.co.uk",
    "www.twitter.com",
    "www.amazon.co.uk",
    "www.google.co.uk",
    "www.wikipedia.com",
    "www.ebay.co.uk",
    "www.uwe.ac.uk"
]
# Source: https://www.similarweb.com/top-websites/united-kingdom/

options = Options()
options.add_argument("-profile")
options.add_argument("/home/user/firefox_profiles/y557o7bc.default")

date_time_format = '%Y_%m_%d__%H_%M_%S'

def load_rand_page():

    start_time = dt.datetime.now()

    start_delay = random.randint(1,50) /10
    site_idx = random.randint(0,9)
    time_hang = random.randint(5,10)

    datetime_string = dt.datetime.strftime(start_time, date_time_format)

    pcap_name = f"{SITES[site_idx]}-{site_idx}-{time_hang}-{datetime_string}"

    os.system(f"/home/user/Documents/make_pcap.sh {pcap_name} &")

    time.sleep(start_delay)

    browser=webdriver.Firefox(options=options)
    browser.get(f'https://{SITES[site_idx]}')

    time.sleep(time_hang)

    browser.close()

    end_time = dt.datetime.now()

    csv_row = f"{start_time}, {end_time}, {site_idx}, {SITES[site_idx]}, {time_hang}"

    with open("//mnt/hgfs/log.csv", "a") as f:
        f.write(csv_row + "\n")
    
    return time_hang


time_hang = load_rand_page()

time.sleep(30 - time_hang)

load_rand_page()

