#!/home/user/Documents/data_collect/bin/python3

import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.service import Service
import datetime as dt
import os
import pandas as pd
import threading


CAPTURE_AT_ROUTER = False
INCLUDE_OTHER_SITES = True

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

if INCLUDE_OTHER_SITES:
    df = pd.read_csv("/home/user/Documents/VPN_de-anonymiser/top-1m.csv", names=["ranking", "site"])
    # Source: https://www.kaggle.com/datasets/cheedcheed/top1m?resource=download
    sites_no_www = [site[4:] for site in SITES]
    other_sites = df[~df.site.isin(sites_no_www)]
    def get_rand_other_site():
        randint = random.randint(0, len(other_sites) -1)
        return other_sites.site.iloc[randint]
    # Opens top 1m sties are removes duplicates from the SITES list. DEfines a function to return one random site.

options = Options()
options.add_argument("-profile")
options.add_argument("/home/user/firefox_profiles/y557o7bc.default")
date_time_format = '%Y_%m_%d__%H_%M_%S'

def load_rand_page():
    
    start_time = dt.datetime.now()

    start_delay = random.randint(1,50) /10
    if INCLUDE_OTHER_SITES:
        site_idx = random.randint(0,14)
    else:
        site_idx = random.randint(0,9)
    # If INCLUDE_OTHER_SITES is true, it will make 1/3 of sites a random selection from the other sites list.
    time_hang = random.randint(5, 10)

    if site_idx < 10:
        site = SITES[site_idx]
    else:
        site = get_rand_other_site()
    # If INCLUDE_OTHER_SITES is False, site_idx will always be smaller than 10, so SITE is always selected from SITES. Is it is True, site_idx maybe upto 14. In 1/3 of cases where rit is above 9, it will us a random site from the top 1m.

    if CAPTURE_AT_ROUTER:
        with open("//mnt/hgfs/site.txt", "w") as f:
            f.write(f"{site},{site_idx},{time_hang}")
    # Writes names to file from host if capturing pcaps from router

    if not CAPTURE_AT_ROUTER:
        datetime_string = dt.datetime.strftime(start_time, date_time_format)
        pcap_name = f"{site}-{site_idx}-{time_hang}-{datetime_string}"
        os.system(f"/home/user/Documents/make_pcap.sh {pcap_name} &")
        # Not required is capturing at router

    time.sleep(start_delay)
    browser=webdriver.Firefox(options=options)

    def load_site(browser, site):
        browser.get(f'https://{site}')
        
    t1 = threading.Thread(target=load_site, args=[browser, site])
    t1.start()

    time.sleep(time_hang)
    browser.close()

    end_time = dt.datetime.now()

    csv_row = f"{start_time}, {end_time}, {site_idx}, {site}, {time_hang}"

    if CAPTURE_AT_ROUTER:
        with open("//mnt/hgfs/log.csv", "a") as f:
            f.write(csv_row + "\n")
    
    return (end_time - start_time).seconds


delays = load_rand_page()

time.sleep(30 - delays)

load_rand_page()