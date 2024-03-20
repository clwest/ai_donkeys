from flet import *
from utils.data import *
from utils.colors import *
# from components.sidebar import Sidebar
from services.data_store import DataStore
# from services.user_services import user_info

class DashBoard(UserControl):

    def __init__(self, page: Page):
        self.page = page
        super().__init__()

    def transfer(self, e):
        self.page.go("/transfer")

    def dashboard(self, e):
        self.page.go("/dashboard")
    
    def transaction_history(self, e):
        self.page.go("/stats/transaction-history")

    def to_security(self, e):
        self.page.go("/security")

    def account_information(self,e):
        self.page.go("/account-information")

    def chatbot(self, e):
        self.page.go("/chatbot")
    
    def docbot(self, e):
        self.page.go("/docbot")
    

    def did_mount(self):
        user_data = self.page.session.get("user")
        username = user_data['username']
        print(f"{username} has logged in at did_mount")

    
    def build(self):

        users_data = self.page.session.get("users")
        active_user = self.page.session.get("username")

        self.settings = Container(
            alignment=alignment.center,
            border_radius=10,
            bgcolor=navbar,
            on_click=self.account_information,
            content=IconButton(
                icon=icons.SETTINGS_OUTLINED,
                icon_color=colors.WHITE
            )
        )
    
        self.profile_avatar = Container(
            border_radius=20,
            padding=5,
            content=CircleAvatar(
                foreground_image_url=AVATAR_IMAGE_URL,
            )
        )
        self.notifications = Stack(
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

        self.top_row = Container(
            margin=20,
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    self.settings,
                    self.profile_avatar,
                    self.notifications

                ]
            )
        )

        self.total_balance = Text(
            "Total Balance",
            color=colors.GREY_500,
            size=16,
            text_align=TextAlign.CENTER,
            spans=[
                TextSpan(
                    text = f"\nWelcome {active_user}",
                    style=TextStyle(
                        size=30,
                        weight=FontWeight.BOLD,
                        color=colors.WHITE
                    )
                ),
                TextSpan(
                    text = f"\n4,760",
                    style=TextStyle(
                        size=30,
                        weight=FontWeight.BOLD,
                        color=colors.WHITE
                    )
                ),
                TextSpan(
                    text=" STX",
                    style=TextStyle(
                        size=30,
                        weight=FontWeight.W_300,
                        color=colors.WHITE
                    )
                )
            ]
        )

        self.month = Text(
            "This month", 
            text_align=TextAlign.LEFT, 
            color=colors.GREY_500, 
            size=15
            )
        self.income = Row(
            controls=[
                Image(
                    src=INCOME_VECTOR_URL,
                    height=25,
                    width=25
                ),
                Text("$3,736",
                color=colors.WHITE,
                weight=FontWeight.BOLD,
                text_align=TextAlign.LEFT,
                size=18,
                spans= [
                    TextSpan(
                        text=".20",
                        style=TextStyle(
                            weight=FontWeight.W_300,
                            color=colors.WHITE
                        )
                    )
                ]
                )
            ]
        )
        self.expenditure = Row(
            controls=[
                Image(
                    src=EXPENDITURE_VECTOR_URL,
                    height=25,
                    width=25
                ),
                Text("$2,710",
                color=colors.WHITE,
                weight=FontWeight.BOLD,
                size=18,
                text_align=TextAlign.CENTER,
                spans=[
                    TextSpan(
                        text=".25",
                        style=TextStyle(
                            weight=FontWeight.W_300,
                            color=colors.WHITE
                        )
                    )
                ]
                )
            ]
        )

        self.expenses = Container(
            margin=20,
            content=Column(
                controls=[
                    self.month,
                    self.income,
                    self.expenditure
                ]
            )
        )

        self.options = ResponsiveRow(
            controls=[
                Container(
                    col={"xs": 4},
                    alignment=alignment.center,
                    content=Column(
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Container(
                                width=90,
                                border_radius=10,
                                bgcolor=colors.GREY_900,
                                padding=10,
                                alignment=alignment.center,
                                content=Column(
                                    spacing=0,
                                    controls=[
                                        Image(src=BACK_ARROW_IMAGE_URL),
                                        Image(src=FORWARD_ARROW_IMAGE_URL)
                                    ]
                                ),
                                on_click=self.transfer,
                            ),
                            Text("Transfer", color=colors.GREY_500, size=14)
                        ]
                    )
                )
            ]
        )

        self.options.controls.extend(
            [
                Container(
                    col={"xs": 4},
                    on_click=self.transfer,
                    alignment=alignment.center,
                    content=Column(
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Container(
                                width=90,
                                border_radius=10,
                                bgcolor=colors.GREY_900,
                                padding=5,
                                content=Text("%", text_align=TextAlign.CENTER, color=colors.GREY_400, weight=FontWeight.BOLD, size=20),
                            ),
                            Text("Deposit", text_align=TextAlign.CENTER, color=colors.GREY_500, size=13)
                        ]
                    )
                ),
                Container(
                    col={"xs": 4},
                    alignment=alignment.center,
                    content=Column(
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Container(
                                width=90,
                                border_radius=10,
                                bgcolor=colors.GREY_900,
                                content=IconButton(
                                    icon=icons.SECURITY,
                                    icon_color=colors.GREY_400,
                                    on_click=self.to_security
                                ),
                            ),
                            Text("Security", text_align=TextAlign.CENTER, color=colors.GREY_500, size=13)
                        ]
                    )
                )
            ]
        )

        for option in OPTIONS:
            option_container = Container(
                col={"xs": 4},
                alignment=alignment.center,
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Container(
                            width=90,
                            border_radius=10,
                            bgcolor=colors.GREY_900,
                            content=IconButton(
                                icon=option[0],
                                icon_color=colors.GREY_400
                            ),
                        ),
                        Text(option[-1],text_align=TextAlign.CENTER, color=colors.GREY_500, size=13)
                    ]
                )
            )
            self.options.controls.append(option_container)
        
        self.nav_bar = Container(
            bgcolor=colors.GREY_900,
            border_radius=border_radius.only(top_left=20, top_right=20),
            height=200,
            alignment=alignment.top_center,
            padding=padding.symmetric(horizontal=30, vertical=20),
            content=Row(
                spacing=90,
                controls=[
                    Container(
                        col={"xs": 4},
                        width=60,
                        border_radius=10,
                        gradient=LinearGradient(
                            colors=mutli_color,
                            begin=alignment.top_right,
                            end=alignment.top_left,
                        ),
                        content=IconButton(
                            icon=icons.ACCOUNT_BALANCE,
                            icon_color=colors.WHITE,
                            on_click=self.dashboard
                        )
                    ),
                    Container(
                        col={"xs": 4},
                        width=60,
                        border_radius=10,
                        content=IconButton(
                            icon=icons.PERSON_SEARCH,
                            icon_color=colors.WHITE,
                            on_click=self.docbot
                        ),
                        
                    ),
                    Container(
                        col={"xs": 4},
                        width=60,
                        border_radius=10,
                        content=IconButton(
                            icon=icons.CHAT_BUBBLE_OUTLINED,
                            icon_color=colors.WHITE,
                            on_click=self.chatbot
                        )
                    ),
                ]
            )
        )

        self.page_controls = Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=30,
            controls=[               
                self.top_row,
                self.total_balance,
                self.expenses,
                self.options,
                self.nav_bar
            ]
        )
        return self.page_controls