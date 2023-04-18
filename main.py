import flet as ft
from pyowm import OWM
from pyowm.utils.config import get_default_config
config_dict = get_default_config()
config_dict['language'] = 'ru'


def find_weather(place):
    owm = OWM('43d81a375c5adea5d5d55f4714d6c52d', config_dict)
    mgr = owm.weather_manager()

    observation = mgr.weather_at_place(place)
    w = observation.weather
    print(w.detailed_status)
    print(w.temperature('celsius'))
    print(w.wind())
    return w.detailed_status, w.temperature('celsius'), w.wind()


def main(page: ft.Page):
    page.window_width = 650
    page.window_height = 500
    page.window_resizable = False
    page.window_always_on_top = True
    page.window_maximizable = False
    page.title = 'Погода'

    region = 'Астрахань'

    def close_dlg(e):
        nonlocal region
        dlg.open = False
        if dlg_text_field.value != '':
            region = dlg_text_field.value
        region_text.value = get_region()
        page.update()

    def get_region():
        return region

    dlg_text_field = ft.TextField(color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_GREY)

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text('Введите название города'),
        content=dlg_text_field,
        actions=[
            ft.ElevatedButton(text='Сохранить', on_click=close_dlg)
        ]
    )

    detailed_status, temp, wind = find_weather(get_region())

    def update_weather():
        nonlocal detailed_status, temp, wind
        detailed_status, temp, wind = find_weather(get_region())
        weather_description_text.value = f'Сейчас в ({region_text.value}) {get_description()}, {round(get_temp())} градусов'
        wind_data_box_text.value = f'Сейчас ветер дует с {get_wind_direction()} стороны,\nскорость {round(get_wind_speed())} м/с'
        return detailed_status, wind, temp

    def restart(e):
        print(update_weather())
        page.update()

    def get_temp():
        return temp['temp']

    def get_wind_speed():
        return wind['speed']

    def get_description():
        return detailed_status

    def get_wind_direction():
        wd = wind['deg']
        if wd > 340 or wd <= 25:
            return 'С'
        if 25 < wd <= 70:
            return 'СВ'
        if 70 < wd < 115:
            return 'В'
        if 115 < wd <= 160:
            return 'ЮВ'
        if 160 < wd <= 205:
            return 'Ю'
        if 205 < wd <= 250:
            return 'ЮЗ'
        if 250 < wd <= 300:
            return 'З'
        if 300 < wd <= 340:
            return 'СЗ'

    def open_change_region_dlg(e):
        page.dialog = dlg
        dlg.open = True
        page.update()

#
    region_text = ft.Text(get_region(), color=ft.colors.WHITE, size=18)
    region_container = ft.Container(
        region_text,
        width=350,
        height=60,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.BLUE_700,
        border_radius=20
    )

    change_region_btn = ft.ElevatedButton(text='Change Region', width=200,
                                          color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_500,
                                          on_click=open_change_region_dlg)

    region_row = ft.Row(controls=[region_container, change_region_btn],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10)
#

#
    weather_icon = ft.Container(content=ft.Icon(ft.icons.SUNNY), width=350, height=250,
                                bgcolor=ft.colors.BLUE_GREY_50, border_radius=17)

    weather_description_text = ft.Text(f'Сейчас в ({region_text.value}) {get_description()}, {round(get_temp())} градусов',
                                       color=ft.colors.WHITE, size=18, text_align=ft.alignment.center_right)

    weather_description = ft.Container(
        weather_description_text,
        alignment=ft.alignment.center_right,
        bgcolor=ft.colors.BLUE_700,
        border_radius=20,
        width=350,
        height=90,
        padding=10
    )

    weather_column = ft.Column(controls=[weather_icon, weather_description], spacing=15)
#
    wind_data_box_text = ft.Text(f'Сейчас ветер дует с {get_wind_direction()} стороны,\nскорость {round(get_wind_speed())} м/с',
                                 color=ft.colors.WHITE)
    wind_data_box = ft.Container(
        wind_data_box_text,
        alignment=ft.alignment.center_right,
        bgcolor=ft.colors.BLUE_700,
        border_radius=20,
        width=240,
        height=240,
        padding=ft.padding.only(right=15)
    )

    restart_bt = ft.ElevatedButton(text='ОБНОВИТЬ', on_click=restart,
                                   width=240, height=100, bgcolor=ft.colors.GREEN_200)

    wind_column = ft.Column(controls=[wind_data_box, restart_bt])
#

    down_row = ft.Row(controls=[weather_column, wind_column])

    all_column = ft.Column(controls=[region_row, down_row], spacing=15)

    page.add(all_column)

    print(detailed_status, wind)

    page.update()


ft.app(target=main)
