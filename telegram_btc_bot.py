import requests
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Replace with your Telegram bot token from BotFather
TELEGRAM_BOT_TOKEN = "7734973074:AAF9tj6Qf5M1KnEK0ZhMvrKmM0kyDZy_048"

# Coinbase API endpoints
API_URL_CAD = "https://api.coinbase.com/v2/prices/BTC-CAD/spot"
API_URL_AED = "https://api.coinbase.com/v2/prices/BTC-AED/spot"

async def get_btc_price():
    """Fetches BTC price in CAD and AED from Coinbase API."""
    try:
        cad_price = requests.get(API_URL_CAD).json()["data"]["amount"]
        aed_price = requests.get(API_URL_AED).json()["data"]["amount"]
        return cad_price, aed_price
    except Exception as e:
        print(f"Error fetching BTC prices: {e}")
        return None, None

async def handle_message(update: Update, context: CallbackContext):
    """Responds to user messages."""
    text = update.message.text.lower()
    
    if text == "price":
        cad_price, aed_price = await get_btc_price()
        if cad_price and aed_price:
            reply = f"💰 Bitcoin Prices:\n🇨🇦 CAD: ${cad_price}\n🇦🇪 AED: {aed_price} AED"
        else:
            reply = "⚠️ Error fetching BTC prices. Try again later."
        
        await update.message.reply_text(reply)

async def main():
    """Starts the bot."""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Handle messages (text)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling (listening for messages)
    print("🚀 Bot is running... (Press Ctrl + C to stop)")
    await app.run_polling()

if __name__ == "__main__":
    # Check if an event loop is already running
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if str(e) == "asyncio.run() cannot be called from a running event loop":
            # If in an environment with an existing event loop (e.g., Jupyter notebook)
            asyncio.create_task(main())
        else:
            raise e
