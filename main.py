import logging
import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Configure o token da OpenAI (você precisa colocar o seu)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ative logs (útil para debug)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Envia a mensagem para o modelo da OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é uma IA divertida, sexy e casual. Responda de forma charmosa, provocante e leve."},
                {"role": "user", "content": user_message},
            ]
        )
        bot_reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(bot_reply)
    except Exception as e:
        await update.message.reply_text("Oops, algo deu errado...")

if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    application.add_handler(message_handler)
    application.run_polling()