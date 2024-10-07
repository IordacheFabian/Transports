# import customtkinter as ctk
from settings import *
from PIL import Image
from tkcalendar import Calendar
# from ttkbootstrap.toast import ToastNotification
from fpdf import FPDF
from tkinter import filedialog
from tkinter import messagebox
import tkintermapview
from geopy.geocoders import Nominatim
from map import *
from qr import *
from random import choice

# database imports
from dotenv import load_dotenv, find_dotenv
import pprint
from pymongo import MongoClient

load_dotenv(find_dotenv())


# class Testing(ctk.CTk):
#     def __init__(self):
#         super().__init__(fg_color=WHITE)
#         self.title('Testing')
#         self.geometry('1600x900')
#         # self.eval('tk::PlaceWindow . center')
#         x = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 10
#         y = (self.winfo_screenheight() - self.winfo_reqheight()) / 10
#         self.geometry("+%d+%d" % (x, y))
#
#         # self.configure(bg='grey15')
#         # self.attributes('-transparentcolor', 'grey15')
#         # self.overrideredirect(True)
#
#         # self.resizable(False, False)
#         self.minsize(1600, 900)
#         InnerFrame(self, 'smecheruion69@gmail.com')
#
#         self.mainloop()


class InnerFrame(ctk.CTkFrame):
    def __init__(self, parent, emails):
        super().__init__(parent, fg_color=WHITE, corner_radius=40)

        # database
        connection_string = 'mongodb://localhost:27017'
        client = MongoClient(connection_string)

        transport_app = client.transport_app
        self.person = transport_app.person
        self.transport = transport_app.transport
        self.responsible = transport_app.responsible
        self.location = transport_app.location
        self.printer = pprint.PrettyPrinter()

        # variables
        self.home_b = False
        self.profile_b = True
        self.filter_b = True
        self.create_transport_b = True
        self.map_b = True
        self.qr_b = True
        self.table_view = []
        self.emails = emails
        self.avatar = choice(docs)

        # logo
        self.create_logo()

        # scrollable frame setup
        self.x = (1600 - (1500 - 100)) / 2
        self.y = (900 - 750) / 2
        self.scrollable_frame = ScrollableFrame(self, self.x, self.y, 'start')
        # self.profile_frame = ProfileFrame(self, self.x, self.y)
        # self.profile_frame.place_forget()

        # layouts
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,), weight=1, uniform='a')
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17), weight=1, uniform='a')

        # widgets
        self.create_buttons()
        SearchBar(self)

        self.place(relx=0, rely=0, relwidth=1, relheight=1)

    def create_buttons(self):
        self.home_btn = WidgetsButton(
            self,
            text='',
            fg_color=WHITE,
            image=HOME_BLACK_CTk,
            hover_color=LIGHT_GRAY,
            command=self.show_home,
            width=40, height=40, row=4, column=0)

        self.profile_btn = WidgetsButton(
            self,
            text='',
            fg_color=WHITE,
            image=PROFILE_CTk,
            hover_color=LIGHT_GRAY,
            width=40, height=40, row=5, column=0, command=self.show_profile)

        self.qr_btn = WidgetsButton(
            self,
            text='',
            fg_color=WHITE,
            image=QR_IMAGE_CTk,
            hover_color=LIGHT_GRAY,
            command=self.show_qr,
            width=40, height=40, row=6, column=0)

        self.settings_btn = WidgetsButton(
            self,
            text='',
            fg_color=WHITE,
            image=SETTINGS_IMAGE_CTk,
            hover_color=LIGHT_GRAY,
            width=40, height=40, row=7, column=0)

        self.filters_btn = WidgetsButton(
            self,
            text='Filters',
            text_color='black',
            fg_color=WHITE,
            image=FILTERS,
            hover_color=LIGHT_GRAY,
            command=self.show_filters,
            width=40, height=40, row=12, column=0, column_span=2, padx=13, sticky='w')

        self.create_transport_btn = WidgetsButton(
            self,
            text='',
            text_color='black',
            fg_color=WHITE,
            image=CREATE_TRANSPORT_IMAGE,
            hover_color=LIGHT_GRAY,
            command=self.show_create_transport,
            width=40, height=40, row=8, column=0)

        self.show_map_btn = WidgetsButton(
            self,
            text='',
            text_color='black',
            fg_color=WHITE,
            image=MAP,
            hover_color=LIGHT_GRAY,
            command=self.show_map,
            width=40, height=40, row=9, column=0)

    def create_logo(self):
        logo = Image.open(LOGO)
        logo_ctk = ctk.CTkImage(
            light_image=logo,
            dark_image=logo,
            size=(90, 60)
        )

        ctk.CTkLabel(self, text='', image=logo_ctk).grid(row=0, column=0, sticky='nsew')

    def show_profile(self):
        if self.profile_b:
            self.profile_frame = ProfileFrame(self, self.x, self.y, self.avatar)

            self.datas()

            self.profile_frame.animate()
            self.home_b = True
            self.profile_b = False
            self.filter_b = True
            self.create_transport_b = True
            self.map_b = True
            self.qr_b = True

    def datas(self):
        count = self.responsible.find({"email": self.emails}, {'_id': 0, 'first_name': 1, 'last_name': 1})
        first_name = self.responsible.find({"email": self.emails}, {'_id': 0, 'first_name': 1})
        last_name = self.responsible.find({"email": self.emails}, {'_id': 0, 'last_name': 1})
        phone = self.responsible.find({"email": self.emails}, {'_id': 0, 'phone': 1})
        email = self.responsible.find({"email": self.emails}, {'_id': 0, 'email': 1})
        age = self.responsible.find({"email": self.emails}, {'_id': 0, 'age': 1})
        ids = self.responsible.find({"email": self.emails}, {'_id': 0, 'id': 1})

        for index, c in enumerate(count):
            idss = str(ids[index])
            fn = str(first_name[index])
            ln = str(last_name[index])
            ph = str(phone[index])
            em = str(email[index])
            ag = str(age[index])
            var = f"Id: {idss[8:len(idss) - 2]}\n\n" \
                  f"First name: {fn[16:len(fn) - 2]}\n\n" \
                  f"Last name: {ln[15:len(ln) - 2]}\n\n" \
                  f"Phone: {ph[11:len(ph) - 2]}\n\n" \
                  f"Email: {em[11:len(em) - 2]}\n\n" \
                  f"Age: {ag[8:len(ag) - 1]}"
            self.profile_frame.add_data(var)

    def show_home(self):
        if self.home_b:
            self.home_b = False
            self.profile_b = True
            self.filter_b = True
            self.create_transport_b = True
            self.map_b = True
            self.qr_b = True

            try:
                self.profile_frame.place_forget()
            except:
                pass

            try:
                self.filter_frame.place_forget()
            except:
                pass

            try:
                self.create_transport.place_forget()
            except:
                pass

            try:
                self.map_frame.place_forget()
            except:
                pass

            try:
                self.qr_frame.place_forget()
            except:
                pass

            # if not self.filter_frame.forget():
            #     self.filter_frame.place_forget()

    def show_filters(self):
        if self.filter_b:
            self.home_b = True
            self.profile_b = True
            self.filter_b = False
            self.create_transport_b = True
            self.map_b = True
            self.qr_b = True

            self.filter_frame = FilterFrame(self, self.x, self.y)
            self.filter_frame.save_button.configure(command=self.filters_command)

    def filters_command(self):
        for i in self.scrollable_frame.table_view:
            i.destroy()

        tlist = []
        transports = self.transport.find({}, {"_id": 0, "id_sofer": 1})
        transports2 = self.transport.find({}, {"_id": 0, "id_locatie": 1, "status": 1, "shipping_date": 1,
                                               "delivery_date": 1})
        idd = self.transport.find({}, {"_id": 0, "id_locatie": 1})
        status = self.transport.find({}, {"_id": 0, "status": 1})
        shipping_date = self.transport.find({}, {"_id": 0, "shipping_date": 1})
        deliver_date = self.transport.find({}, {"_id": 0, "delivery_date": 1})
        for t in enumerate(transports):
            var = str(t)
            tlist.append(var[18:len(var) - 3])

        id_loc = []
        locations = self.location.find({}, {"_id": 0, "address": 1})
        for i, l in enumerate(locations):
            var = str(l)
            id_loc.append(var[13:len(var) - 2])
            print(i)
            print(var[13:len(var) - 2])

        count = ''

        text_transports = []
        text_profile = []
        id_loc_list = []

        for index, t in enumerate(transports2):
            ids = str(idd[index])
            st = str(status[index])
            ss = str(shipping_date[index])
            dd = str(deliver_date[index])
            var = f"Id: {ids[16:len(ids) - 2]}\n" \
                  f"Status: {st[12:len(st) - 2]}\n" \
                  f"Shipping date: {ss[19:len(ss) - 2]}\n" \
                  f"Delivery date: {dd[19:len(dd) - 2]}"

            if dd[19:len(dd) - 2] == self.filter_frame.label_var.get():
                id_loc_list.append(ids[16:len(ids) - 2])
                text_transports.append(var)

        # transporters
        for i in enumerate(tlist):
            var = str(i)
            var = str(var[5:len(var) - 2])
            count = self.person.find({"id": var}, {'_id': 0, 'first_name': 1, 'last_name': 1})
            first_name = self.person.find({"id": var}, {'_id': 0, 'first_name': 1})
            last_name = self.person.find({"id": var}, {'_id': 0, 'last_name': 1})
            phone = self.person.find({"id": var}, {'_id': 0, 'phone': 1})
            email = self.person.find({"id": var}, {'_id': 0, 'email': 1})
            age = self.person.find({"id": var}, {'_id': 0, 'age': 1})
            ids = self.person.find({"id": var}, {'_id': 0, 'id': 1})

            for index, c in enumerate(count):
                idss = str(ids[index])
                fn = str(first_name[index])
                ln = str(last_name[index])
                ph = str(phone[index])
                em = str(email[index])
                ag = str(age[index])
                var = f"Id: {idss[8:len(idss) - 2]}\n" \
                      f"First name: {fn[16:len(fn) - 2]}\n" \
                      f"Last name: {ln[15:len(ln) - 2]}\n" \
                      f"Phone: {ph[11:len(ph) - 2]}\n" \
                      f"Email: {em[11:len(em) - 2]}\n" \
                      f"Age: {ag[8:len(ag) - 1]}"
                text_profile.append(var)
                # TableView(self, fg_color=WHITE, image_label=AVATAR_2, text_profile=var, text_transport='')
        try:
            i = 0
            for profile in enumerate(text_profile):
                var = text_transports[i]
                print(text_transports[i])
                var1 = id_loc_list[i]
                var2 = id_loc[int(var1) - 1]
                print(var2)
                self.scrollable_frame.table_view.append(
                    TableView(self.scrollable_frame, fg_color=WHITE, image_label=choice(docs), text_profile=profile[1],
                              text_transport=var, text_location=var2, show_pdf_btn=True))
                i += 1
        except:
            print("eroor")
            pass

    def show_create_transport(self):
        if self.create_transport_b:
            self.home_b = True
            self.profile_b = True
            self.filter_b = True
            self.create_transport_b = False
            self.map_b = True
            self.qr_b = True

            self.create_transport = CreateTransportFrame(self, self.x, self.y)

    def show_map(self):
        if self.map_b:
            self.home_b = True
            self.profile_b = True
            self.filter_b = True
            self.create_transport_b = True
            self.map_b = False
            self.qr_b = True

            self.map_frame = MapFrame(self, self.x, self.y)

    def show_qr(self):
        if self.map_b:
            self.home_b = True
            self.profile_b = True
            self.filter_b = True
            self.create_transport_b = True
            self.map_b = True
            self.qr_b = False

            self.qr_frame = QRFrame(self, self.x, self.y)


class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, x, y, var):
        super().__init__(parent, fg_color=GRAY, width=1500, height=750, corner_radius=40)

        # variables
        self.x = x
        self.y = y

        # database
        connection_string = 'mongodb://localhost:27017'
        client = MongoClient(connection_string)


        transport_app = client.transport_app
        self.person = transport_app.person
        self.transport = transport_app.transport
        self.printer = pprint.PrettyPrinter()

        self.table_view = []

        if var == 'start':
            self.start()
        else:
            self.filters_command()

        self.place(relx=x / 1600 - 0.009, rely=y / 900, relwidth=0.948, relheight=0.828)

    def start(self):
        # transporters
        count = self.person.find({}, {'_id': 0, 'first_name': 1, 'last_name': 1})
        first_name = self.person.find({}, {'_id': 0, 'first_name': 1})
        last_name = self.person.find({}, {'_id': 0, 'last_name': 1})
        phone = self.person.find({}, {'_id': 0, 'phone': 1})
        email = self.person.find({}, {'_id': 0, 'email': 1})
        age = self.person.find({}, {'_id': 0, 'age': 1})

        for index, i in enumerate(count):
            fn = str(first_name[index])
            ln = str(last_name[index])
            ph = str(phone[index])
            em = str(email[index])
            ag = str(age[index])
            var = f"First name: {fn[16:len(fn) - 2]}\n" \
                  f"Last name: {ln[15:len(ln) - 2]}\n" \
                  f"Phone: {ph[11:len(ph) - 2]}\n" \
                  f"Email: {em[11:len(em) - 2]}\n" \
                  f"Age: {ag[8:len(ag) - 1]}"

            self.table_view.append(
                TableView(self, fg_color=WHITE, image_label=choice(docs), text_profile=var, text_transport=''))

    def find_person_transport(self):

        for i in self.table_view:
            i.destroy()

        tlist = []
        transports = self.transport.find({}, {"_id": 0, "id_sofer": 1})
        transports2 = self.transport.find({}, {"_id": 0, "status": 1, "shipping_date": 1, "delivery_date": 1})
        status = self.transport.find({}, {"_id": 0, "status": 1})
        shipping_date = self.transport.find({}, {"_id": 0, "shipping_date": 1})
        deliver_date = self.transport.find({}, {"_id": 0, "delivery_date": 1})
        for t in enumerate(transports):
            var = str(t)
            tlist.append(var[18:len(var) - 3])

        count = ''

        text_transports = []
        text_profile = []

        for index, t in enumerate(transports2):
            st = str(status[index])
            ss = str(shipping_date[index])
            dd = str(deliver_date[index])
            var = f"Status: {st[12:len(st) - 2]}\n" \
                  f"Shipping date: {ss[19:len(ss) - 2]}\n" \
                  f"Delivery date: {dd[19:len(dd) - 2]}"
            text_transports.append(var)

        # transporters
        for i in enumerate(tlist):
            var = str(i)
            var = str(var[5:len(var) - 2])
            count = self.person.find({"id": var}, {'_id': 0, 'first_name': 1, 'last_name': 1})
            first_name = self.person.find({"id": var}, {'_id': 0, 'first_name': 1})
            last_name = self.person.find({"id": var}, {'_id': 0, 'last_name': 1})
            phone = self.person.find({"id": var}, {'_id': 0, 'phone': 1})
            email = self.person.find({"id": var}, {'_id': 0, 'email': 1})
            age = self.person.find({"id": var}, {'_id': 0, 'age': 1})
            ids = self.person.find({"id": var}, {'_id': 0, 'id': 1})

            for index, c in enumerate(count):
                idss = str(ids[index])
                fn = str(first_name[index])
                ln = str(last_name[index])
                ph = str(phone[index])
                em = str(email[index])
                ag = str(age[index])
                var = f"Id: {idss[8:len(idss) - 2]}\n" \
                      f"First name: {fn[16:len(fn) - 2]}\n" \
                      f"Last name: {ln[15:len(ln) - 2]}\n" \
                      f"Phone: {ph[11:len(ph) - 2]}\n" \
                      f"Email: {em[11:len(em) - 2]}\n" \
                      f"Age: {ag[8:len(ag) - 1]}"
                text_profile.append(var)
                # TableView(self, fg_color=WHITE, image_label=AVATAR_2, text_profile=var, text_transport='')
        i = 0
        for profile in enumerate(text_profile):
            var = text_transports[i]
            TableView(self, fg_color=WHITE, image_label=AVATAR_2, text_profile=profile[1], text_transport=var)
            i += 1

    def show_transports(self):
        pass

    def placement(self):
        self.place(relx=self.x / 1600 - 0.009, rely=self.y / 900, relwidth=0.948, relheight=0.828)


class ProfileFrame(ctk.CTkFrame):
    def __init__(self, parent, x, y, avatar):
        super().__init__(parent, fg_color=GRAY, width=1500, height=750, corner_radius=40)

        self.start_pos_photo = -0.3
        self.end_pos_photo = 0.1
        self.width = abs(0 - 0.3)

        self.start_pos_data = 1
        self.end_pos_data = 0.6

        self.pos_photo = self.start_pos_photo
        self.pos_data = self.start_pos_data
        self.in_start_pos_photo = True
        self.in_start_pos_data = True

        self.photo_frame = ctk.CTkFrame(self, corner_radius=40, fg_color=LIGHT_GREEN)
        self.data_frame = ctk.CTkFrame(self, corner_radius=40, fg_color=LIGHT_GREEN)

        self.photo_frame.place(relx=self.pos_photo, rely=0.05, relwidth=self.width, relheight=0.9)
        self.data_frame.place(relx=self.pos_data, rely=0.05, relwidth=self.width, relheight=0.9)

        self.add_image(avatar)

        # ctk.CTkButton(self, text='Click me', command=self.animate).pack()
        self.place(relx=x / 1600 - 0.009, rely=y / 900, relwidth=0.948, relheight=0.828)

    def add_image(self, avatar):
        ctk.CTkLabel(self.photo_frame, text='', image=avatar).place(relx=0.18, rely=0.2)
        ctk.CTkButton(self.photo_frame, text='Settings', corner_radius=20,
                      text_color='black', font=ctk.CTkFont(family=FONT, size=FONT_SIZE, weight='bold'),
                      fg_color=GRAY, width=200, height=100).place(relx=0.3, rely=0.7)

    def add_data(self, data):
        ctk.CTkLabel(self.data_frame, text=data, font=ctk.CTkFont(family=FONT, size=25, weight='bold')).place(relx=0.1,
                                                                                                              rely=0.2)

    def animate(self):
        if self.in_start_pos_photo:
            self.animate_forward()
        else:
            self.animate_backward()

        if self.in_start_pos_data:
            self.animate_forward_data()
        else:
            self.animate_backward_data()

    def animate_forward(self):
        if self.pos_photo < self.end_pos_photo:
            self.pos_photo += 0.008
            self.photo_frame.place(relx=self.pos_photo, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos_photo = False

        # if self.pos_data > self.end_pos_data:
        #     self.pos_data -= 0.008
        #     self.data_frame.place(relx=self.pos_data, rely=0.05, relwidth=self.width, relheight=0.9)
        #     self.after(10, self.animate_forward)
        # else:
        #     self.in_start_pos_data = False

    def animate_forward_data(self):
        if self.pos_data > self.end_pos_data:
            self.pos_data -= 0.008
            self.data_frame.place(relx=self.pos_data, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_forward_data)
        else:
            self.in_start_pos_data = False

    def animate_backward(self):
        if self.pos_photo > self.start_pos_photo:
            self.pos_photo -= 0.008
            self.photo_frame.place(relx=self.pos_photo, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_backward)
        else:
            self.in_start_pos_photo = True

        # if self.pos_data < self.start_pos_data:
        #     self.pos_data += 0.008
        #     self.data_frame.place(relx=self.pos_data, rely=0.05, relwidth=self.width, relheight=0.9)
        #     self.after(10, self.animate_backward)
        # else:
        #     self.in_start_pos_data = True

    def animate_backward_data(self):
        if self.pos_data < self.start_pos_data:
            self.pos_data += 0.008
            self.data_frame.place(relx=self.pos_data, rely=0.05, relwidth=self.width, relheight=0.9)
            self.after(10, self.animate_backward_data)
        else:
            self.in_start_pos_data = True


class WidgetsButton(ctk.CTkButton):
    def __init__(self, parent, row, column, column_span=1, row_span=1, sticky='', padx=0, **kwargs):
        super().__init__(parent, **kwargs)

        self.grid(row=row, column=column, columnspan=column_span, rowspan=row_span, sticky=sticky, pady=10, padx=padx)


class TableView(ctk.CTkFrame):
    def __init__(self, parent, text_profile, text_transport, text_location='', show_pdf_btn=False, image_label=AVATAR_1,
                 **kwargs):
        font = ctk.CTkFont(family=FONT, size=FONT_SIZE, weight='bold')

        super().__init__(parent, **kwargs, corner_radius=40)

        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')

        self.label2_var = ctk.StringVar(value=text_profile)
        self.label3_var = ctk.StringVar(value=text_transport)
        self.text_location = text_location

        self.label1 = ctk.CTkLabel(self, text='', image=image_label, fg_color=LIGHT_GREEN,
                                   width=100, height=300, corner_radius=40
                                   ).grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        self.label2 = ctk.CTkLabel(self, text=text_profile, textvariable=self.label2_var, image=NOTES,
                                   width=100, height=300, corner_radius=40, text_color='black', font=font,
                                   fg_color=LIGHT_GRAY
                                   ).grid(row=0, column=1, sticky='nsew', padx=20, pady=20)
        self.label3 = ctk.CTkLabel(self, text=text_transport, textvariable=self.label3_var, text_color='black',
                                   font=font, image=NOTES,
                                   fg_color=LIGHT_GRAY2, width=100, height=300, corner_radius=40
                                   ).grid(row=0, column=2, sticky='nsew', padx=20, pady=20)

        self.pdf_btn = ctk.CTkButton(self, text='PDF', font=font, fg_color=LIGHT_GREEN, corner_radius=10,
                                     width=100, height=50, command=self.pdf_generator)
        if show_pdf_btn:
            self.pdf_btn.grid(row=0, column=2, sticky='s', pady=60)
        self.pack(expand=True, fill='both', pady=20, padx=30)

    def pdf_generator(self):
        my_pdf = FPDF()
        my_pdf.add_page()
        my_pdf.set_font('ARIAL', 'B', size=40)
        my_pdf.fill_color = WHITE
        my_pdf.image('images/logo.png', 0, 0, 60, 30)

        text1 = f"\n\n\n\n\n{self.label2_var.get()}\n\n{self.label3_var.get()}\n\n{self.text_location}"
        my_pdf.cell(200, 50, txt='Transport Info', ln=1, align='C')

        my_pdf.set_font('ARIAL', size=16)
        my_pdf.multi_cell(0, 10, text1)

        file_path = filedialog.asksaveasfilename()
        if file_path:
            my_pdf.output(f"{file_path}.pdf")


class SearchBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=WHITE)

        ctk.CTkEntry(self, placeholder_text='Search', border_width=0,
                     fg_color=WHITE, width=158, height=50, corner_radius=20, text_color='black').pack(side='right')
        ctk.CTkLabel(self, text='', image=SEARCH).pack(side='left')

        self.grid(row=0, column=1, columnspan=2)


class FilterFrame(ctk.CTkFrame):
    def __init__(self, parent, x, y):
        super().__init__(parent, fg_color=LIGHT_GRAY2, width=1500, height=750, corner_radius=40)

        font = ctk.CTkFont(family=FONT, size=20, weight='bold')

        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.columnconfigure(0, weight=1, uniform='a')

        # variables
        self.label_var = ctk.StringVar()

        vector = []
        for i in range(24):
            if i >= 12:
                for j in range(60):
                    if j % 10 == 0:
                        if j == 0:
                            var = f"{i}:00"
                        else:
                            var = f"{i}:{j}"
                        vector.append(var)

        self.entry_hour = ctk.CTkOptionMenu(self, values=vector, fg_color=WHITE, corner_radius=20, width=400, height=50,
                                            text_color='black', button_color=LIGHT_GREEN3,
                                            button_hover_color=LIGHT_GREEN,
                                            dynamic_resizing=True)
        self.entry_hour.grid(row=2, column=0)

        self.label_date = ctk.CTkLabel(self, text='', textvariable=self.label_var, fg_color=WHITE, corner_radius=20,
                                       width=400, height=50,
                                       text_color='black', font=ctk.CTkFont(family=FONT, size=25, weight='bold')
                                       )

        self.label_date.grid(row=1, column=0)

        self.cal = Calendar(self, selectmode='day', year=2023, month=5, day2=15)
        self.cal.grid(row=0, column=0)

        self.button1 = ctk.CTkButton(self, text='Get date', font=font, fg_color=LIGHT_GREEN, corner_radius=20,
                                     width=100, height=50, command=self.get_date)
        self.button1.grid(row=1, column=0, sticky='n')

        self.save_button = ctk.CTkButton(self, text='Save', font=font, fg_color=LIGHT_GREEN, corner_radius=20,
                                         width=100,
                                         height=50)
        self.save_button.grid(row=3, column=0)

        self.place(relx=x / 1600 - 0.009, rely=y / 900, relwidth=0.948, relheight=0.828)

    def get_date(self):
        self.label_var.set(self.cal.get_date())


class CreateTransportFrame(ctk.CTkFrame):
    def __init__(self, parent, x, y):
        super().__init__(parent, fg_color=LIGHT_GRAY2, width=1500, height=750, corner_radius=40)

        # database
        connection_string = 'mongodb://localhost:27017'
        client = MongoClient(connection_string)

        transport_app = client.transport_app
        self.transport = transport_app.transport
        self.location = transport_app.location
        self.person = transport_app.person
        self.printer = pprint.PrettyPrinter()

        # font
        font = ctk.CTkFont(family=FONT, size=20, weight='bold')

        self.rowconfigure((0, 1), weight=1, uniform='a')
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')

        self.label = ctk.CTkLabel(
            self, text='Create transport',
            text_color='black', font=ctk.CTkFont(family=FONT, size=80, weight='bold')
        )

        self.label.grid(row=0, column=0, columnspan=3)

        self.locations = ['Choose location']
        self.id_persons = ['Choose transporter']

        id_address = self.location.find({}, {"_id": 0, "address": 1})
        for index in enumerate(id_address):
            var = str(index[1])
            self.locations.append(var[13:len(var) - 2])

        id_person = self.person.find({}, {"_id": 0, "id": 1})
        for index in enumerate(id_person):
            var = str(index[1])
            self.id_persons.append(var[8:len(var) - 2])

        self.combo_location = ctk.CTkComboBox(
            self, fg_color=WHITE, corner_radius=20, width=400, height=50, border_width=0, font=font,
            text_color='black', button_color=LIGHT_GREEN, button_hover_color=LIGHT_GREEN,
            values=self.locations)

        self.combo_gate = ctk.CTkComboBox(
            self, fg_color=WHITE, corner_radius=20, width=400, height=50, border_width=0, font=font,
            text_color='black', button_color=LIGHT_GREEN, button_hover_color=LIGHT_GREEN, values=['Choose gate'])

        self.combo_transporter = ctk.CTkComboBox(
            self, fg_color=WHITE, corner_radius=20, width=400, height=50, border_width=0, font=font,
            text_color='black', button_color=LIGHT_GREEN, button_hover_color=LIGHT_GREEN,
            values=self.id_persons)

        self.create_button = ctk.CTkButton(
            self, text='Create', font=font, fg_color=LIGHT_GREEN, corner_radius=20,
            width=100, height=50, command=self.add_transport)

        self.cale = Calendar(self, selectmode='day', year=2023, month=5, day2=15)

        self.combo_location.grid(row=0, column=0, sticky='s')
        self.combo_gate.grid(row=0, column=1, sticky='s')
        self.combo_transporter.grid(row=0, column=2, sticky='s')
        self.create_button.grid(row=1, column=1, sticky='s')
        self.cale.grid(row=1, column=1, sticky='n', pady=50)

        self.place(relx=x / 1600 - 0.009, rely=y / 900, relwidth=0.948, relheight=0.828)

    def add_transport(self):

        id_loc = self.location.find({}, {"_id": 0, "id": 1})
        id_address = self.location.find({}, {"_id": 0, "address": 1})
        id_var = -1
        loc = 'Choose location'

        for index, i in enumerate(self.locations):
            var = str(i)
            if var == self.combo_location.get():
                id_var = str(index + 1)
                loc = var

        count = self.transport.count_documents(filter={})
        # print(count)

        if count < 10:
            var = f"0{count}"
        else:
            var = str(count)

        document = {
            "id": var,
            "id_sofer": str(self.combo_transporter.get()),
            "id_locatie": id_var,
            "status": "shipped",
            "shipping_date": "N/A",
            "delivery_date": str(self.cale.get_date())
        }
        if str(self.combo_transporter.get()) == 'Choose transporter' or loc == 'Choose location':
            # ToastNotification(
            #     title='Warning',
            #     message='Incorrect choice',
            #     duration=2000,
            #     bootstyle='light',
            #     position=(50, 100, 'se')
            # )
            pass
        else:
            messagebox.showinfo('Transport created successfully')
            self.transport.insert_one(document)


# Testing()
