import asyncio
import requests
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Bot, Dispatcher, types, F
from config import BOT_TOKEN, YAND_TOKEN, BELGOROD_LAT, BELGOROD_LON

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def get_weather():
    url = f'https://api.weather.yandex.ru/v2/forecast?'
    headers = {
        "X-Yandex-API-Key": YAND_TOKEN
    }
    params = {
        "lat": BELGOROD_LAT,
        "lon": BELGOROD_LON,
        "lang": "ru_RU"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        print("Ответ API:", data)

        fact = data["fact"]
        temp = fact["temp"]
        feels_like = fact["feels_like"]
        humidity = fact["humidity"]
        pressure_mm = fact["pressure_mm"]
        condition = fact["condition"]
        wind_speed = fact["wind_speed"]

        conditions = {
            "clear": "ясно",
            "partly-cloudy": "малооблачно",
            "cloudy": "облачно",
            "overcast": "пасмурно",
            "drizzle": "морось",
            "light-rain": "небольшой дождь",
            "rain": "дождь",
            "moderate-rain": "умеренный дождь",
            "heavy-rain": "сильный дождь",
            "continuous-heavy-rain": "ливень",
            "showers": "ливни",
            "wet-snow": "мокрый снег",
            "snow": "снег",
            "hail": "град",
            "thunderstorm": "гроза",
            "fog": "туман"
        }
        description = conditions.get(condition, condition)

        message = (
            f"🌤 Погода в Белгороде:\n\n"
            f"!Температура: {temp} °C\n"
            f"!Ощущается как: {feels_like} °C\n"
            f"!Влажность: {humidity} %\n"
            f"!Давление: {pressure_mm} мм рт. ст.\n"
            f"!Состояние: {description}\n"
            f"!Ветер: {wind_speed} м/с"
        )
        return message

    except KeyError as e:
        return f"!Ошибка: не удалось извлечь данные ({e}). Проверьте структуру ответа API."
    except Exception as e:
        return f"Ошибка получения погоды: {e}"

@dp.message(Command("weather"))
async def send_weather(message: Message):
    weather_info = await get_weather()
    await message.answer(weather_info)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Напиши /weather, чтобы узнать погоду в Белгороде.")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())






