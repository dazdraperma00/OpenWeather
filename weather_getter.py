import asyncio

import aiohttp


class WhetherGetter:
    """Сущность для совершения запросов во внешний источник.

    """

    def __init__(self):
        self.clients_by_city = {}
        self.loop = asyncio.get_event_loop()
        self.URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
        self.API_TOKEN = '298996eb774cd549c4a0cdd8e11d3c47'
        # self.session = aiohttp.ClientSession()

    def get_whether(self, city: str) -> asyncio.Future:
        """Метод, возвращающий объект future.
           "Подписывает" вызывающию корутину на получение результата.
           Создает таск, который резолвит объект future.
        """
        obj = self.clients_by_city.get(city, None)
        if obj is None:
            # print(f"There is no future yet! I will create one for {city}!")
            fut = self.loop.create_future()
            task = asyncio.create_task(self.api_request(city))
            obj = [fut, task, 0]  # Добавляем созданный таск, и счетчик ожидающих
            self.clients_by_city[city] = obj
        obj[2] += 1

        return obj[0]

    async def api_request(self, city: str):
        """Корутина, отмечающая future объект как выполненый
           и удаляет его из дикта
        """
        forecast = await self.weather_getter(city)
        self.clients_by_city[city][0].set_result(forecast)
        del self.clients_by_city[city]

    async def weather_getter(self, city: str):
        """Коррутина для запроса во внешний источник"""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.URL.format(city, self.API_TOKEN)) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None

    def cancel_tasks(self, city_names: [str]):
        """Закрывает зашедуленные таски"""
        for city in city_names:
            obj = self.clients_by_city.get(city, None)
            #  Если таск ожидает только одна корутина, закрываем его
            if obj is not None and obj[2] == 1:
                obj[1].cancel()
                del self.clients_by_city[city]
