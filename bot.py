from telegram.ext import (ApplicationBuilder, MessageHandler, filters,
                          CallbackQueryHandler, CommandHandler)

from gpt import *
from util import *

async def start(update, context):
    # await send_photo(update, context, "avatar_main")
    # await send_text(update, context, "Привіт користувач")
    msg = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, msg)
    await show_main_menu(update, context, {
        "start": "Головне меню",
        "profile": "Генерація Tinder-профіля \uD83D\uDE0E",
        "opener": "Повідомлення для знайомства \uD83D\uDD70",
        "message": "Переписка від вашого імені \uD83D\uDE08",
        "date": "Спілкування з зірками \uD83D\uDD25",
        "gpt": "Задати питання ChatGPT\uD83D\uDDE0"
    })

async def gpt(update, context):
    dialog.mode = "gpt"
    await send_photo(update, context, "gpt")
    msg = load_message("gpt")
    await send_text(update, context, msg)

async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)

async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)

def load_token(token_name):
    with open("resources/" + token_name + ".txt", "r", encoding="utf8") as file:
        return file.readline()

dialog = Dialog()
dialog.mode = None

TOKEN = load_token("token")
ChatGPT_TOKEN = load_token("ChatGPT_TOKEN")

chatgpt = ChatGptService(ChatGPT_TOKEN)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.run_polling()
