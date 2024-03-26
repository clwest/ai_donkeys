from flet import *
from services.auth_services import signup_user
from utils.colors import *

def show_signup_dialog(page, on_signup_success):
    def register(e):
        if email_input.value != "":
            if password_input.value == confirm_password_input.value and len(password_input.value) >= 5:
                # Capture the user
                email = email_input.value
                username = username_input.value
                password = password_input.value
                on_signup_success = signup_user(email, username, password)
                print(f"User {username} created an account")
                dialog.open = False
                page.update()

            else:
                error_message.value = on_signup_success.get("message", "Registration fialed, please try again")
                page.update()
        else:
            error_message.value = "Please fill in all fields"
            page.update()

    # Define the UI components for Register dialog
    username_input = TextField(label="Username", autofocus=True)
    email_input = TextField(label="Email")
    password_input = TextField(label="Password", password=True)
    confirm_password_input = TextField(label="Confirm Password", password=True)
    error_message = Text(value="", color=custom_colors["red_text"])
    register_btn = ElevatedButton(text="Register", on_click=register)

    # Create teh dialog
    dialog = AlertDialog(
        title=Text("Register"),
        content=Column([
            username_input,
            email_input,
            password_input,
            confirm_password_input,
            error_message,
            register_btn
        ],
        tight=True),
        actions=[]
    )
    page.dialog = dialog
    dialog.open = True
    page.update()