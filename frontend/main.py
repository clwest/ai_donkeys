from flet import *
from utils.colors import *
from utils import routes

def main(page: Page):
    page.title = "Donkey Betz"
    page.fonts = {
        "Oswald": FONT_URL
    }
    page.theme = Theme(font_family="Poppins")
    
    def route_change(event : RouteChangeEvent):
        
        page.views.clear()
        page.views.append(
            routes.router(page)[page.route]
        )
        
    page.on_route_change = route_change
    page.go('/')
    


app(target=main, view=AppView.WEB_BROWSER, port=5050, assets_dir="assets")
