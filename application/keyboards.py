from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


geo_request_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Send location", request_location=True)],
            [KeyboardButton(text="❌ Cancel")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
