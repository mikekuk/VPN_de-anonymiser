#!/usr/bin/env python3

# Work in progress. Currently visualise 20 sec capture. Will go on to make predictions onn rolling 20 sec capture.


# Suppress excess logging to terminal.
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


from scapy.all import sniff, IP
# import multiprocessing
import threading
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime as dt
import time
import tensorflow as tf


TIME_FRAME = 10
CLIENT = "192.168.254.0"
IFACE = "ens33"
OFFSET = 0
SCALER_MAX = 709.0  # Max values observed during training, thus required for current model.

print("[+] Loading model.")
model = tf.keras.models.load_model('models/convlstm_model_Datetime_2022_05_26__23_52_24__loss_0.08553284406661987_acc_0.9906666874885559.h5')
print(f"[+] Loaded model {model}.")


SITES = [
    "www.amazon.co.uk",
    "www.bbc.co.uk",
    "www.ebay.co.uk",
    "www.facebook.com",
    "www.google.co.uk",
    "www.google.com",
    "www.twitter.com",
    "www.uwe.ac.uk",
    "www.wikipedia.com",
    "www.youtube.com"
]

def gen_matrix():

    def add_pkt(packet):
        if IP in packet:
            time_round = round(packet.time - start_time, 1) + OFFSET
            length = packet[IP].len
            dir = (lambda x: 0 if x[IP].src == CLIENT else 1)(packet)
            matrix[int(time_round * 10)-1][int(length / 10)-1][dir] += 1

    start_time = dt.now().timestamp()
    matrix = np.zeros([200, 150, 2])
    sniff(filter="ip", prn=add_pkt, timeout=int(TIME_FRAME), iface=IFACE)
    return np.array([matrix])

def predict(matrix):
    predictions = model.predict(matrix/SCALER_MAX)
    print("\n\n")
    for i in range(len(SITES)):
        print(f"{SITES[i]} - {round(predictions[0][i], 2)}")
    print("\n\n")

def plot_matrix(matrix):
    plt.imshow(np.pad(matrix[0], (0,1)), aspect="auto")
    plt.show()


def main():
    count = 5
    while count > 0:
        t1 = time.perf_counter()
        matrix = gen_matrix()
        t2 = time.perf_counter()
        print(f"Time taken for capture: {t2 - t1}")
        p2 = threading.Thread(target=predict, args=[matrix])
        p2.start()
        t3 = time.perf_counter()
        print(f"Time taken for process start: {t3 - t2}")
        print(f"Time taken for loop: {t3 - t1}")
        count -= 1
        



if __name__ == "__main__":
    main()