from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
import requests
import json

# Load API keys from .env
load_dotenv()
HF_API_KEY = os.getenv("HuggingFace_API_KEY")  # Hugging Face API key
TOKEN = os.getenv("TOKEN")  # Telegram bot token

# Model Name (Use a reliable Hugging Face chatbot model)
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"  # Change if needed

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

# Hugging Face API function
def query_huggingface(text):
    """Sends user input to Hugging Face API and returns response"""
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    payload = {"inputs": text}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response_json = response.json()

        # Check if API response contains generated text
        if isinstance(response_json, list) and "generated_text" in response_json[0]:
            return response_json[0]["generated_text"]
        elif "error" in response_json:
            return f"API Error: {response_json['error']}"
        else:
            return "Sorry, I couldn't understand that. Try again!"
    
    except requests.exceptions.RequestException as e:
        return "Error: Unable to connect to Hugging Face API."

# Start command
@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("Hello! I am TeleBot, Created by Mihir.\nHow can I assist you? 😊")

# Help command
@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    help_command = """
    🤖 *TeleBot Commands*:
    /start - Start the bot
    /help - Show this help message
    \n Just type your message and I'll respond! 🚀
    """
    await message.reply(help_command, parse_mode="Markdown")

# Handle user messages
@dispatcher.message_handler()
async def chat_huggingface(message: types.Message):
    print(f">>> USER: {message.text}")

    response = query_huggingface(message.text)
    
    print(f">>> Bot: {response}")
    await bot.send_message(chat_id=message.chat.id, text=response)

# Start the bot
if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
