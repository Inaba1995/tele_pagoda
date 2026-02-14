import asyncio
import requests
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Bot, Dispatcher, types, F

from config import BOT_TOKEN, YAND_TOKEN, BELGOROD_LAT, BELGOROD_LON


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def get_weather():
    url = f'https://api.weather.yandex.ru/v2/forecast?lat=52.37125&lon=4.89388'
    headers = {
        "X-Yandex-API-Key": YAND_TOKEN
    }
    params = {
        "lat": BELGOROD_LAT,
        "lon": BELGOROD_LON,
        "lang": "ru_RU"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]


        message = (
            f"🌤 Погода в Белгороде:\n\n"
            f"Температура: {temp} °C\n"
            f"Ощущается как: {feels_like} °C\n"
            f"Влажность: {humidity} %\n"
            f"Давление: {pressure} гПа\n"
            f"Небо: {description}\n"
            f"Ветер: {wind_speed} м/с"
        )
        return message
    except Exception as e:
        return f"Ошибка получения погоды: {e}"



@dp.message(F.text == "/weather")
async def cmd_weather(message: types.Message):
    weather_info = await get_weather()
    await message.answer(weather_info)



@dp.message(CommandStart)
async def start(message: Message):
    await message.answer("Привет, ленивый человек, не способный открыть даже браузер! Нажми /weather, чтобы узнать погоду в Белгороде.")



@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Вот шо у нас есть: \n /help, \n /start, \n /weather")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
