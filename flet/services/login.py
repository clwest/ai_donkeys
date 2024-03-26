   # TODO: Still need to add error handling and error messages
from flet import *
from services.auth_services import login_user
from services.register import show_signup_dialog
from utils.colors import *


def show_login_dialog(page, on_login_success):
    def login(e):
        if username_input.value and password_input.value:
            login_result = login_user(username_input.value, password_input.value)
            
            if login_result.get("success"):
                # Handle successful log
                jwt_token = login_result.get("token")
                user = login_result.get("user")
                username = login_result.get("username")

                # Saving JWT and username in session
                page.session.set("jwt_token", jwt_token)
                page.session.set("user", user)
                page.session.set("username", username)

                
                on_login_success(login_result)
                print(f"User {username} has logged in")
                dialog.open = False
                page.update()
            else:
                # update the page/dialog with an error message
                error_msg.value = login_result.get("message", "Login failed, please try again")
                page.update()
        else:
            # Update the page/dialog with an error message for empty fileds
            error_msg.value = "Please fill in all fields"
            page.update()
    
    # Define UI components for the login dialog
    username_input = TextField(label="Username", autofocus=True)
    password_input = TextField(label="Password", password=True)
    error_msg = Text(value="", color=custom_colors["red_text"])
    login_btn = ElevatedButton(text="Login", on_click=login)

    # Create the dialog
    dialog = AlertDialog(
        title=Text("Login"),
        content=Column([
            username_input,
            password_input,
            error_msg,
            login_btn

        ],
        tight=True
        ),
        actions=[]
    )

    page.dialog = dialog
    dialog.open = True
    page.update()
    
