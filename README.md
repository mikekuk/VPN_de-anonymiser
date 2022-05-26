# VPN De-anonymiser

This project is intended to identify what website a user is browsing under a VPN, without breaking the crypto.
It does this with a ML model made in Tensorflow.

## Dataflow

data_visulise.ipynb is used for initial data visualisation.

If required, extract_clips.py is used to exctact sessions and 20 second clips from larger pcaps. This is set to work with the ISCX VPN-No nVPN dateset.

extract_arrays.ipynb is used to extract and save numpy arrays of the correct shape for training the model.

data_visulise.ipynb is sued to visualise the extracted arrays.


ml_test.ipynb is used to train and save the models. 


