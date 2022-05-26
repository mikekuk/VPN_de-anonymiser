import os
import shutil
from scapy.all import *



def check_paths(paths: list):
    """
    Checks all paths are valid directories.
    """
    print(f"[+] Extracting following paths: {paths}")
    for path in paths:
        if os.path.exists(path) and os.path.isdir(path):
            print(f"[+] {path} OK.")
        else:
            print(f"[!] ERROR - {path} not valid.")
    print("[+] All paths OK.")



def check_dependencies():
    """
    Checks all command line utilities are installed and present in PATH.
    """
    tools = [
        "editcap",
    ]
    print(f"[+] Checking install command line utilities: {tools}")
    status = True
    for tool in tools:
        status = shutil.which(tool) is not None
        if not status:
            print(f"[!] {tool} not installed.")
    if status:
        print("[+] All dependencies OK.")
    return status


def split_to_clips(file_path: str, timeframe: int, clips_dir: str):
    print(f"[+] Getting clips from {file_path}.")
    if not file_path[-5:] == ".pcap":
        print(f"[!] {file_path} is not of pcap format!")
        return 1
    else:
        os.system(f"editcap -i {timeframe} -s 128 {file_path} {clips_dir}/{file_path.split('/')[-1]}-{timeframe}_sec_clip.pcap")
        print(f"[+] Extracted clips from {file_path}.")
    

def extract_streams(path: str, file: str):
    """
    Reads pcap and pcapng files and extraces bidirectional streams.
    These are then saved as new pcaps in a directory named extracted,
    The files are named with the original file, src and dst IP and port.
    """
    packets = rdpcap(f"{path}/{file}")

    def get_stream(pcap):
        # Creates dict of the packets for bi-directional streams
        streams = {}

        def check_names(src, dst, sport, dport):
            # Checks if stream already exists in either direction
            name1 = f"{src}-{dst}-{sport}-{dport}"
            name2 = f"{dst}-{src}-{dport}-{sport}"
            if name1 in streams:
                return name1
            elif name2 in streams:
                return name2
            else:
                return False

        for pkt in pcap:
            if TCP in pkt:
                src = pkt[IP].src
                dst = pkt[IP].dst
                sport = pkt[TCP].sport
                dport = pkt[TCP].dport
                name = check_names(src, dst, sport, dport)
                if name:
                    streams[name].append(pkt)
                else:
                    name = f"{src}-{dst}-{sport}-{dport}"
                    streams[name] = []
                    streams[name].append(pkt)
        return streams

    streams = get_stream(packets)

    # Extract the pcaps from the file
    if file[-5:] == ".pcap":
        epath = f"{path}/extracted/{file[:-5]}"
    elif file[-7:] == ".pcapng":
        epath = f"{path}/extracted/{file[:-7]}"
    if not (os.path.exists(epath) and os.path.isdir(epath)):
        os.mkdir(epath)
    for name, stream in streams.items():
        wrpcap(f"{epath}/{file[:-5]}-{name}.pcap", stream)
