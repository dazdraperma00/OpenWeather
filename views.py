import asyncio

from aiohttp import web


async def search(request):
    params = request.query
    if len(params) != 1 or 'ids' not in params:
        message = "Incorrect request."
        return web.HTTPNotFound(reason=message)

    city_ids = params['ids'].strip(',').split(',')

    results = []
    city_names = [request.app['locations'][int(city_id)] for city_id in city_ids]
    weather_getter = request.app['weather_getter']  # Сущность для запросов во внешний источник
    aws = [weather_getter.get_whether(city) for city in city_names]
    for fut in asyncio.as_completed(aws):
        forecast = await fut

        if forecast is None:
            # Закрываем оставшиеся таски
            weather_getter.cancel_tasks(city_names)

            message = 'Internal error!'
            return web.HTTPNotFound(reason=message)
        results.append(forecast)

    response = {
        'status': 'ok',
        'data': results
    }

    return web.json_response(response)


async def locations(request):
    loc = request.app['locations']
    data = {
        'status': 'ok',
        'data': {"locations": loc}
    }

    return web.json_response(data)
