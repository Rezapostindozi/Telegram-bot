from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config.config import TOKEN


# ساخت نمونه ربات تلگرام با استفاده از توکن تعریف شده در فایل .env
bot = TeleBot(TOKEN)
