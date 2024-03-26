from flet import *
from utils.colors import *
from services.login import show_login_dialog
from services.register import show_signup_dialog

class AppBarManager:
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.user_logged_in = False
        self.appbar_items = self.get_initial_appbar_items()

    def get_initial_appbar_items(self):
        # Inital items Login, Chatbot, Etc.
        def on_login_click(e):
            print("Login Clicked")
            show_login_dialog(self.page, self.on_login_success)
        
        def on_register_click(e):
            print("Register Clicked")
            show_signup_dialog(self.page, self.on_register_success)

        return [
            PopupMenuItem(text="Login", on_click=on_login_click),
            PopupMenuItem(), # Dividers   
            PopupMenuItem(text="Register", on_click=on_register_click),
            PopupMenuItem(), # Dividers

        ]
    
    def on_login_success(self, login_result):
        active_user = self.page.session.get("username")
        self.user_logged_in = True
        self.update_appbar()
        return active_user

    def on_register_success(self, signup_user):
        self.user_logged_in = True
        self.update_appbar()

    def update_appbar(self):
        if self.user_logged_in:
            active_user = self.page.session.get("username")
            self.appbar_items = [
                PopupMenuItem(text=f"{active_user}'s Profile"),
                PopupMenuItem(),  # Divider
                PopupMenuItem(text="Chatbot"),
                PopupMenuItem(),
                PopupMenuItem(text="Settings"),
                PopupMenuItem(),
                PopupMenuItem(text="Logout"),
            ]
        else:
            self.appbar_items = self.get_initial_appbar_items()
        self.page.appbar = self.create_appbar()
        self.page.update()


    def create_appbar(self):
        # Create and return Appbar based on current state
        return AppBar(
            leading=Icon(icons.CABIN, color="black"),
            leading_width=100,
            title=Text("Donkey Betz AI Services", font_family="Oswald", size=36, text_align="start", color="black"),
            center_title=False,
            toolbar_height=75,
            bgcolor=custom_colors["cyan"],
            actions=[
                Container(
                    content=PopupMenuButton(items=self.appbar_items),
                    margin=margin.only(left=50, right=25),
                )
            ]
        )