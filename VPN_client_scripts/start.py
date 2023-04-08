import time
import subprocess
import boto3
import requests
import os


# Get Host detils and write to enviroment varible for win_gen_data.py to read.

def get_instance_id():
    # Get instance metadata from the metadata service
    url = 'http://169.254.169.254/latest/meta-data/instance-id'
    response = requests.get(url)
    instance_id = response.text
    return instance_id

def get_tag_value(instance_id, tag_key):
    # Create an EC2 client
    ec2 = boto3.client('ec2')

    # Get the tags for the instance
    response = ec2.describe_tags(Filters=[{
        'Name': 'resource-id',
        'Values': [instance_id]
    }])

    # Find and return the value of the specified tag key
    for tag in response['Tags']:
        if tag['Key'] == tag_key:
            return tag['Value']

    return None


def get_region_id():
    # Get availability zone from the metadata service
    url = 'http://169.254.169.254/latest/meta-data/placement/availability-zone'
    response = requests.get(url)
    availability_zone = response.text

    # Remove the last character from the availability zone to get the region
    region_id = availability_zone[:-1]
    return region_id

def get_tag_value(instance_id, tag_key, region_id):
    # Create an EC2 client with the specified region
    ec2 = boto3.client('ec2', region_name=region_id)

    # Get the tags for the instance
    response = ec2.describe_tags(Filters=[{
        'Name': 'resource-id',
        'Values': [instance_id]
    }])

    # Find and return the value of the specified tag key
    for tag in response['Tags']:
        if tag['Key'] == tag_key:
            return tag['Value']

    return None

intstance_id = get_instance_id()
region = get_region_id()

host_tag = get_tag_value(intstance_id, "Name", region)
ow_ratio_tag = get_tag_value(intstance_id, "Ratio", region)
pet_tag = get_tag_value(intstance_id, "PET", region)

os.environ["HOST_TAG"] = host_tag

# Get open world ratio if tag exists
try:
    os.environ["OW_RATIO"] = ow_ratio_tag
except:
    pass

# Get PET if tag exists
try:
    os.environ["PET"] = pet_tag
except:
    pass


# Update urls list

def download_and_save(url, file_path):
    # Download the document from the URL
    response = requests.get(url)
    response.raise_for_status()

    # Save the contents to the specified file path
    with open(file_path, "wb") as file:
        file.write(response.content)

# Update csv list
url = "https://raw.githubusercontent.com/mikekuk/VPN_de-anonymiser/main/VPN_client_scripts/urls/top_100_v2.csv"
file_path = "C:\\Users\\Administrator\\Documents\\GitHub\\VPN_de-anonymiser\\VPN_client_scripts\\urls\\top_100_v2.csv"
download_and_save(url, file_path)

# Update win_get_data
url = "https://raw.githubusercontent.com/mikekuk/VPN_de-anonymiser/main/VPN_client_scripts/win_gen_data.py"
file_path = "C:\\Users\\Administrator\\Documents\\GitHub\\VPN_de-anonymiser\\VPN_client_scripts\\win_gen_data.py"
download_and_save(url, file_path)

subprocess.run(["python", "C:\\Users\\Administrator\\Documents\\GitHub\\VPN_de-anonymiser\\VPN_client_scripts\\collect.py"])