import os
from slack_api_helper import get_channel_members, get_channel_list
from slack_sdk import WebClient
import boto3

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

channel_members = get_channel_members('CPPNTCLSE', client)

# channels = get_channel_list('T0B0XJCTC', client)

print(channel_members)

print(channels)

# Retrieve the list of existing buckets
s3 = boto3.client('s3')
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')
