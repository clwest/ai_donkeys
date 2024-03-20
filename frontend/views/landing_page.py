from flet import *
from utils.data import *
from utils.colors import *

class LandingPage(UserControl):

    def __init__(self, page: Page):
        self.page = page
        super().__init__()

    def start(self, e):
        self.back_arrow.content.visible = True
        self.study.visible = False
        self.welcome_text.visible = False
        self.register_btn.visible = False
        self.sign_in.visible = False

        self.update()

    def back_home(self, e):
        self.back_arrow.visible = False
        self.study.visible = True
        self.welcome_text.visible = True
        self.regsiter_btn.visible = True
        self.sign_in.visible = True

        self.update()

    def sign_up(self, e):
        self.page.go("/signup")

    def login(self, e):
        self.page.go("/login")

    def build(self):
        self.study = Container(
            margin=margin.only(top=20, bottom=20),
            content=Image(
                src="assets/img/study.png",
                height=200,
                width=205
            )
        )
        self.welcome_text = Text(
            "Donkey Betz AI Services",
            color=text,
            size=25,
            weight=FontWeight.W_900,
            text_align=TextAlign.CENTER
        )
        self.register_btn = Container(
            margin=margin.only(top=20, bottom=20),
            content=ElevatedButton(
                on_click=self.sign_up,
    
                style=ButtonStyle(
                    color=text,
                    bgcolor=custom_colors["slate"],
                    shape=BeveledRectangleBorder(radius=30),
                ),
                content=Container(
                    alignment=alignment.center,
                    padding=20,
                    content=Text("Create an account",
                    size=16,
                    weight=FontWeight.W_700
                    )
                )
            )
        )

        self.sign_in = Container(
            margin=margin.only(top=20, bottom=20),
            content=ElevatedButton(
                on_click=self.login,
    
                style=ButtonStyle(
                    color=text,
                    bgcolor=custom_colors["slate"],
                    shape=BeveledRectangleBorder(radius=30),
                ),
                content=Container(
                    alignment=alignment.center,
                    padding=20,
                    content=Text("Login",
                    size=16,
                    weight=FontWeight.W_700
                    )
                )
            )
        )
        self.back_arrow = Container(
            alignment=alignment.top_left,
            content= IconButton(
            icon = icons.ARROW_BACK,
            visible=False,
            icon_color=colors.WHITE,
            on_click=self.back_home
            ),
        )

        self.welcome_page = Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self.back_arrow,
                self.study,
                self.welcome_text,
                self.register_btn,
                self.sign_in,
            ]
        )

        return self.welcome_page
    