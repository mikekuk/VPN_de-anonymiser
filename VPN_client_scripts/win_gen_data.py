#!/home/user/Documents/data_collect/bin/python3

import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.service import Service
import datetime as dt
import os
import subprocess
import pandas as pd
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
import threading


VM_NAME = "VM1"

CAPTURE_AT_ROUTER = False
INCLUDE_OTHER_SITES = True
OPENWORLD_RATIO = 1 # ratio of len(SITES) to add as openwrold data. eg, 0.5 means add half the length of the SITES list as openworld sites (0.5:1 ratio), 1 means add the number (1:1 ratio)


sites_df = pd.read_csv("C:\\Users\\Administrator\\Documents\\GitHub\\VPN_de-anonymiser\\VPN_client_scripts\\urls\\top_100.csv", names=["ranking", "site"])
sites = list(sites_df.site)

if INCLUDE_OTHER_SITES:
    df = pd.read_csv("C:\\Users\\Administrator\\Documents\\GitHub\\VPN_de-anonymiser\\VPN_client_scripts\\urls\\top10k_cleaned.csv", names=["ranking", "site"])
    # Source: https://www.kaggle.com/datasets/cheedcheed/top1m?resource=download
    other_sites = df[~df.site.isin(sites)]
    def get_rand_other_site():
        randint = random.randint(0, len(other_sites) -1)
        return other_sites.site.iloc[randint]
    # Opens top 1m sties are removes duplicates from the SITES list. Defines a function to return one random site.

options = Options()
options.binary_location = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
options.add_argument("-profile")
options.add_argument("C:\\Users\\Administrator\\AppData\\Local\\Mozilla\\Firefox\\Profiles\\i315s0il.default-release-1")
caps = DesiredCapabilities().FIREFOX
caps["pageLoadStrategy"] = "normal"  #  complete
# caps["pageLoadStrategy"] = "eager"  #  interactive
# caps["pageLoadStrategy"] = "none"   #  undefined

date_time_format = '%Y_%m_%d__%H_%M_%S'

def load_rand_page():
    
    start_time = dt.datetime.now()

    len_sites = len(sites)
    addition = int(len_sites * (OPENWORLD_RATIO))

    start_delay = random.randint(1,30) /10

    if INCLUDE_OTHER_SITES:
        site_idx = random.randint(0,(len_sites + addition -1))
    else:
        site_idx = random.randint(0,len_sites - 1)
    # If INCLUDE_OTHER_SITES is true, it will make 1/3 of sites a random selection from the other sites list.
    time_hang = random.randint(10, 15)

    if site_idx < len_sites:
        site = sites[site_idx]
    else:
        site = get_rand_other_site()
    # If INCLUDE_OTHER_SITES is False, site_idx will always be smaller than 10, so SITE is always selected from SITES. Is it is True, site_idx maybe upto 14. In 1/3 of cases where rit is above 9, it will us a random site from the top 1m.

    if CAPTURE_AT_ROUTER:
        with open("//mnt/hgfs/site.txt", "w") as f:
            f.write(f"{site},{site_idx},{time_hang}")
    # Writes names to file from host if capturing pcaps from router

    if not CAPTURE_AT_ROUTER:
        datetime_string = dt.datetime.strftime(start_time, date_time_format)
        pcap_name = f"{site}-{VM_NAME}-{site_idx}-{time_hang}-{datetime_string}"
        # subprocess.Popen(["start", "", "C:\\Users\\Administrator\\Documents\\GitHub\\VPN_de-anonymiser\\VPN_client_scripts\\make_pcap.bat", pcap_name], shell=True)
        os.system(f'start "" C:\\Users\\Administrator\\Documents\\GitHub\\VPN_de-anonymiser\\VPN_client_scripts\\make_pcap.bat {pcap_name}')
        # Not required is capturing at router

    time.sleep(start_delay)
    browser=webdriver.Firefox(executable_path="C:\\Drivers\\geckodriver.exe", options=options, capabilities=caps)
    browser.set_page_load_timeout(time_hang)

    try:
        browser.get(f'https://{site}')
        time.sleep(time_hang)
        browser.close()
        status = "success"
    except TimeoutException as e:
        print("[-] Page load Timeout Occurred. Quitting !!!")
        browser.close()
        status = "timeout"
    except BaseException as e:
        print(f"[-] Other error occurred. {e} Quitting !!!")
        browser.close()
        status = f"{str(e).replace(',', ' - ')}"
    
    browser.close()
    
    end_time = dt.datetime.now()


    csv_row = f"{start_time}, {end_time}, {site_idx}, {site}, {time_hang}, {status}"

    if not CAPTURE_AT_ROUTER:
        with open("C:\\Users\\Administrator\\Documents\\pcaps.log.csv", "a") as f:
            f.write(csv_row + "\n")
    
    return (end_time - start_time).seconds


load_rand_page()

