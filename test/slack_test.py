import requests

myToken = "xoxb-3348226843249-3337959274820-CU2f0XUxBQZS6PcMM7pP2B0y"

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

post_message(myToken, '#bitcoin', 'test')