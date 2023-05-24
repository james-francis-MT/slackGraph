from slack_helper import get_channel_members, get_channel_list
import boto3

# channel_members = get_channel_members('CPPNTCLSE')

# channels = get_channel_list('T0B0XJCTC')

# print(channel_members)

# print(channels)

# Retrieve the list of existing buckets
s3 = boto3.client('s3')
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')
