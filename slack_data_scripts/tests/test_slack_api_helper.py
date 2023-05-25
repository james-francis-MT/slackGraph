import sys
import pytest
from slack_sdk.web import SlackResponse
sys.path.insert(0, '/Users/jamesfrancis/repos/slackGraph/')
from slack_data_scripts.src.slack_api_helper import get_channel_members

def slack_response_helper(data):
    return SlackResponse(status_code=200, data=data, client=MockWebClient(), http_verb='', api_url='', req_args={}, headers={})

class MockWebClient:
    def __init__(self):
        pass

    def conversations_members(self, channel: str):
        return slack_response_helper({'ok': True, 'members': ['member1', 'member2']})

def test_calls_the_correct_api():
    mock_client = MockWebClient()
    assert get_channel_members('blah', mock_client) == ['member1', 'member2']

def test_raises_error_if_status_is_not_ok():
    mock_client = MockWebClient()
    mock_client.conversations_members = lambda channel: slack_response_helper({'ok': False, 'members': ['member1', 'member2']})
    with pytest.raises(RuntimeError) as error_info:
        get_channel_members('blah', mock_client)
    assert 'received non 200 response' in str(error_info.value)
