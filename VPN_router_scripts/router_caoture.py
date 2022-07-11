import os
import time
import datetime as dt

pcap_name = "router"
date_time_format = '%Y_%m_%d__%H_%M_%S'
file_path = "//mnt/hgfs/site.txt"

 
def capture(pcap_name):
    start_time = dt.datetime.now()

    start_epoch = int(start_time.strftime('%s'))
    modified_time = os.path.getmtime(file_path)
    while (start_epoch - modified_time) > 1:
        modified_time = os.path.getmtime(file_path)
    # Checks if the file_path was modified under 1 second ago. If not it waits until it is beofre executring. This ensures the correct data is loaded on read. 

    with open(file_path, "r") as f:
        text = f.read()
    site, site_idx, time_hang = text.split(",")
    # Opens filepath to get site detials from client. 

    datetime_string = dt.datetime.strftime(start_time, date_time_format)
    pcap_name = f"{site}-{site_idx}-{time_hang}-{datetime_string}"
    time.sleep(0.1)
    os.system(f"/home/user/code/VPN_de-anonymiser/VPN_client_scripts/make_pcap.sh {pcap_name} &")
    end_time = dt.datetime.now()
    return (end_time - start_time).seconds

if __name__ == "__main__":
    delay = capture(pcap_name)
    time.sleep(30 - delay)
    capture(pcap_name)
