# from flet import *
# from utils.data import *
# from utils.colors import *
# from views.login import Login

# class Navbar(UserControl):
#     def __init__(self, page: Page):
#         self.page = page
#         super().__init__()

#         self.user_auth_button = PopupMenuItem(text="Sign in\nRegister", on_click=self.navigate_to_login)

#         self.appbar_items = [
#             self.user_auth_button,
#             PopupMenuButton(), # Divider
#         ]

#         self.appbar = AppBar(
#             leading=Icon(icons.CASTLE, color="black"),
#             leading_width=100,
#             title=Text("Donkey Betz AI", size=32, text_align="start", color=custom_colors["cyan"]),
#             center_title=False,
#             toolbar_height=75,
#             bgcolor=colors.CYAN_500,
#             actions=[
#                 Container(
#                     content=PopupMenuButton(items=self.appbar_items),
#                     margin=margin.only(left=50, right=25)
#                 )
#             ]
#         )
#         print(f"Debugging self page:", page)
#         print(f"Appbar initialized: ", self.appbar)
#         # Assign the AppBar to the page

#         self.page.appbar = self.appbar
#         # print(f"Page appbar after assignment", self.page.appbar)
#         # self.page.update()
    
    # def navigate_to_login(self, e):
    #     self.page.go("/login")


