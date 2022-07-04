# VPN De-anonymiser

This project is intended to identify what website a user is browsing under a VPN, without breaking the crypto.
It does this with a ML model made in Tensorflow.

## Set up

The lab has been setup with two Ubuntu Linux VMs, one acting as a VPN Client and one as a router. The clients has been configured to route all traffic through the router. tHe router has IP forwarding enabled, and is running two network interfaces. Both machines have access to a shared files called 'pcap_data' on the host machine.

### VPN configuration.

P.I.A VPN has been installed on the client, and is running OpenVPN protocol through UDP with AES128 GCM encryption.

## File uses

The files in VPN_router_scripts and VPN_client_scripts are intended to run on those two machine.

THe client gen_data.py is trigger to run every minute form crontab with the following entry.

```
* * * * * DISPLAY=:0 /home/user/Documents/data_collect/bin/python3 /home/user/Documents/gen_data.py
```

For this to work as intended, the selenium drivers need to be installed. This can be downloaded form https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/

The client will save all pcaps to the shared pcap_data directory.

If required, extract_clips.py is used to exctact sessions and 20 second clips from larger pcaps. This is set to work with the ISCX VPN-No nVPN dateset.

extract_arrays.ipynb is used to extract and save numpy arrays of the correct shape for training the model.

data_visulise.ipynb is sued to visualise the extracted arrays.

ml_test.ipynb is used to train and save the models. 

predict.ipynb is used to evaluate the model with subsequent datasets.

real_time_capture.py in VPN_router-scrips is used to make realtime predictions of what what the clent is doing from the router. 

functions.py contains helper function that are used for other scripts. 