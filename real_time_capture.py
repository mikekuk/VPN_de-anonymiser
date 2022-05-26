#! /Users/michaelkearney/.local/share/virtualenvs/UNB_Datasets-qeLdalLc/bin/python3

# Work in progress. Currently visualise 20 sec capture. Will go on to make predictions onn rolling 20 sec capture.

from socket import timeout
from scapy.all import sniff, IP
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime as dt

TIME_FRAME = 20
CLIENT = "10.249.147.245"
IFACE = "en0"

## Define our Custom Action function
def custom_action(packet):
    if IP in packet:
        time_round = round(packet.time - start_time, 1)
        length = packet[IP].len
        dir = (lambda x: 0 if x[IP].src == CLIENT else 1)(packet)
        matrix[int(time_round * 10)-1][int(length / 10)-1][dir] += 1



start_time = dt.now().timestamp()
matrix = np.zeros([TIME_FRAME * 10, 150, 2])
sniff(filter="ip", prn=custom_action, timeout=int(TIME_FRAME), iface=IFACE)
plt.imshow(np.pad(matrix, (0,1)), aspect="auto")
plt.show()