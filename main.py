import os
import psutil
from slack_sdk import WebClient
import time
from time import sleep
from slack_sdk.errors import SlackApiError

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

last_time = 0
while True:
        mem_per = psutil.virtual_memory().percent
        cpu_per = psutil.cpu_percent()

        if (mem_per > 80 or cpu_per > 80) and time.time() - last_time > 60 * 60:
            last_time = time.time()
            try:
                text = "Hey you doing experiments! \n " \
                       f"You are using more than 80% of your memory ({mem_per}%) or cpu ({cpu_per}%)." \
                       f" Please stop it! \n" \
                       "Leave something so I can continue living!"
                response = client.chat_postMessage(channel='#servers-monitoring', text=text)
                assert response["message"]["text"] == "Hello world!"

            except SlackApiError as e:
                # You will get a SlackApiError if "ok" is False
                assert e.response["ok"] is False
                assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
                print(f"Got an error: {e.response['error']}")
        sleep(30)
