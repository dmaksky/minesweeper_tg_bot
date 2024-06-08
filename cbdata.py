from aiogram.filters.callback_data import CallbackData


class FieldCallbackFactory(CallbackData, prefix="field"):
    x: int
    y: int
    click_mode: str


class SwitchCallbackFactory(CallbackData, prefix="switch"):
    click_mode: str


class MenuCallbackFactory(CallbackData, prefix="menu"):
    mode: str
