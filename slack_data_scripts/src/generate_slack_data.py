import os
import json
import boto3
from slack_api_helper import get_channel_members, get_channel_list, get_user_list
from slack_sdk import WebClient

SLACK_TEAM_ID = 'T0B0XJCTC'

slack_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
s3 = boto3.client('s3')

def store_in_s3(body, key):
    print(f"storing object {key} in slack-data-store")
    s3.put_object(Body=body, Bucket='slack-data-store', Key=key)

# Get all channels
# Store all channel data in S3
channels = get_channel_list(SLACK_TEAM_ID, slack_client)

filtered_channels = list(filter(lambda channel: channel['num_members'] > 0, channels))

for channel in filtered_channels:
    store_in_s3(json.dumps(channel), f"channels/{channel['id']}.json")

# For each channel, get all members
# Store channel members data in S3
for channel in filtered_channels:
    print(f"Getting members for {channel['id']}")
    members = get_channel_members(channel['id'], slack_client)
    store_in_s3(json.dumps({'members': members}), f"members/{channel['id']}.json")

# Get all members in team
# Store all member info in S3
users = get_user_list(SLACK_TEAM_ID, slack_client)

for user in users:
    store_in_s3(json.dumps(user), f"users/{user['id']}.json")