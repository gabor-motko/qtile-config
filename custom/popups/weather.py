from os.path import expanduser
from json import load as json_load

from qtile_extras.popup.toolkit import PopupAbsoluteLayout, PopupRelativeLayout, PopupText, PopupImage, PopupWidget
from theme import theme as tm

weather_icons_path = expanduser("~/.config/qtile/assets/weathericons/256/")

# Convert bearing in degrees to cardinal and intercardinal directions.
def degrees_to_compass8(deg):
    i = round(deg / 45) % 8
    return ("N", "NE", "E", "SE", "S", "SW", "W", "NW")[i]
    # return ("", "", "", "", "", "", "", "")[i]

# Convert bearing to the directions of a 16-point compass rose.
def degrees_to_compass16(deg):
    i = round(deg / 22.5) % 16
    return ("N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW")[i]


def coord_format(data):
    lon = float(data["lon"])
    lat = float(data["lat"])

    ew = "E" if lon >= 0 else "W"
    ns = "N" if lat >= 0 else "S"

    return f"{abs(lat):.4f} {ns} {abs(lon):.4f} {ew}"

def weather_popup(qtile, data):
    location = data["name"] if data["id"] else coord_format(data["coord"])
    weather_icon = data["weather"][0]["icon"] if len(data["weather"]) > 0 else "none"
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    temp_range = (data["main"]["temp_min"], data["main"]["temp_max"])
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    wind_dir = data["wind"]["deg"]

    sunrise = data["sys"]["sunrise"]
    sunset = data["sys"]["sunset"]

    control_defaults = dict(
        background = "#00000000",
        font = tm.font
    )

    controls = [
        PopupText(
            text = f"Weather ({location})",
            pos_x = 100, pos_y = 0,
            width = 300, height = 40,
            fontsize = 18,
            h_align = "center", v_align = "center",
            **(control_defaults | dict(
                font = tm.font_bold
            )),
        ),
        PopupImage(
            filename = f"{weather_icons_path}/{weather_icon}.png",
            pos_x = 0, pos_y = 20,
            height = 80, width = 80,
            mask = True,
            colour = "#ffffff",
            **control_defaults,
        ),
        PopupText(
            text = f"Temperature: {temp:.0f}°C (feels like {feels_like:.0f}°C)",
            pos_x = 100, pos_y = 40,
            width = 300, height = 20,
            fontsize = 16,
            h_align = "left", v_align = "center",
            **control_defaults
        ),
        PopupText(
            text = f"Humidity: {humidity:.0f}%",
            pos_x = 100, pos_y = 60,
            width = 300, height = 20,
            fontsize = 16,
            h_align = "left", v_align = "center",
            **control_defaults
        ),
        PopupText(
            text = f"Wind: {wind_speed:.0f}km/h {degrees_to_compass8(wind_dir)}",
            pos_x = 100, pos_y = 80,
            width = 300, height = 20,
            fontsize = 16,
            h_align = "left", v_align = "center",
            **control_defaults
        ),
    ]

    layout = PopupAbsoluteLayout(
        qtile, controls = controls,
        width = 400, height = 120,
        close_on_click = True,
        background = tm.bg_translucent,
        border = tm.fg_inactive, border_width = 2
    )

    layout.show(centered = True)
