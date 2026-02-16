import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

# أمر /start
async def start(update, context):
    await update.message.reply_text("هلا بيك 👋 البوت شغال على Render مجاناً")

dispatcher.add_handler(CommandHandler("start", start))

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

if __name__ == "__main__":
    bot.set_webhook(url=os.getenv("RENDER_EXTERNAL_URL") + "/webhook")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
