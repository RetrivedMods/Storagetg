import os
import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Read environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
SAFELINK_URL = os.getenv('SAFELINK_URL')  # Replace with your safelink URL

if not BOT_TOKEN or not CHANNEL_ID or not SAFELINK_URL:
    raise ValueError("Please set BOT_TOKEN, CHANNEL_ID, and SAFELINK_URL environment variables.")

async def start(update: Update, context):
    await update.message.reply_text('Send me a file to upload!')

async def handle_file(update: Update, context):
    file = await update.message.effective_attachment.get_file()
    file_path = f"downloads/{file.file_id}"
    await file.download_to_drive(file_path)

    # Upload file to channel
    with open(file_path, 'rb') as f:
        message = await context.bot.send_document(chat_id=CHANNEL_ID, document=InputFile(f))

    # Generate download link
    file_id = message.document.file_id
    file_link = f"https://t.me/{CHANNEL_ID[1:]}/{message.message_id}"
    safelink = f"{SAFELINK_URL}?file={file_link}"

    # Send safelink to user
    await update.message.reply_text(f"Your file is uploaded! Download link: {safelink}")

    # Clean up
    os.remove(file_path)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()
