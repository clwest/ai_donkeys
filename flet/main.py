from flet import *
from utils.colors import *
from utils import routes
from components.navbar import AppBarManager


def main(page: Page):
    page.title = "Donkey Betz"
    page.fonts = {
        "Oswald": FONT_URL
    }
    page.theme = Theme(font_family="Poppins")
    app_bar_manager = AppBarManager(page)
    page.appbar = app_bar_manager.create_appbar()


    # def route_change(event : RouteChangeEvent):
        
    #     page.views.clear()
    #     route_view = routes.router(page).get(page.route, None)
    #     if route_view:
    #         page.views.append(route_view)
    
    def route_change(event: RouteChangeEvent):
        page.views.clear()
        route_dict = routes.router(page)  # Ensure this returns a dict of routes to views
        current_view = route_dict.get(page.route)
        if current_view:
            page.views.append(current_view)
        else:
            print(f"No view registered for {page.route}")

    page.on_route_change = route_change
    page.go('/')

app(target=main, view=AppView.WEB_BROWSER, port=5050, assets_dir="assets")
