from views import search, locations


def setup_routes(app):
    app.router.add_get('/search', search)
    app.router.add_get('/locations', locations)
