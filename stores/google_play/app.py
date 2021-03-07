from rx import Observable

from stores.model import App


class GooglePlayApp(App):
    @property
    def app_id(self) -> str:
        pass

    @property
    def country_code(self) -> str:
        pass

    @property
    def reviews(self) -> Observable:
        pass
