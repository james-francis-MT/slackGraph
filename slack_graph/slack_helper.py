import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

def slack_error_handler(error):
    assert error.response["ok"] is False
    assert error.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {error.response['error']}")
    raise error

def get_channel_members(channel_id):
    try:
        response = client.conversations_members(channel=channel_id)
        print(f'status code: {response.status_code}')
        if response.data['ok'] is True:
            return response.data['members']
        raise RuntimeError('received non 200 response')
    except SlackApiError as error:
        slack_error_handler(error)
        return {}

def get_user_info(use_id):
    try:
        response = client.users_info(user=use_id)
        print(f'status code: {response.status_code}')
        if response.data['ok'] is True:
            return response.data['user']
        raise RuntimeError('received non 200 response')
    except SlackApiError as error:
        slack_error_handler(error)
        return {}
