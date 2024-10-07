from PIL import Image
import customtkinter as ctk

FONT = 'Calibri'
FONT_SIZE = 16

LIGHT_GREEN = '#00b594'
LIGHT_GREEN2 = '#4ccfb7'
LIGHT_GREEN3 = '#00e0b7'
WHITE = '#ffffff'
GRAY = '#bfbfbf'
LIGHT_GRAY = '#d4d4d4'
LIGHT_GRAY2 = '#ebebeb'

CLOSE_EYE = 'images/close_eye.png'
OPEN_EYE = 'images/open_eye.png'
LOGO = 'images/logo.png'

HOVER_GREEN = '#33ffd9'
HOVER_WHITE = '#defff9'
HOVER_GRAY = '#e6fffa'


# map urls
MAIN_URL = "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
TERRAIN_URL = "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga"
PAINT_URL = "http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.png"

# colors
COLOR_RANGE = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
ENTRY_BG = '#FFF'
SIDE_PANEL_BG = '#EEE'
HISTORY_HOVER_COLOR = '#AAA'
BUTTON_COLOR = '#dbdbdb'
BUTTON_HOVER_COLOR = '#C9C9C9'

# text
TEXT_FONT = 'Helvetica'
TEXT_SIZE = 14
TEXT_COLOR = '#000'
CLOSE_ITEM_COLOR = '#555'

# image paths
map_image_path = 'images/map.png'
paint_image_path = 'images/paint.png'
terrain_image_path = 'images/terrain.png'

rows = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17)
columns = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17)

HOME_BLACK = Image.open('images/home_black.png')
HOME_BLACK_CTk = ctk.CTkImage(
    light_image=HOME_BLACK,
    dark_image=HOME_BLACK,
    size=(40, 40)
)

HOME_LIGHT = Image.open('images/home_light.png')
HOME_LIGHT_CTk = ctk.CTkImage(
    light_image=HOME_LIGHT,
    dark_image=HOME_LIGHT,
    size=(40, 40)
)

PROFILE = Image.open('images/profile.png')
PROFILE_CTk = ctk.CTkImage(
    light_image=PROFILE,
    dark_image=PROFILE,
    size=(40, 40)
)

QR_IMAGE = Image.open('images/qr_img.png')
QR_IMAGE_CTk = ctk.CTkImage(
    light_image=QR_IMAGE,
    dark_image=QR_IMAGE,
    size=(40, 40)
)

SETTINGS_IMAGE = Image.open('images/settings_img.png')
SETTINGS_IMAGE_CTk = ctk.CTkImage(
    light_image=SETTINGS_IMAGE,
    dark_image=SETTINGS_IMAGE,
    size=(40, 40)
)
CREATE_TRANSPORT_IMAGE = Image.open('images/create_transport.png')
CREATE_TRANSPORT_IMAGE = ctk.CTkImage(
    light_image=CREATE_TRANSPORT_IMAGE,
    dark_image=CREATE_TRANSPORT_IMAGE,
    size=(40, 40)
)


AVATAR_1 = Image.open('avatars/img.png')
AVATAR_1 = ctk.CTkImage(
    light_image=AVATAR_1,
    dark_image=AVATAR_1,
    size=(300, 300)
)

AVATAR_2 = Image.open('avatars/img_1.png')
AVATAR_2 = ctk.CTkImage(
    light_image=AVATAR_2,
    dark_image=AVATAR_2,
    size=(300, 300)
)

AVATAR_3 = Image.open('avatars/img_2.png')
AVATAR_3 = ctk.CTkImage(
    light_image=AVATAR_3,
    dark_image=AVATAR_3,
    size=(300, 300)
)

AVATAR_4 = Image.open('avatars/img_3.png')
AVATAR_4 = ctk.CTkImage(
    light_image=AVATAR_4,
    dark_image=AVATAR_4,
    size=(300, 300)
)

AVATAR_5 = Image.open('avatars/img_4.png')
AVATAR_5 = ctk.CTkImage(
    light_image=AVATAR_5,
    dark_image=AVATAR_5,
    size=(300, 300)
)

AVATAR_6 = Image.open('avatars/img_5.png')
AVATAR_6 = ctk.CTkImage(
    light_image=AVATAR_6,
    dark_image=AVATAR_6,
    size=(300, 300)
)

AVATAR_7 = Image.open('avatars/img_6.png')
AVATAR_7 = ctk.CTkImage(
    light_image=AVATAR_7,
    dark_image=AVATAR_7,
    size=(300, 300)
)

AVATAR_8 = Image.open('avatars/img_7.png')
AVATAR_8 = ctk.CTkImage(
    light_image=AVATAR_8,
    dark_image=AVATAR_8,
    size=(300, 300)
)

FILTERS = Image.open('images/filters.png')
FILTERS = ctk.CTkImage(
    light_image=FILTERS,
    dark_image=FILTERS,
    size=(40, 40)
)

SEARCH = Image.open('images/search.png')
SEARCH = ctk.CTkImage(
    light_image=SEARCH,
    dark_image=SEARCH,
    size=(20, 20)
)

NOTES = Image.open('images/notes.png')
NOTES = ctk.CTkImage(
    light_image=NOTES,
    dark_image=NOTES,
    size=(500, 300)
)

MAP = Image.open('images/map_image.png')
MAP = ctk.CTkImage(
    light_image=MAP,
    dark_image=MAP,
    size=(40, 40)
)

docs = [
    AVATAR_1,
    AVATAR_2,
    AVATAR_3,
    AVATAR_4,
    AVATAR_5,
    AVATAR_6,
    AVATAR_7,
    AVATAR_8
]