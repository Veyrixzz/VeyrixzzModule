# meta developer: @veyrixzz

from .. import loader, utils
import requests

class LiveToolsMod(loader.Module):
    """Live-трекер от veyrixzz — все валюты, вся крипта, солнце"""
    strings = {"name": "LiveTools"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.command()
    async def курс(self, message):
        """Показать курс любой валюты к рублю: .курс usd"""
        code = utils.get_args_raw(message).lower()
        if not code:
            await message.edit("💱 Укажи код валюты: .курс usd")
            return
        try:
            data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
            valutes = data["Valute"]
            if code.upper() not in valutes:
                available = ", ".join(valutes.keys())
                await message.edit(f"❌ Не найдена такая валюта.\nДоступные: {available.lower()}")
                return
            val = valutes[code.upper()]
            await message.edit(f"💱 {code.upper()} к RUB:\n"
                               f"• Покупка: {val['Value']:.2f} ₽\n"
                               f"• Вчера: {val['Previous']:.2f} ₽")
        except Exception as e:
            await message.edit(f"⚠️ Ошибка получения курса: {e}")

    @loader.command()
    async def crypto(self, message):
        """Курс любой криптовалюты к USD: .crypto bitcoin"""
        coin = utils.get_args_raw(message).lower()
        if not coin:
            await message.edit("🪙 Укажи название крипты: .crypto bitcoin")
            return
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {"ids": coin, "vs_currencies": "usd"}
            res = requests.get(url, params=params).json()

            if coin not in res:
                await message.edit("❌ Не найдена такая криптовалюта (используй id из CoinGecko)")
                return

            price = res[coin]["usd"]
            await message.edit(f"🪙 {coin.upper()} сейчас: ${price}")
        except Exception as e:
            await message.edit(f"⚠️ Ошибка получения крипты: {e}")

    @loader.command()
    async def sun(self, message):
        """Время восхода и заката: .sun город"""
        city = utils.get_args_raw(message)
        if not city:
            await message.edit("🌇 Укажи город: .sun krasnodar")
            return
        try:
            geo = requests.get("https://geocoding-api.open-meteo.com/v1/search", params={"name": city}).json()
            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]

            sun = requests.get("https://api.open-meteo.com/v1/forecast", params={
                "latitude": lat,
                "longitude": lon,
                "daily": "sunrise,sunset",
                "timezone": "auto"
            }).json()

            sunrise = sun["daily"]["sunrise"][0].split("T")[1]
            sunset = sun["daily"]["sunset"][0].split("T")[1]

            await message.edit(f"🌅 Город: {city.title()}\n"
                               f"• Восход: {sunrise}\n"
                               f"• Закат: {sunset}")
        except:
            await message.edit("❌ Не удалось получить данные о солнце.")