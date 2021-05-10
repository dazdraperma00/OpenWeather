from views import search, locations


def setup_routes(app):
    app.router.add_get('/api/v1/weather/search', search)
    app.router.add_get('/api/v1/weather/locations', locations)
