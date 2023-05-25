from slack_sdk.errors import SlackApiError
from slack_sdk.web import WebClient

def slack_error_handler(error):
    assert error.response["ok"] is False
    assert error.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {error.response['error']}")
    raise error

def get_channel_members(channel_id, client: WebClient):
    try:
        response = client.conversations_members(channel=channel_id)
        print(f'status code: {response.status_code}')
        if response.data['ok'] is True:
            return response.data['members']
        raise RuntimeError('received non 200 response')
    except SlackApiError as error:
        slack_error_handler(error)
        return {}

def get_user_info(use_id, client: WebClient):
    try:
        response = client.users_info(user=use_id)
        print(f'status code: {response.status_code}')
        if response.data['ok'] is True:
            return response.data['user']
        raise RuntimeError('received non 200 response')
    except SlackApiError as error:
        slack_error_handler(error)
        return {}

def get_channel_list(team_id, client: WebClient):
    try:
        channels = []
        complete = False
        cursor = ''

        while(not complete):
            response = client.conversations_list(team_id=team_id, cursor=cursor)
            print(f'status code: {response.status_code}')
            if not response.data['ok']:
                raise RuntimeError('received non 200 response')
            
            channels += response.data['channels']
            if response.data['response_metadata']['next_cursor']:
                cursor = response.data['response_metadata']['next_cursor']
            else:
                complete = True
            print(f'total channels so far: {len(channels)}')

        return channels
    
    except SlackApiError as error:
        slack_error_handler(error)
        return {}
    
def get_user_list(team_id, client: WebClient):
    try:
        users = []
        complete = False
        cursor = ''

        while(not complete):
            response = client.users_list(team_id=team_id, cursor=cursor)
            print(f'status code: {response.status_code}')
            if not response.data['ok']:
                raise RuntimeError('received non 200 response')
            
            users += response.data['members']
            if response.data['response_metadata']['next_cursor']:
                cursor = response.data['response_metadata']['next_cursor']
                print(f'total users so far: {len(users)}')
            else:
                complete = True
        
        return users
    
    except SlackApiError as error:
        slack_error_handler(error)
        return {}