import os
import time
import json
from slackclient import SlackClient
from watson_developer_cloud import ConversationV1


# Chatbot's ID as constant
BOT_ID = ""

# Other Constants
AT_BOT = "<@" + BOT_ID + ">"

# Channels to which bot is added
bot_channels = ['']

# Instantiate Slack Client
slack_client = SlackClient('')


# Watson Constants
conversation = ConversationV1(
  username='',
  password='',
  version=''
)

workspace_id = ''

context = {}


def action(command):
    if 'xyz' in command:
        print "Action Invoked"
    else:
        pass



def parse_slack_output(slack_rtm_output):
    """
        This parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    #print output_list
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
            elif output and 'text' in output and 'bot_id' not in output and output['channel'] not in bot_channels:
                return output['text'].lower(), \
                       output['user']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Optimus Prime connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                action(command)
                response = conversation.message(
                workspace_id=workspace_id,
                message_input={'text': command},
                context=context # Replace with the context obtained from the initial request
                )
                output = str(response['output']['text'][0])
                context = response['context']
                slack_client.api_call("chat.postMessage", channel=channel, text=output, as_user=True)
                
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID")
