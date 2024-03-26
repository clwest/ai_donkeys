from flet import *
from utils.data import *
from utils.colors import *


class AccountInformation(UserControl):

    def __init__(self, page: Page):
        self.page = page
        super().__init__()

    def dashboard(self, e):
        self.page.go("/dashboard")
    
    def sign_out(self, e):
        self.page.go("/")

    def build(self):
        active_user = self.page.session.get("username")

        
        self.top = Container(
            margin=20,
            content=Row(
                alignment=MainAxisAlignment.SPACE_EVENLY,
                controls=[
                    Container(
                        alignment=alignment.top_left,
                        content=IconButton(
                            icon=icons.ARROW_BACK,
                            icon_color=colors.WHITE,
                            on_click=self.dashboard
                        ),
                    ),
                    Text("Account Settings", weight=FontWeight.W_500, size=15, color=colors.WHITE),
                    Stack(
                        [
                            Container(
                                alignment=alignment.center,
                                border_radius=10,
                                bgcolor=colors.GREY_900,
                                content=IconButton(
                                    icon=icons.NOTIFICATIONS_NONE,
                                    icon_color=colors.WHITE
                                ),
                            ),
                            Container(
                                margin=margin.only(left=30),
                                alignment=alignment.top_right,
                                content=CircleAvatar(bgcolor=custom_colors["slate"], radius=5)
                            )
                        ]
                    )
                ]
            )
        )

        self.account_details = Container(
            margin=10,
            border=border.all(1, colors.GREY_500),
            content=ListTile(
                leading=CircleAvatar(
                    foreground_image_url=AVATAR_IMAGE_URL
                ),
                title=Text(f"\n{active_user}", color=colors.WHITE, size=13),
                subtitle=Text("Account Details", color=colors.GREY_400, size=12),
                trailing=Icon(icons.ARROW_FORWARD_IOS_OUTLINED, color=colors.GREY_500)
            )
        )

        self.sign_out_text = Container(
            margin=50,
            on_click=self.sign_out,
            content=Text(
                "Sign out",
                color=colors.RED
            )
        )

        self.settings_control = Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self.top,
                self.account_details,
                self.sign_out_text
            ]
        )

        return self.settings_control