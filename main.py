from aiohttp import web

from routes import setup_routes
from settings import config
from weather_getter import WhetherGetter


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status != 404:
            return response
        message = response.reason
    except web.HTTPException as ex:
        if ex.status != 404:
            raise
        message = ex.reason
    return web.json_response({'status': 'error', 'message': message})


app = web.Application(middlewares=[error_middleware])

app['locations'] = config['locations']

weather_getter = WhetherGetter() # Сущность для запросов во внешний источник
app['weather_getter'] = weather_getter

setup_routes(app)
web.run_app(app)
