#!/home/user/Documents/data_collect/bin/python3

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *


import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
# from selenium.webdriver import FirefoxProfile
import datetime as dt
import os
import subprocess
import pandas as pd
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
import threading
import numpy as np


CAPTURE_AT_ROUTER = False
INCLUDE_OTHER_SITES = True
OPENWORLD_RATIO = 0.5 # ratio of len(SITES) to add as openwrold data. eg, 0.5 means add half the length of the SITES list as openworld sites (0.5:1 ratio), 1 means add the number (1:1 ratio)
TIMEFRAME = 20

# Constants for array extractiion
MIN_PACKETS = 50

CLIENT_SUBNET = '172'

try:
    pet = os.environ['PET']
except:
    pet = "vpn" 

if pet == "tor":
    tor = True
else:
    tor = False


try:
    hostname = os.environ['HOST_TAG']
except:
    hostname = "testing"


try:
    ow_ratio = float(os.environ['OW_RATIO'])
except:
    ow_ratio = OPENWORLD_RATIO


sites_df = pd.read_csv("C:\\Users\\Administrator\\Documents\\GitHub\\VPN_de-anonymiser\\VPN_client_scripts\\urls\\top_100_v2.csv", names=["ranking", "site", "tor_compatible"])
if tor:
    sites_df = sites_df[sites_df["tor_compatible"] == 1]
sites = list(sites_df.site)

if INCLUDE_OTHER_SITES:
    df = pd.read_csv("C:\\Users\\Administrator\\Documents\\GitHub\\VPN_de-anonymiser\\VPN_client_scripts\\urls\\top10k_cleaned.csv", names=["ranking", "site"])
    # Source: https://www.kaggle.com/datasets/cheedcheed/top1m?resource=download
    other_sites = df[~df.site.isin(sites)]
    def get_rand_other_site():
        randint = random.randint(0, len(other_sites) -1)
        return other_sites.site.iloc[randint]
    # Opens top 1m sties are removes duplicates from the SITES list. Defines a function to return one random site.


firefox_options = Options()

if tor:
    firefox_options.set_preference("network.proxy.type", 1)
    firefox_options.set_preference("network.proxy.socks", "127.0.0.1")
    firefox_options.set_preference("network.proxy.socks_port", 9150)
    firefox_options.set_preference("network.proxy.socks_remote_dns", True)



firefox_options.set_preference("profile.default_content_settings.cookies", 2)
firefox_options.set_preference("profile.default_content_setting_values.cookies", 2)
firefox_options.set_preference("browser.shell.checkDefaultBrowser", False)
firefox_options.set_preference("browser.cache.disk.enable", False)
firefox_options.set_preference("browser.cache.memory.enable", False)
firefox_options.set_preference("browser.cache.offline.enable", False)
firefox_options.set_preference("network.http.use-cache", False)

firefox_options.binary_location = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
firefox_options.set_capability("pageLoadStrategy", "normal")  # complete
# firefox_options.set_capability("pageLoadStrategy", "eager")  # interactive
# firefox_options.set_capability("pageLoadStrategy", "none")   # undefined

firefox_service = Service(executable_path="C:\\Drivers\\geckodriver.exe")
browser = webdriver.Firefox(service=firefox_service, options=firefox_options)


date_time_format = '%Y_%m_%d__%H_%M_%S'



# Define a function to run the tshark command
def run_tshark(name):
    if tor:
        cmd = f'"C:\\Program Files\\Wireshark\\tshark.exe" -i 4 -s 128 -a duration:20 -w "C:\\Users\\Administrator\\Documents\\pcaps\\{name}.pcap" port 9001'
    else:
        cmd = f'"C:\\Program Files\\Wireshark\\tshark.exe" -i 4 -s 128 -a duration:20 -w "C:\\Users\\Administrator\\Documents\\pcaps\\{name}.pcap" host 154.16.196.216'
    subprocess.run(cmd, shell=True)



def load_rand_page():
    
    start_time = dt.datetime.now()

    len_sites = len(sites)
    addition = int(len_sites * (ow_ratio))

    start_delay = random.randint(1,10) /10

    if INCLUDE_OTHER_SITES:
        site_idx = random.randint(0,(len_sites + addition -1))
    else:
        site_idx = random.randint(0,len_sites - 1)
    # If INCLUDE_OTHER_SITES is true, it will make 1/3 of sites a random selection from the other sites list.
    time_hang = random.randint(15, 20)

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
        pcap_name = f"{site}-{hostname}-{site_idx}-{time_hang}-{datetime_string}-{pet}"


        
        # Run the tshark command in a separate thread  
        tshark_thread = threading.Thread(target=run_tshark, args=(pcap_name,))
        tshark_thread.start()
    
        
        # os.system(f'start "" C:\\Users\\Administrator\\Documents\\GitHub\\VPN_de-anonymiser\\VPN_client_scripts\\make_pcap.bat {pcap_name}')
        # Not required is capturing at router

    time.sleep(start_delay)
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

    
    browser.quit()
    
    # browser.close()
    
    end_time = dt.datetime.now()

    tshark_thread.join()


    csv_row = f"{start_time}, {end_time}, {site_idx}, {site}, {time_hang}, {status}"

    if not CAPTURE_AT_ROUTER:
        with open("C:\\Users\\Administrator\\Documents\\pcaps.log.csv", "a") as f:
            f.write(csv_row + "\n")
    

    def is_inbound(packet):
        if packet[IP].src[:3] == CLIENT_SUBNET:
            return False
        else:
            return True

    def extract_features_from_clips(clip):

        matrix_small = np.zeros([TIMEFRAME * 10, 150, 2])
        matrix_large = np.zeros([TIMEFRAME * 100, 1500, 2])
        df_encoding = np.zeros(5000, dtype=int)
        cumul_encoding = np.zeros(100)

        start_time = clip[0].time

        for i, pkt in enumerate(clip):
            if IP in pkt:

                size = pkt[IP].len
                inbound = is_inbound(pkt)

                # Matrix small

                length = (lambda x: x if x <= 1500 else 1500)(size) # Packets over 1500 are rounded down to 1500
                dir = (lambda: 0 if inbound else 1)()
                time_round = round(pkt.time - start_time, 2) 
                if time_round >= 20:
                    time_round = 20.0
                matrix_small[int(round(time_round, 1) * 10)-1][int(length / 10)-1][dir] += 1

                # Matrix large

                matrix_large[int(time_round * 100)-1][int(length)-1][dir] += 1

                # DF

                if i < 5000 and inbound:
                    df_encoding[i] = 1
                elif i < 5000 and not inbound:
                    df_encoding[i] = -1

                
                # CUMUL

                if i < 100 and inbound:
                    cumul_encoding[i] += size
                elif i < 100 and not inbound:
                    cumul_encoding[i] -= size
                
                
        return np.array(matrix_small), np.array(matrix_large), np.array(df_encoding), np.cumsum(np.array(cumul_encoding))
    

    last_pcap = rdpcap(f"C:\\Users\\Administrator\\Documents\\pcaps\\{pcap_name}.pcap")

    if len(last_pcap) > MIN_PACKETS:
    
        array_small, array_large, df_encoding, cumul_encoding = extract_features_from_clips(last_pcap)


        # # Comment out for prod, just used for testing.
        # from matplotlib import pyplot as plt
        # plt.imshow(np.pad(array, (0,1)), aspect="auto")
        # plt.show()


        pcap_path = f"C:\\Users\\Administrator\\Documents\\pcaps\\{pcap_name}.pcap"
        array_small_path  = f"C:\\Users\\Administrator\\Documents\\arrays\\{pcap_name}-small.npy"
        array_large_path = f'C:\\Users\\Administrator\\Documents\\arrays\\{pcap_name}-large.npy'
        df_encoding_path = f'C:\\Users\\Administrator\\Documents\\arrays\\{pcap_name}-df.npy'
        cumul_encoding_path = f'C:\\Users\\Administrator\\Documents\\arrays\\{pcap_name}-cumul.npy'
        
        with open(array_small_path, "wb") as f:
            np.save(f, array_small)

                
        with open(array_large_path, "wb") as f:
            np.save(f, array_large)

                
        with open(df_encoding_path, "wb") as f:
            np.save(f, df_encoding)

                
        with open(cumul_encoding_path, "wb") as f:
            np.save(f, cumul_encoding)


        def copy_and_delete(file_path):
            if file_path[-3:] == 'cap':
                    location = "pcaps"
            else:
                location = "arrays"

            copy_cmd = f'aws s3 cp "{file_path}" s3://{location}-for-wfa/'
            delete_cmd = f'del "{file_path}"'

            subprocess.run(copy_cmd, shell=True)
            subprocess.run(delete_cmd, shell=True)
        
        copy_and_delete(pcap_path)
        copy_and_delete(array_small_path)
        copy_and_delete(array_large_path)
        copy_and_delete(df_encoding_path)
        copy_and_delete(cumul_encoding_path)

load_rand_page()

