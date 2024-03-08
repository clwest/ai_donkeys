from flet import *
from utils.data import *
from utils.colors import *

class Chatbot(UserControl):
    
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.prompts = []

    def home(self, e):
        self.page.go("/")

        
    def new_chat(self, e):
        chat = Row(
            controls=[
                Icon(icons.MODE_COMMENT_OUTLINED, color=USER_CHATBOX),
                Text("New Chat", color=USER_CHATBOX)
            ]
        )
        self.chat_history.controls.insert(0, chat)
        self.update()

    def prompt_hover(self, e):
        # Data property --> True as string
        # Data property --> False as string

        # Change background color of propmts
        e.control.bgcolor = colors.SURFACE_VARIANT if e.data == "true" else navbar

        # Make icon visible
        # control = Container control
        # content = Row content
        e.control.content.controls[-1].visible = True if e.data == "true" else False
        self.update()

    def close_sidebar(self, e):
        self.left_navbar.visible = False
        self.text_interface.col = {"lg": 2}
        self.applogo.visible = True
        self.update()

    def open_sidebar(self, e):
        self.left_navbar.visible = True
        self.text_interface.col = {"lg": 10}
        self.sidebar.visible = False
        self.update()

    def send_message(self, e):
        pass

    def input_on_change(self, e):
        self.send_message_btn.icon_color = colors.WHITE if self.input.value == "" else SLATE
        self.update()

    def submit(self, e):
        self.applogo.visible = False
        self.responsive_prompt.visible = False
        self.conversations.visible = True   

        if isinstance(e, ContainerTapEvent):
            # Predefined prompts on page
            prompt_value = f"{e.control.content.controls[0].value} {e.control.content.controls[0].spans[0].text[1:]}"
            message = Text(value=prompt_value)
        else:
            # User query
            input_value = e.control.value
            message = Text(value=input_value)
        
        # Create query
        query_prompt = Container(
            alignment=alignment.top_left,
            padding=padding.symmetric(horizontal=40, vertical=20),
            bgcolor=USER_CHATBOX,
            content=Row(
                wrap=True,
                controls=[
                    Image(
                        src="assets/img/poker.png",
                        height=25,
                        width=25
                    ),
                    message
                ]
            )
        )

        self.input.value = ""
        self.conversations.controls.append(query_prompt)
        self.update()
        # *** Call Chatbot API ***
        chatbot_response = chatgpt_response(message.value)

        response = Container(
            alignment=alignment.top_left,
            bgcolor=AI_CHATBOX,
            padding=padding.symmetric(horizontal=30, vertical=20),
            content=Row(
                wrap=True,
                controls=[
                    Image(
                        src="assets/img/study.png",
                        height=25,
                        width=25,
                    ),
                    Text(value=chatbot_response)
                ]
            )
        )

        self.conversations.controls.extend(response)
        self.update()

    def build(self):
        self.action_buttons = Row(
            controls=[
                Container(
                    padding=padding.only(left=5, top=5, bottom=5, right=10),
                    border=border.all(1, red_text),
                    border_radius=10,
                    content=TextButton(
                        text="New Chat",
                        icon=icons.CHAT_BUBBLE_OUTLINE_OUTLINED,
                        icon_color="black",
                        style=ButtonStyle(
                            color=colors.WHITE54,
                        ),
                        on_click=self.new_chat
                    )
                ),
                Container(
                    padding=padding.symmetric(vertical=5),
                    border=border.all(1, red_text),
                    border_radius=10,
                    on_click=self.close_sidebar,
                    content=TextButton(
                        icon=icons.VIEW_SIDEBAR_OUTLINED,
                        icon_color="black",
                        style=ButtonStyle(
                            color=colors.WHITE54,
                        )
                    ),
                    tooltip="Close sidebar"
                )
            ]
        )
        self.chat_history = ListView(
            padding=padding.only(top=8),
            width=275,
            height=450,
            expand=True,
            spacing=20,
        )

        self.bottom_row = Column(
            controls=[
                Divider(
                    thickness=1, height=1, color=colors.GREY_800
                ),
                Row(
                    controls=[
                        Icon(icons.TABLE_ROWS_OUTLINED, color="black"),
                        Text("Home", size=15, weight=FontWeight.W_300)
                    ]
                ),
                Row(
                    controls=[
                        # Need to make dynamic img and username
                        Image(
                            src="assets/img/poker.png",
                            width=25,
                            height=25
                        ),
                        Text("Donkey King", size=15, weight=FontWeight.W_400)
                    ]
                )
            ]
        )

        self.applogo = Container(
            margin=margin.only(bottom=250, top=40, left=345),
            content=Text(
                "Donkey Betz",
                color=colors.GREY_500,
                weight=FontWeight.BOLD,
                size=40
            )
        )

        # For loop to create prompt buttons on page
        for button in DEFAULT_PROMPTS:
            prompt = Container(
                padding=5,
                border=border.all(1, color=colors.GREY_500),
                border_radius=10,
                height=55,
                width=120,
                col={"xs": 4, "sm": 6, "lg": 8, "xl": 10},
                on_click=self.submit,
                on_hover=self.prompt_hover,
                content=Row(
                    controls=[
                        Text(
                            value=button[0],
                            color=SLATE,
                            weight=FontWeight.BOLD,
                            size=15,
                            spans=[
                                TextSpan(
                                    text=button[1],
                                    style=TextStyle(
                                        size=12,
                                        weight=FontWeight.NORMAL
                                    )
                                )
                            ]
                        ),
                        Icon(icons.SEND_OUTLINED, color=colors.GREY_600, visible=False),
                    ]
                )
            )
            self.prompts.append(prompt)
        
        self.responsive_prompt = ResponsiveRow(
            controls=self.prompts
        )

        self.conversations = ListView(
            height=600,
            width=1000,
            expand=True,
            visible=False,
            spacing=20
        )

        self.response = Container(
            content=Row(
                controls=[
                    Image(
                        src="assests/img/study.png",
                        height=25,
                        width=25
                    ),
                ]
            )
        )

        self.sidebar = Container(
            border=border.all(1, red_text),
            border_radius=10,
            on_click=self.open_sidebar,
            content=TextButton(
                icon=icons.VIEW_SIDEBAR_OUTLINED,
                icon_color="black",
                style=ButtonStyle(
                    color=colors.WHITE54,
                ),
                tooltip="Open Sidebar"
            ),
            visible=False
        )

        self.input = TextField(
            hint_text="Start chat",
            border=InputBorder.NONE,
            color=colors.GREY_500,
            cursor_color="grey",
            shift_enter=True,
            multiline=True,
            on_change=self.input_on_change,
            on_submit=self.submit,
            filled=True
        )

        self.send_message_btn = IconButton(
            icon=icons.SEND_OUTLINED,
            icon_color=colors.GREY_500,
            tooltip="Start chat",
        )

        self.send_stack = Stack(
            controls=[
                Container(
                    height=60,
                    margin=margin.only(top=5),
                    padding=padding.symmetric(horizontal=15, vertical=5),
                    border_radius=10,
                    content=self.input,
                ),
                Container(
                    content=self.send_message_btn,
                    margin=margin.only(left=865, top=15, right=10),
                    height=20,
                    width=20,
                    padding=2,
                    on_click=self.send_message
                )
            ]
        )

        self.left_navbar = Container(
            bgcolor=SLATE,
            padding=3,
            width=450,
            height=785,
            col={"lg": 2},
            content=Column(
                expand=True,
                alignment=MainAxisAlignment.START,
                controls=[
                    self.action_buttons,
                    self.chat_history,
                    self.bottom_row
                ]
            )
        )

        self.text_interface = Container(
            height=785,
            width=1000,
            padding=padding.symmetric(vertical=35, horizontal=100),
            col={"lg": 10},
            bgcolor=h3,
            content=Column(
                controls=[
                    self.sidebar,
                    self.applogo,
                    self.responsive_prompt,
                    self.conversations,
                    self.send_stack
                ]
            )
        )

        self.top_row = ResponsiveRow(
            alignment=MainAxisAlignment.START,
            controls=[
                self.left_navbar,
                self.text_interface
            ]
        )

        return self.top_row

        # self.page_controls = Column(
        #     alignment=MainAxisAlignment.CENTER,
        #     horizontal_alignment=CrossAxisAlignment.CENTER,
        #     spacing=30,
        #     controls=[
        #         self.left_navbar,
        #         self.text_interface
        #     ]
        # )

        # return self.page_controls