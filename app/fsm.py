from aiogram.fsm.state import StatesGroup, State


class FilmCreateForm(StatesGroup):
    title = State()
    desc = State()
    url = State()
    photo = State()
    rating = State()
