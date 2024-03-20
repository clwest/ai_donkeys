from flet import *
from utils.data import *
from utils.colors import *

class DocBot(UserControl):

    def __init__(self, page: Page):
        super().__init__()

        self.page = page
        self.title = "Docs Bot"

    def dashboard(self, e):
        self.page.go("/dashboard")
    
    def build(self):

        self.top = Container(
            margin=20,
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Container(
                        alignment=alignment.top_left,
                        content=IconButton(
                            icon=icons.ARROW_BACK,
                            icon_color=colors.WHITE,
                            on_click=self.dashboard
                        )
                    ),
                    Text("Enter a URL", weight=FontWeight.W_500),
                ]
            )
        )
        self.update()

        self.page_control = Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self.top
            ]
        )

        return self.page_control