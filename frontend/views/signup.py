from flet import *
from utils.data import *
from utils.colors import *
import random

class SignUp(UserControl):

    def __init__(self, page: Page):
        self.page = page
        super().__init__()

    def to_onboarding(self, e):
        print("click")
        self.page.go("/")

    def confirm(self, e):
        # self.page.client_storage.clear()
        if self.email.content.value != "":
            if self.password.content.value == self.confirm_password.content.value and len(self.password.content.value) >= 5:
                user_instance = {
                    "email": self.email.content.value,
                    "username": self.username.content.value,
                    "password": self.password.content.value,
                    # Add wallets for Eth, Stx, and FLOW
                    "account_no": str(random.randrange(1_000_000_000_000_000, 2_000_000_000_000_000))
                }
                if self.page.client_storage.contains_key("users"):
                    # Adding new users  
                    user_data = self.page.client_storage.get("users")
                    user_data.append(user_instance)
                    self.page.client_storage.set("users", user_data)

                    # Adding accounts/wallets
                    accounts_details = self.page.client_storage.get("wallet_address")
                    accounts_details[self.username.content.value] = user_instance["account_no"]
                    self.page.client_storage.set("wallet_address", accounts_details)
                else:
                    self.page.client_storage.set("users", [user_instance])
                    self.page.client_storage.set("wallet_address", {self.username.content.value : user_instance["account_no"]})

                print(self.page.client_storage.get("users"))
                print(self.page.client_storage.get("wallet_address"))
                self.page.go("/signup/success")

    def build(self):
        self.back_arrow=Container(
            alignment=alignment.top_left,
            content=IconButton(
                icon=icons.ARROW_BACK,
                icon_color=colors.WHITE,
                on_click=self.to_onboarding,
            ),
        )
        self.email_password=Container(
            margin=margin.only(top=0),
            content=Text(
                "Create a new account",
                color=colors.WHITE,
                size=24,
                weight=FontWeight.BOLD,
                spans=[
                    TextSpan(
                        "\nPlease fill out the following",
                        style=TextStyle(
                            size=14,
                            weight=FontWeight.W_900,
                        )
                    )
                ]
            )
        )

        self.email_label = Text("Email Address", size = 14, color= colors.WHITE, weight= FontWeight.W_300)

        self.username_label = Text("Username", size = 14, color= colors.WHITE, weight= FontWeight.W_300)

        self.password_label = Text("Enter Password", size = 14, color= colors.WHITE, weight= FontWeight.W_300)

        self.confirm_password_label = Text("Confirm Password", size = 14, color= colors.WHITE, weight= FontWeight.W_300)

        self.email = Container(
            bgcolor=colors.GREY_500,
            border_radius=10,
            width=350,
            content=TextField(
                border=InputBorder.NONE,
                cursor_color=colors.BLACK,
                color=h3
            )
        )

        self.username = Container(
            bgcolor=colors.GREY_500,
            border_radius=10,
            width=350,
            content=TextField(
                border=InputBorder.NONE,
                cursor_color=colors.BLACK,
                color=h3
            )
        )

        self.password = Container(
            bgcolor=colors.GREY_500,
            border_radius=10,
            width=350,
            content=TextField(
                border=InputBorder.NONE,
                cursor_color=colors.BLACK,
                color=h3,
                password=True
            )
        )

        self.confirm_password = Container(
           bgcolor=colors.GREY_500,
           border_radius=10,
           width=350,
           content=TextField(
            border=InputBorder.NONE,
            cursor_color=colors.BLACK,
            color=h3,
            password=True,
           )
        )
        self.signup_btn = Container(
            on_click=self.confirm,
            margin=margin.only(top=50, bottom=20),
            content=ElevatedButton(
                style=ButtonStyle(
                    color=colors.WHITE,
                    bgcolor=SLATE,
                    shape=RoundedRectangleBorder(radius=10),
                ),
                content=Container(
                    alignment=alignment.center,
                    padding=10,
                    height=50,
                    width=100,
                    content=Text(
                        "Sign Up",
                        size=16,
                        weight=FontWeight.W_700
                        )
                )
            )
        )
        return Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self.back_arrow,
                self.email_password,
                self.email_label,
                self.email,
                self.username_label,
                self.username,
                self.password_label,
                self.password,
                self.confirm_password_label,
                self.confirm_password,
                self.signup_btn
            ]
        )
