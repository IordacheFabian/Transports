from transports import *
from transporters import *

# database imports
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient

load_dotenv(find_dotenv())


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=WHITE)
        self.geometry('1600x900')
        self.title('Transports')
        self.iconbitmap('images/icon.ico')

        import ctypes

        my_app_id = 'App'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

        self.resizable(False, False)

        self.first_frame = FirstFrame(self, 0, 0, 1, 1, WHITE, 0)

        # database
        load_dotenv(find_dotenv())
        self.connection_string = 'mongodb://localhost:27017'
        self.client = MongoClient(self.connection_string)

        # create database
        test_db = self.client.test
        self.collections = test_db.list_collection_names()

        self.mainloop()


class FirstFrame(ctk.CTkFrame):
    def __init__(self, parent, rel_x, rel_y, rel_width, rel_height, color, corner_radius):

        # image
        my_image = Image.open(LOGO)

        # database
        connection_string = 'mongodb://localhost:27017'
        client = MongoClient(connection_string)

        # create database
        transport_app = client.transport_app
        self.person = transport_app.person
        self.responsible = transport_app.responsible

        # setup
        super().__init__(parent, fg_color=color, corner_radius=corner_radius, border_width=0)

        label = ctk.CTkLabel(
            self,
            text='',
            image=ctk.CTkImage(
                light_image=my_image,
                dark_image=my_image,
                size=(250, 120)
            ))

        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, uniform='a')
        self.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        Label(self, 'Login to Your Account', 'black', 2, 0, 3, 80)

        self.email = Entry(self, 5, 0, 'Email', pas=False)
        self.password = Entry(self, 6, 0, 'Password', pass_but=True)

        # self.button = Button(self, 'Log In', WHITE, LIGHT_GREEN, 7, 1, HOVER_GREEN)
        self.button = ctk.CTkButton(self,
                                    text='Login',
                                    text_color=WHITE,
                                    fg_color=LIGHT_GREEN,
                                    width=150,
                                    height=50,
                                    corner_radius=100,
                                    hover_color=HOVER_GREEN,
                                    font=ctk.CTkFont(family=FONT, size=20, weight='bold'),
                                    command=self.sign_in)

        self.button.grid(row=7, column=1)

        self.last_frame = LastFrame(self, 0.6, 0.01, 0.39, 0.98, LIGHT_GREEN, 30)
        self.error = False
        self.color_index = 15

        # self.sign_in()

        label.grid(row=0, column=0, sticky='w')
        self.place(relx=rel_x, rely=rel_y, relwidth=rel_width, relheight=rel_height)

    def sign_in(self):
        email1 = self.person.find_one({"email": str(self.email.get())})
        password1 = self.person.find_one({"password": str(self.password.get())})
        email2 = self.responsible.find_one({"email": str(self.email.get())})
        password2 = self.responsible.find_one({"password": str(self.password.get())})
        var = str(self.email.get())
        if email1 and password1:
            for widget in self.winfo_children():
                widget.destroy()

            InnerFrameT(self, var)
        elif email2 and password2:
            for widget in self.winfo_children():
                widget.destroy()

            InnerFrame(self, var)
        else:
            self.error_animation()

    def error_animation(self):
        self.error = True
        if self.color_index > 0:
            self.color_index -= 1
            border_color = f"#F{COLOR_RANGE[self.color_index]}{COLOR_RANGE[self.color_index]}"
            text_color = f"#{COLOR_RANGE[-self.color_index - 1]}00"
            self.email.configure(border_color=border_color, text_color=text_color)
            self.password.configure(border_color=border_color, text_color=text_color)
            self.after(40, self.error_animation)
        else:
            self.remove_error()

    def remove_error(self):
        if self.error:
            self.email.configure(border_color=WHITE, text_color='black')
            self.password.configure(border_color=WHITE, text_color='black')
            self.color_index = 15


class LastFrame(ctk.CTkFrame):
    def __init__(self, parent, rel_x, rel_y, rel_width, rel_height, color, corner_radius):
        super().__init__(parent, fg_color=color, corner_radius=corner_radius, border_width=0)

        # layout
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6), uniform='a', weight=1)
        self.columnconfigure(0, weight=1, uniform='a')

        label_1 = Label(self, 'New here?', WHITE, 2, 0, 1, 60)
        label_2 = Label(self, 'Sign up and discover a great\n amount of new opportunities!', WHITE, 3, 0, 3, 20)

        # button = Button(self, 'Sign In', 'black', WHITE, 4, 0, hover_col=HOVER_WHITE)
        button = ctk.CTkButton(self,
                               text='Sign In',
                               text_color='black',
                               fg_color=WHITE,
                               width=150,
                               height=50,
                               corner_radius=100,
                               hover_color=HOVER_WHITE,
                               font=ctk.CTkFont(family=FONT, size=20, weight='bold'),
                               command=self.login)
        button.grid(row=4, column=0)

        # database
        connection_string = 'mongodb://localhost:27017'
        client = MongoClient(connection_string)

        # create database
        transport_app = client.transport_app
        self.person = transport_app.person
        self.responsible = transport_app.responsible

        self.widgets_list = [label_1, label_2, button]

        self.place(relx=rel_x, rely=rel_y, relwidth=rel_width, relheight=rel_height)

    def login(self):
        for index, i in enumerate(self.widgets_list):
            i.destroy()

        self.grid_forget()

        label_1 = ctk.CTkLabel(self, text='Login', font=ctk.CTkFont(family=FONT, size=50, weight='bold'))
        label_1.pack(pady=100)

        first_name = SignInEntry(self, placeholder_text='First name', fg_color=WHITE, width=300, height=40,
                                 corner_radius=100, text_color='black', border_width=0)

        last_name = SignInEntry(self, placeholder_text='Last name', fg_color=WHITE, width=300, height=40,
                                corner_radius=100, text_color='black', border_width=0)

        email = SignInEntry(self, placeholder_text='Email', fg_color=WHITE, width=300, height=40,
                            corner_radius=100, text_color='black', border_width=0)

        password = SignInEntry(self, placeholder_text='Password', fg_color=WHITE, width=300, height=40,
                               corner_radius=100, text_color='black', border_width=0)

        age = SignInEntry(self, placeholder_text='Age', fg_color=WHITE, width=300, height=40,
                          corner_radius=100, text_color='black', border_width=0)

        phone = SignInEntry(self, placeholder_text='Phone', fg_color=WHITE, width=300, height=40,
                            corner_radius=100, text_color='black', border_width=0)

        address = SignInEntry(self, placeholder_text='Address', fg_color=WHITE, width=300, height=40,
                              corner_radius=100, text_color='black', border_width=0)

        sign_as_res = ctk.CTkButton(self,
                                    text='SignIn as Responsible',
                                    text_color='black',
                                    fg_color=WHITE,
                                    width=150,
                                    height=50,
                                    corner_radius=100,
                                    hover_color=HOVER_WHITE,
                                    font=ctk.CTkFont(family=FONT, size=20, weight='bold'))
        sign_as_res.pack(pady=30, padx=40, side='left')

        sign_as_tr = ctk.CTkButton(
            self,
            text='SignIn as transporter',
            text_color='black',
            fg_color=WHITE,
            width=150,
            height=50,
            corner_radius=100,
            hover_color=HOVER_WHITE,
            command=lambda: self.add_to_data_base(first_name, last_name, email, password, age, phone, address),
            font=ctk.CTkFont(family=FONT, size=20, weight='bold'))
        sign_as_tr.pack(pady=30, padx=40, side='right')

    def add_to_data_base(self, fn, ln, email, password, age, phone, address):
        document = {
            "first_name": fn.get(),
            "last_name": ln.get(),
            "email": email.get(),
            "password": password.get(),
            "age": age.get(),
            "phone": phone.get(),
            "address": address.get()
        }

        self.person.insert_one(document)


class Button(ctk.CTkButton):
    def __init__(self, parent, text, text_color, color, row, column, hover_col, column_span=1):
        super().__init__(
            parent,
            text=text,
            text_color=text_color,
            fg_color=color,
            width=150,
            height=50,
            corner_radius=100,
            hover_color=hover_col,
            font=ctk.CTkFont(family=FONT, size=20, weight='bold'),
            command=self.verify
        )

        # variable
        self.ver = False

        self.grid(row=row, column=column, columnspan=column_span)

    def verify(self):
        self.ver = True


class Entry(ctk.CTkEntry):
    def __init__(self, parent, row, column, text, pas=True, pass_but=False, borders_col=WHITE):

        # image
        self.close_eye = Image.open(CLOSE_EYE)
        self.open_eye = Image.open(OPEN_EYE)

        # /config
        super().__init__(
            parent,
            fg_color=GRAY,
            placeholder_text=text,
            placeholder_text_color='#707070',
            width=500,
            height=60,
            corner_radius=100,
            text_color='black',
            border_width=3,
            border_color=borders_col
        )

        if pas:
            self.configure(show='*')

        # eye button and var
        self.switch_eye = True

        if pass_but:
            self.button = ctk.CTkButton(
                parent,
                text='',
                image=ctk.CTkImage(
                    light_image=self.close_eye,
                    dark_image=self.close_eye,
                    size=(20, 20)),
                width=20,
                height=20,
                fg_color=GRAY,
                corner_radius=0,
                hover_color=HOVER_GRAY,
                command=self.eye_command,
            )
            self.button.place(relx=0.43, rely=0.634)

        self.grid(row=row, column=column, columnspan=3)

    def eye_command(self):
        if self.switch_eye:
            self.button.configure(
                image=ctk.CTkImage(
                    light_image=self.open_eye,
                    dark_image=self.open_eye,
                    size=(20, 20)),
            )

            self.configure(show='')
            self.switch_eye = False
        else:
            self.button.configure(image=ctk.CTkImage(
                light_image=self.close_eye,
                dark_image=self.close_eye,
                size=(20, 20)), )

            self.configure(show='*')
            self.switch_eye = True


class Label(ctk.CTkLabel):
    def __init__(self, parent, text, text_color, row, column, column_span, size):
        super().__init__(
            parent,
            text=text,
            font=ctk.CTkFont(family=FONT, size=size, weight='bold'),
            text_color=text_color
        )

        self.grid(row=row, column=column, columnspan=column_span)


class SignInEntry(ctk.CTkEntry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.pack(pady=10)


App()
