import json
from pprint import pprint
from settings import DB

"""
Обробка json-файлу
"""

"""
films.json
[
   {"title": "...",
    "desk": "...",
    "url": "...",
    "photo": "..."
    "rating": "..."
    },
    
   {....},
]
"""

# CRUD


def get_films(data_file=DB) -> list:
    try:
        with open(data_file) as films_db:
            films = json.load(films_db)
            return films
    except json.decoder.JSONDecodeError:
        print("db is empty")
        return None


def get_film_by_id(film_id: int = 0, data_file=DB) -> dict:
    films: list = get_films(data_file)
    if films:
        return films[film_id]


def create_film(film: dict, data_file=DB):
    list_films: list = get_films(data_file)
    
    if list_films is None:
        list_films = []
    list_films.append(film)
    
    with open(data_file, "w") as films_db:
        json.dump(list_films, films_db, indent=4)
    
    return True


def edit_film():
    pass


def delete_film():
    pass


if __name__ == "__main__":
    # from settings import DB
    
    # pprint(get_film_by_id(1, DB))
    film = {
        "title": "KUNG FU PANDA 4",
        "desc": "Kung Fu Panda 4 is fun for the whole family -- maybe not as much fun as the first three, but still a good time. Read audience reviews",
        "url": "https://www.rottentomatoes.com/m/kung_fu_panda_4",
        "photo": "AgACAgIAAxkBAAPGZh_DPCFqkLzfF9Dm0IlJ270juBIAAjfZMRtTmAFJZWO1UXO_K90BAAMCAAN4AAM0BA",
        "rating": "72%"
    }
    
    create_film(film, DB)
