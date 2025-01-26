#!pip install transformers torch python-telegram-bot
#!pip install transformers torch python-telegram-bot nest_asyncio

import os
import subprocess
from transformers import AutoModelForCausalLM, AutoTokenizer
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import nest_asyncio
import asyncio

# Apply `nest_asyncio` to fix nested event loops in Jupyter/Colab
nest_asyncio.apply()

# Install dependencies
print("Installing dependencies. This might take a few minutes...")
dependencies = ["transformers", "torch", "python-telegram-bot"]
for dependency in dependencies:
    subprocess.run(["pip", "install", dependency], check=True)

# LLM setup
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
print(f"Loading model {MODEL_NAME}. This might take a while...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
print("Model loaded successfully.")

# Telegram bot setup
TELEGRAM_API_TOKEN = "7568042284:AAGVOiXYcYmfkkS0Z572vT606VvP-ZAssxs"  # Replace with your bot's API token

if TELEGRAM_API_TOKEN == "YOUR_TELEGRAM_BOT_API_TOKEN":
    raise ValueError("Please replace 'YOUR_TELEGRAM_BOT_API_TOKEN' with your actual API token from BotFather.")

def generate_response(input_text):
    """Generate a response using the LLM."""
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=50)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

async def handle_message(update, context):
    """Handle incoming messages from Telegram users."""
    user_message = update.message.text.lower()
    print(f"Received message: {user_message}")

   # Special case: Respond with an animal fact
    if "tell me about cats and some facts about them" in user_message:
        response = (
            "Purring Mystery: Cats purr at a frequency of about 25-150 Hz, which can promote tissue regeneration and healing in themselves and even humans! "
            "Whisker Superpower: A cat’s whiskers aren’t just for looks—they are highly sensitive tools that help them sense changes in their environment and measure spaces to see if they can fit through.\n"
            "Sleeping Champions: Cats sleep for 12-16 hours a day on average, making them one of the sleepiest animals on Earth.\n"
            "2.Toe Beans: The soft pads on a cat's paws, often called 'toe beans' help them move silently while hunting.\n"
            "3.Tail Communication: Cats use their tails to communicate. A raised tail often means they’re happy or confident, while a flicking tail can indicate irritation or curiosity.\n"
            "4.Unique Nose Prints: A cat’s nose has a unique pattern, much like a human fingerprint!\n"
            "5.Hunting Instincts: Even domesticated cats retain strong hunting instincts, often chasing after toys or small moving objects to mimic their natural behavior\n"
            "peedy Sprinters: Cats can run up to 30 mph (48 km/h) over short distances, making them incredibly fast when they need to be.\n\n"

        )
    else:
        response = generate_response(user_message)

    print(f"Generated response: {response}")
    await update.message.reply_text(response)

async def start(update, context):
    """Handle the /start command."""
    await update.message.reply_text("Hello! I'm your AI assistant. Ask me anything!")

async def main():
    """Main function to run the Telegram bot."""
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Starting the bot...")
    await application.run_polling()  # Corrected method to start polling

if __name__ == "__main__":
    # Run the bot using asyncio to handle the event loop
    asyncio.run(main())
