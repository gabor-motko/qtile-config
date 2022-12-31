from qtile_extras.widget import GenPollUrl
from qtile_extras.widget import OpenWeather
from typing import Callable

QUERY_URL = "http://api.openweathermap.org/data/2.5/weather?"
DEFAULT_KEY = "7834197c2338888258f8cb94ae14ef49"


class OpenWeather2(OpenWeather):
    on_poll_callback: Callable = None

    def __init__(self, **config):
        OpenWeather.__init__(self, **config)
        if "callback" in config:
            self.on_poll_callback = config["callback"]
        self.response = None

    def parse(self, response):
        if self.on_poll_callback is not None:
            self.on_poll_callback(self, response)
        return OpenWeather.parse(self, response)
