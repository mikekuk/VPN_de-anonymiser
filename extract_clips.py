#!/usr/bin/env python3

# Used to extract 20 clips of streams from larger dataset. Inputs directory of mixed pcaps and outputs labeled 20 clips suitable for the input to extract_arrays.ipynb.

import os
from functions import check_paths, check_dependencies, split_to_clips, extract_streams


PATHS = [
    "SCX-VPN-NonVPN-2016/NonVPN-PCAPs-01",
    "SCX-VPN-NonVPN-2016/VPN-PCAPS-01",
    "SCX-VPN-NonVPN-2016/VPN-PCAPs-02"
]

TIMEFRAME = 20

######################## Stage 0 - Checks ######################## 

check_paths(PATHS)

check_dependencies()

######################## Stage 1 - Extract Streams ######################## 

for path in PATHS:
    dir_list = os.listdir(path)
    print(f"[+] {len(dir_list)} files found in {path}.")
    print(f"[+] {dir_list}")
    total = len(dir_list)

    if not os.path.exists(path + "/extracted"):
        os.mkdir(path + "/extracted")

    i = 1
    for file in dir_list:
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path) and (full_path[-5:] == ".pcap" or full_path[-7:] == ".pcapng") and not os.path.isdir(full_path):
            print(f"[+] Extracting {full_path}, {i} of {total}.")
            if os.path.exists(os.path.join(path, "extracted", file.split(".")[0])):
                print(f"[-] {path}/extracted/{file} already exists")
            else:
                extract_streams(path, file)
            i += 1
        else:
            print(f"[-] Skipping. {full_path} is not a pcap.")

print("[+] All paths extracted.")

######################## Stage 2 - Split to timeframe ######################## 

print(f"[+] Extracting {TIMEFRAME} second clips from streams")

clips_dir = f"{TIMEFRAME}_Sec_Clips"
print(f"[+] Creating {clips_dir}.")
os.makedirs(clips_dir, exist_ok=True)

extracted_dirs = [path + "/extracted" for path in PATHS]

print(f"[+] Extracted stream directories: {extracted_dirs}")

for path in extracted_dirs:
    print(f"[+] Extracting clips from {path}")
    files = os.listdir(path)
    for file in files:
        if os.path.isdir(os.path.join(path, file)):
            streams = os.listdir(os.path.join(path, file))
            for stream in streams:
                split_to_clips(os.path.join(path, file, stream), timeframe=TIMEFRAME, clips_dir=clips_dir)

######################## Stage 3 - extract clips to array ######################## 

# Use extract_arrays.ipynb for this step.