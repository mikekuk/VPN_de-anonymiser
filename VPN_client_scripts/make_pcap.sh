#!/bin/bash

tcpdump -i ens33 -s 128 -G 20 -W 1 -w /mnt/hgfs/$1.pcap