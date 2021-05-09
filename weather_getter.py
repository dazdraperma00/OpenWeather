import aiohttp

URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
API_TOKEN = '298996eb774cd549c4a0cdd8e11d3c47'


async def weather_getter(app, id_: [int]):
    async with aiohttp.ClientSession() as session:
        city = app['locations'][id_]
        async with session.get(URL.format(city, API_TOKEN)) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None
