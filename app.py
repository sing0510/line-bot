from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('73Mu8Bojy7PwkWxy+bV0eFVUVasQzliOpdStK1TK4j3Ed39P3U9HFT5cvlZyiqDi66k84dv/AE4eoIN3iuyuUVYevWRh1IlRg0FJ4bC6I2ae/UrM2l7aOfhSJENxiHX0gkVPHSRo/SrqyO2krMKwEgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('44b266ad1513f57b4ef8d44a82884c1e')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()