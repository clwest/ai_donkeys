from flet import *
from utils.data import *
from utils.colors import *
from services.auth_services import login_user

class Login(UserControl):
    def __init__(self, page: Page):
        self.page = page
        super().__init__()

    def home(self, e):
        self.page.go("/")

    # TODO: Still need to add error handling and error messages
    def login(self, e):
        if self.username.content.value != "" and self.password.content.value != "":
            username = self.username.content.value
            password = self.password.content.value

            login_result = login_user(username, password)
           
            if login_result.get("success"):
                jwt_token = login_result.get("token")
                user = login_result.get("user")
                username = login_result.get("username")
                
                # Saving the JWT and username in session storage
                self.page.session.set("jwt_token", jwt_token)
                self.page.session.set("user", user)
                self.page.session.set("username", username)
                self.page.go("/dashboard")
            else:
                error_message = login_result.get("message", "Login failed, please try again")
        else:
            pass
        
    def build(self):
        self.back_arrow = Container(
            alignment= alignment.top_left,
            content = IconButton(
                icon= icons.ARROW_BACK,
                icon_color=colors.WHITE,
                on_click = self.home,
            ),
        )

        self.image = Container(
            margin= margin.symmetric(horizontal=80, vertical=50),
            content= Image(
                src = LOGIN_IMAGE_URL
            )
        )

        self.username_label = Text("Username", size = 14, color= colors.WHITE, weight= FontWeight.W_300)

        self.password_label = Text("Enter Password", size = 14, color= colors.WHITE, weight= FontWeight.W_300)
        
        self.username = Container(
            bgcolor= colors.WHITE,
            border_radius= 10,
            content= TextField(
                color=colors.BLACK,
                border= InputBorder.NONE,
                cursor_color= colors.BLACK
            )
        )

        self.password = Container(
            bgcolor= colors.WHITE,
            border_radius= 10,
            content= TextField(
                color= colors.BLACK,
                border= InputBorder.NONE,
                cursor_color= colors.BLACK,
                password= True,
            )
        )

        self.login_btn = Container(
            on_click= self.login,
            margin= margin.only(top=120, bottom=20, left=70),
            content= ElevatedButton(
                style= ButtonStyle(
                    color= colors.WHITE,
                    bgcolor=custom_colors["slate"],
                    shape=RoundedRectangleBorder(radius=10),
                ),
                content= Container(
                    alignment= alignment.center,
                    padding= 10,
                    height= 50,
                    width= 100,
                    content= Text("Login",
                                  size=16,
                                  weight= FontWeight.W_700
                        )
                )
            )
        )
        self.page_controls = Column(
            alignment= MainAxisAlignment.CENTER,
            horizontal_alignment= CrossAxisAlignment.START,
            controls= [
                Row(
                    spacing= 200,
                    controls=[
                        self.back_arrow
                    ]
                ),
                self.image,
                self.username_label,
                self.username,
                self.password_label,
                self.password,
                self.login_btn
            ]
        )

        return self.page_controls