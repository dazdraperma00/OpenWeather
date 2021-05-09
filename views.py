import asyncio

from aiohttp import web

from weather_getter import weather_getter


async def search(request):
    query = request.query
    if len(query) != 1 or 'ids' not in query:
        message = "Incorrect request."
        return web.HTTPNotFound(reason=message)

    ids = query['ids'].strip(',').split(',')

    results = []
    aws = [weather_getter(request.app, int(id_)) for id_ in ids]
    for fut in asyncio.as_completed(aws):
        result = await fut
        if result is None:
            message = 'Internal error!'
            return web.HTTPNotFound(reason=message)
        results.append(result)

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
