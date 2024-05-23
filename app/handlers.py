from pprint import pprint

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F

from app.data.db import get_films, get_film_by_id, create_film
from app.fsm import FilmCreateForm
from app.keyboards import main_menu_keyboard, build_films_keyboard, build_film_details_keyboard, cancel_states_keyboard
from settings import DB


# Усі обробники варто закріплювати за Router або Dispatcher
router = Router()


# Обробник для команди /start
@router.message(Command("start"))
@router.message(Command("menu"))
async def command_start_handler(message: Message) -> None:
    if message.text == "/start":
        await message.answer(f"Hello, {message.from_user.full_name}!",
                             reply_markup=main_menu_keyboard())
    else:
        await message.answer(f"Menu:",
                             reply_markup=main_menu_keyboard())


# Обробник для команди /films та повідомлення із текстом films
@router.message(Command("films"))
@router.message(F.text == "Перелік фільмів")
async def list_films(message: Message):
    films = get_films(data_file=DB)
    if films:
        keyboard = build_films_keyboard(films)
        await message.answer("Виберіть будь-який фільм:", reply_markup=keyboard)
    else:
        await message.answer("Нажаль зараз відсутні фільми. Спробуйте /create_film для створення нового.")


# Обробник для inline-кнопки детального опису фільма
@router.callback_query(F.data.startswith("film_"))
async def show_film_details(callback: CallbackQuery) -> None:
    film_id = int(callback.data.split("_")[-1])
    
    film: dict = get_film_by_id(film_id=film_id)
    
    photo_id = film.get('photo')
    
    text = f"Назва: {film.get('title')}\nОпис: {film.get('desc')}\nРейтинг: {film.get('rating')}"
    keyboard = build_film_details_keyboard(film_id, film)
    # await callback.message.answer(text=text, reply_markup=keyboard)
    await callback.message.answer_photo(photo_id, caption=text, reply_markup=keyboard)
    await callback.message.delete()


@router.callback_query(F.data == "back")
async def back_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()
    await callback.answer()
    await list_films(callback.message)  # відображення списку фільмів
   


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "відміна")
@router.message(F.text == "Cancel creating film")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Створення фільму відмінено",
        reply_markup=main_menu_keyboard()
    )


@router.message(Command("create_film"))
@router.message(F.text == "Додати новий фільм")
async def create_film_command(message: Message, state: FSMContext) -> None:
    # очистити кінцевий автомат на випадок, якщо він не був завершений коректно
    await state.clear()
    
    # починаємо кінцевий автомат з першого стану (State)
    await state.set_state(FilmCreateForm.title)
    await message.answer(text="Яка назва фільму?",
                         reply_markup=cancel_states_keyboard())


# другий стан  (State) кінцевий автомат
@router.message(FilmCreateForm.title)
async def proces_title(message: Message, state: FSMContext) -> None:
    # збеігаемо попереднє значення title
    data = await state.update_data(title=message.text)
    print(data)
    # змінюємо стан на наступний
    await state.set_state(FilmCreateForm.desc)
    await message.answer("Який опис фільму?",
                         reply_markup=cancel_states_keyboard())


@router.message(FilmCreateForm.desc)
async def process_desc(message: Message, state: FSMContext):
    data = await state.update_data(desc=message.text)
    await state.set_state(FilmCreateForm.url)
    
    await message.answer(f"Надайте посилання на фільм: {data.get('title')}",
                         reply_markup=cancel_states_keyboard())
    

@router.message(FilmCreateForm.url)
async def process_url(message: Message, state: FSMContext):
    if message.text.startswith("https://") or message.text.startswith("http://"):
        data = await state.update_data(url=message.text)
        print(data)
        await state.set_state(FilmCreateForm.photo)
        await message.answer(f"Надайте фото для афіши фільму: {data.get('title')}",
                             reply_markup=cancel_states_keyboard())
    else:
        data = await state.get_data()
        await message.answer(f"Невірне посилання на {data.get('title')}",
                             reply_markup=cancel_states_keyboard())
        
        
@router.message(FilmCreateForm.photo)
async def proces_photo_binary(message: Message, state: FSMContext) -> None:
    # збережемо найбільший розмір фото
    print(message.photo)
    
    if message.photo:
        photo = message.photo[-1]
        photo_id = photo.file_id

        data = await state.update_data(photo=photo_id)
        await state.set_state(FilmCreateForm.rating)
        await message.answer(f"Надайте рейтинг фільму: {data.get('title')}",
                             reply_markup=cancel_states_keyboard())
    else:
        data = await state.get_data()
        await message.answer(f"Це не фото, додай афішу до : {data.get('title')}")
        

# Завершуемо кінцевий автомат
@router.message(FilmCreateForm.rating)
async def proces_rating(message: Message, state: FSMContext) -> None:
    data = await state.update_data(rating=message.text)
    await state.clear()  # stop FSM
    # додаемо фільм у файл
    create_film(data)
    await message.answer(f"Фільму  {data.get('title')} додано до бібліотеки",
                         reply_markup=main_menu_keyboard())
