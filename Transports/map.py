import customtkinter as ctk
from settings import *
import tkintermapview
from geopy.geocoders import Nominatim
from PIL import Image


class MapFrame(ctk.CTkFrame):
    def __init__(self, parent, x, y):
        ctk.set_appearance_mode('light')
        super().__init__(parent, fg_color=WHITE, width=1500, height=750, corner_radius=40)

        # data
        self.input_string = ctk.StringVar()

        # layout
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=8, uniform='a')

        # widgets
        self.map_widget = MapWidget(self, self.input_string, self.submit_location)
        self.side_panel = SidePanel(self, self.map_widget.set_style, self.map_widget.set_address)

        self.place(relx=x / 1600 - 0.009, rely=y / 900, relwidth=0.948, relheight=0.828)

    def submit_location(self, event):
        # get data
        geolocator = Nominatim(user_agent='my-user')
        location = geolocator.geocode(self.input_string.get())

        # update the map
        if location:
            self.map_widget.set_address(location.address)
            self.side_panel.history_frame.add_location_entry(location)

            # clear the input
            self.input_string.set('')
        else:
            self.map_widget.location_entry.error_animation()


class MapWidget(tkintermapview.TkinterMapView):
    def __init__(self, parent, input_string, submit_location):
        super().__init__(parent)
        self.grid(row=0, column=1, sticky='nsew')

        # entry widget
        self.location_entry = LocationEntry(self, input_string, submit_location)

    def set_style(self, view_style):
        if view_style == 'map':
            self.set_tile_server(MAIN_URL)
        if view_style == 'terrain':
            self.set_tile_server(TERRAIN_URL)
        if view_style == 'paint':
            self.set_tile_server(PAINT_URL)


class LocationEntry(ctk.CTkEntry):
    def __init__(self, parent, input_string, submit_location):
        self.color_index = 15
        color = COLOR_RANGE[self.color_index]

        self.error = False

        super().__init__(
            parent,
            textvariable=input_string,
            corner_radius=10,
            border_width=4,
            fg_color=ENTRY_BG,
            border_color=f"#F{color}{color}",
            text_color=TEXT_COLOR,
            font=ctk.CTkFont(family=TEXT_FONT, size=TEXT_SIZE)
        )
        self.place(relx=0.5, rely=0.95, anchor='center')

        self.bind('<Return>', submit_location)

        input_string.trace('w', self.remove_error)

    def error_animation(self):
        self.error = True
        if self.color_index > 0:
            self.color_index -= 1
            border_color = f"#F{COLOR_RANGE[self.color_index]}{COLOR_RANGE[self.color_index]}"
            text_color = f"#{COLOR_RANGE[-self.color_index - 1]}00"
            self.configure(border_color=border_color, text_color=text_color)
            self.after(40, self.error_animation)

    def remove_error(self, *args):
        if self.error:
            self.configure(border_color=ENTRY_BG, text_color=TEXT_COLOR)
            self.color_index = 15


class SidePanel(ctk.CTkFrame):
    def __init__(self, parent, set_style, update_map):
        super().__init__(parent, fg_color=SIDE_PANEL_BG)
        self.grid(row=0, column=0, sticky='nsew')

        # widgets
        ViewButtons(self, set_style)
        self.history_frame = HistoryFrame(self, update_map)


class HistoryFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, update_map):
        super().__init__(parent)
        self.pack(expand=True, fill='both', padx=5, pady=5)
        self.font = ctk.CTkFont(family=TEXT_FONT, size=TEXT_SIZE)
        self.update_map = update_map

        self.add_location_entry("Strada Vulcanului 15, Codlea 505100")
        self.add_location_entry("Bulevardul Traian 19, Hunedoara 331110")
        self.add_location_entry("Bulevardul Nicolae Bălcescu 186, Pitești 110101")
        self.add_location_entry("Strada Depozitelor 17, Hunedoara 330179")
        self.add_location_entry("Kosovska, Entrance Zvezda 4, Kragujevac 34000, Serbia")
        self.add_location_entry("Naseleno mesto bez ulicen sistem Recica, Tabanovce 1300, Macedonia de Nord")

    def add_location_entry(self, location):
        HistoryItem(self, location, self.font, self.update_map)


class HistoryItem(ctk.CTkFrame):
    def __init__(self, parent, location, font, update_map):
        super().__init__(parent)
        self.pack(fill='x')

        # data
        self.address = location
        # town = self.address.split(',')[0]
        # country = self.address.split(',')[-1]
        # if town == country:
        #     address_string = town
        # else:
        #     address_string = f"{town}, {country}"

        # widgets
        ctk.CTkButton(self, command=lambda: update_map(self.address), text=self.address[:15], font=font, anchor='w',
                      fg_color='transparent', hover_color=HISTORY_HOVER_COLOR,
                      text_color=TEXT_COLOR).pack(side='left')
        ctk.CTkButton(self, command=lambda: self.pack_forget(), text='x', font=font, anchor='e', fg_color='transparent',
                      hover_color=HISTORY_HOVER_COLOR, width=10,
                      text_color=TEXT_COLOR).pack(side='right')


class ViewButtons(ctk.CTkFrame):
    def __init__(self, parent, set_style,):
        super().__init__(parent, fg_color='transparent')
        self.pack(side='bottom', fill='both', padx=5, pady=5)

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')

        # images
        map_image = ctk.CTkImage(
            dark_image=Image.open(map_image_path),
            light_image=Image.open(map_image_path),
        )

        paint_image = ctk.CTkImage(
            dark_image=Image.open(paint_image_path),
            light_image=Image.open(paint_image_path),
        )

        terrain_image = ctk.CTkImage(
            dark_image=Image.open(terrain_image_path),
            light_image=Image.open(terrain_image_path),
        )

        # widgets
        ctk.CTkButton(self, text='', command=lambda: set_style('map'), width=60, image=map_image, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR).grid(row=0, column=0, sticky='w')
        ctk.CTkButton(self, text='', command=lambda: set_style('terrain'), width=60, image=paint_image, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR).grid(row=0, column=1)
        ctk.CTkButton(self, text='', command=lambda: set_style('paint'), width=60, image=terrain_image, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR).grid(row=0, column=2, sticky='e')
